// The locked model (models/candidates/final_v2_2026-10-20), evaluated in JavaScript.
//
// data/model.json holds every fitted parameter of the two pipelines and every tree, written by
// web/scripts/export_web_data.py. This file applies them the way scikit-learn, XGBoost and LightGBM do:
//   features: City/District normalised -> StandardScaler -> imputer, one-hot, target encoding of the
//             City|District|Ward, City|Project and City|District|Street keys, in the ColumnTransformer's order;
//   XGBoost:  the matrix the pipeline makes is sparse, and XGBoost reads an absent entry (a zero) as missing;
//             values and split points are float32, a feature goes left when value < split;
//   LightGBM: an absent entry is the value 0; NaN goes the default way where the split was learned with
//             missing values, and counts as 0 elsewhere; a feature goes left when value <= threshold;
//   price:    0.5 x XGBoost + 0.5 x LightGBM, in tỷ đồng.
// tests/test_web_model.py checks the result against the pickled model on thousands of rows.
// Plain ES module with no dependencies: the browser and Node (the tests) both import it.

const f32 = Math.fround;

/** Same rule as notebook 03 (C03): NFC, collapse spaces, drop trailing periods. Missing stays missing. */
export function normalizeLocation(value) {
  if (value === null || value === undefined || (typeof value === "number" && Number.isNaN(value))) return null;
  return String(value).normalize("NFC").replace(/\s+/g, " ").trim().replace(/\.+$/, "").trim();
}

function isMissing(value) {
  return value === null || value === undefined || value === "" || (typeof value === "number" && Number.isNaN(value));
}

/** Turn the JSON into lookup tables once. */
export function loadModel(json) {
  const components = json.components.map((component) => {
    let width = 0;
    const blocks = component.preprocessing.map((block) => {
      const prepared = { ...block, offset: width };
      if (block.kind === "onehot") {
        prepared.index = block.categories.map((cats) => new Map(cats.map((c, i) => [c, i])));
        prepared.starts = [];
        for (const cats of block.categories) {
          prepared.starts.push(width);
          width += cats.length;
        }
      } else {
        if (block.kind === "target") prepared.maps = block.encodings.map((e) => new Map(Object.entries(e)));
        width += block.columns.length;
      }
      return prepared;
    });
    const trees = component.trees.map((t) => ({
      left: Int32Array.from(t.left),
      right: Int32Array.from(t.right),
      feature: Int32Array.from(t.feature),
      value: Float64Array.from(t.value),
      defaultLeft: Uint8Array.from(t.defaultLeft),
      missingNaN: t.missingNaN ? Uint8Array.from(t.missingNaN) : null,
    }));
    return { name: component.name, weight: component.weight, kind: component.kind, base: component.base, blocks, width, trees };
  });
  const model = { ...json, components };
  for (const check of json.checks || []) {
    const got = predict(model, check.input);
    if (!(Math.abs(got - check.price) < 1e-5)) {
      throw new Error(`model self-check failed: ${got} instead of ${check.price}`);
    }
    if (check.interval && model.interval) {
      const range = predictInterval(model, check.price);
      if (range.low !== check.interval[0] || range.high !== check.interval[1]) {
        throw new Error(`interval self-check failed: ${range.low}–${range.high} instead of ${check.interval.join("–")}`);
      }
    }
  }
  return model;
}

/** The 80% range of notebook 04 around a price (as model_interface.Interval.around): the price group's two ends,
 * clipped to the training prices, always containing the price. Null when model.json has no range. */
export function predictInterval(model, price) {
  const band = model.interval;
  if (!band) return null;
  const p = band.params;
  let low, high;
  if (p.method === "constant") {
    low = price - p.q;
    high = price + p.q;
  } else {
    let g = 0; // bisect_right: how many group edges are <= price
    while (g < p.edges.length && p.edges[g] <= price) g++;
    low = price + p.groups[g].q_lo;
    high = price + p.groups[g].q_hi;
  }
  const [floor, ceiling] = band.priceRange;
  low = Math.min(Math.min(Math.max(low, floor), ceiling), price);
  high = Math.max(Math.min(Math.max(high, floor), ceiling), price);
  return { low, high, coverage: band.coverage, rows: band.rows };
}

/** The row the ColumnTransformer outputs, as a dense vector (absent sparse entries are 0). */
function featureVector(component, input) {
  const x = new Float64Array(component.width);
  const city = normalizeLocation(input.City);
  const district = normalizeLocation(input.District);
  const located = { ...input, City: city, District: district };
  for (const block of component.blocks) {
    if (block.kind === "scale") {
      block.columns.forEach((column, i) => {
        const raw = located[column];
        let z = isMissing(raw) ? NaN : (Number(raw) - block.mean[i]) / block.scale[i];
        if (Number.isNaN(z) && block.fill) z = block.fill[i];
        x[block.offset + i] = z;
      });
    } else if (block.kind === "onehot") {
      block.columns.forEach((column, i) => {
        const raw = located[column];
        const value = isMissing(raw) ? block.fill[i] : String(raw);
        const at = block.index[i].get(value);
        if (at !== undefined) x[block.starts[i] + at] = 1; // unknown categories: all zeros (handle_unknown="ignore")
      });
    } else if (block.kind === "target") {
      block.parts.forEach((parts, i) => {
        const values = parts.map((p) => located[p]);
        const key = values.some(isMissing) ? block.fill : values.join(" | ");
        const encoded = block.maps[i].get(key);
        x[block.offset + i] = encoded === undefined ? block.default : encoded;
      });
    }
  }
  return x;
}

function xgboost(component, x) {
  let sum = f32(component.base);
  for (const t of component.trees) {
    let node = 0;
    while (t.feature[node] !== -1) {
      const v = x[t.feature[node]];
      if (v === 0 || Number.isNaN(v)) node = t.defaultLeft[node] ? t.left[node] : t.right[node];
      else node = f32(v) < t.value[node] ? t.left[node] : t.right[node];
    }
    sum = f32(sum + t.value[node]);
  }
  return sum;
}

function lightgbm(component, x) {
  let sum = 0;
  for (const t of component.trees) {
    let node = 0;
    while (t.feature[node] !== -1) {
      let v = x[t.feature[node]];
      if (Number.isNaN(v)) {
        if (t.missingNaN[node]) {
          node = t.defaultLeft[node] ? t.left[node] : t.right[node];
          continue;
        }
        v = 0;
      }
      node = v <= t.value[node] ? t.left[node] : t.right[node];
    }
    sum += t.value[node];
  }
  return sum;
}

/** Price in tỷ đồng. `input` holds the 12 dataset fields and the address parts Ward, Project, Street
 * as the model's parser writes them (lower case; a street without its leading "đường"/"phố"). */
export function predict(model, input) {
  let price = 0;
  for (const component of model.components) {
    const x = featureVector(component, input);
    const part = component.kind === "xgboost" ? xgboost(component, x) : lightgbm(component, x);
    price += component.kind === "xgboost" ? f32(component.weight * part) : component.weight * part;
  }
  return price;
}

/** Each component's own prediction, for the parity test. */
export function predictParts(model, input) {
  return Object.fromEntries(model.components.map((c) => {
    const x = featureVector(c, input);
    return [c.name, c.kind === "xgboost" ? xgboost(c, x) : lightgbm(c, x)];
  }));
}
