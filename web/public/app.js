// The web version of app/streamlit_app.py: same fields, rules, copy and figures, with the model running in
// the browser (model.js). Copy, schema and reference facts come from data/reference.json, which
// web/scripts/export_web_data.py writes from app/core, so both apps say the same thing.
import { loadModel, predict, predictInterval } from "./model.js";

const S = {
  model: null, modelStatus: "loading", modelProblem: "",
  attempted: false, outcome: { kind: "initial" }, backup: null,
  arrived: false, // set when someone asks for an estimate: the next render plays the arrival once
  pin: null, ringDeg: 0,
};
let REF, C, FIELDS, BY_NAME, UNKNOWN, LOC;

// ---------------------------------------------------------------- formatting (app/core/formatting.py)

/** Python's format(x, ".{d}f"): rounds the exact binary value, ties to even. */
function fixed(x, d) {
  const neg = x < 0;
  const [int, frac] = Math.abs(x).toFixed(100).split(".");
  let digits = int + frac.slice(0, d);
  const rest = frac.slice(d);
  const up = rest[0] > "5" || (rest[0] === "5" && (/[1-9]/.test(rest.slice(1)) || Number(digits.at(-1)) % 2 === 1));
  if (up) {
    const arr = digits.split("");
    let i = arr.length - 1;
    while (i >= 0 && arr[i] === "9") arr[i--] = "0";
    if (i < 0) arr.unshift("1"); else arr[i] = String(Number(arr[i]) + 1);
    digits = arr.join("");
  }
  const whole = d ? digits.slice(0, -d) || "0" : digits;
  const text = d ? `${whole}.${digits.slice(-d)}` : whole;
  return neg && /[1-9]/.test(text) ? `-${text}` : text;
}

function number(value, digits = 1, trim = true) {
  let text = fixed(value, digits);
  if (trim && text.includes(".")) text = text.replace(/0+$/, "").replace(/\.$/, "");
  const [whole, frac] = text.split(".");
  const grouped = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return frac === undefined ? grouped : `${grouped},${frac}`;
}
const count = (n) => number(n, 0);
const percent = (share) => `${number(share * 100, 0)}%`;
const price = (ty) => number(ty, 1, false);
function priceWords(ty) {
  const rounded = Number(fixed(ty, 1));
  const whole = Math.trunc(rounded);
  const trieu = Number(fixed((rounded - whole) * 1000, 0));
  const parts = [];
  if (whole) parts.push(`${count(whole)} tỷ`);
  if (trieu) parts.push(`${trieu} triệu`);
  return `tức ${(parts.length ? parts : ["0"]).join(" ")} đồng`;
}

// ---------------------------------------------------------------- small helpers

const $ = (selector, root = document) => root.querySelector(selector);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const icon = (name) => `<span class="ico" aria-hidden="true">${name}</span>`;
/** content.py strings use Python's "{name}" placeholders. */
const t = (key, params = {}) => C[key].replace(/\{(\w+)\}/g, (_, k) => params[k]);
const NBSP = " ";

const PRIVACY = "Mô hình chạy ngay trong trình duyệt của bạn: thông tin bạn nhập không được gửi đến máy chủ nào.";
const LOADING_MODEL = "Đang nạp mô hình…";
const LOAD_FAILED = "Không tải được dữ liệu của ứng dụng";
// how the form is laid out: fields per row, or column spans per row (as LAYOUT in streamlit_app.py)
const LAYOUT = { location: [2, 2, 1], size: [3], structure: [3], extra: [2, 1, 1] };

// ---------------------------------------------------------------- reading and writing the form

function parseDecimal(text) {
  const raw = String(text ?? "").trim();
  const cleaned = raw.toLowerCase().replace(/\s/g, "").replace(/(m²|m2|m)$/, "").replace(",", ".");
  if (!cleaned) return null;
  if (!/^[+-]?(\d+\.?\d*|\.\d+)(e[+-]?\d+)?$/.test(cleaned)) return raw;
  const value = Number(cleaned);
  return Number.isFinite(value) ? value : raw;
}

function readValues() {
  const values = {};
  for (const f of FIELDS) {
    const el = document.getElementById(f.key);
    if (f.kind === "decimal") values[f.name] = parseDecimal(el.value);
    else if (f.kind === "count") {
      if (el.validity.badInput) values[f.name] = el.value || "?";
      else values[f.name] = el.value === "" ? null : Number(el.value);
    } else if (f.kind === "choice") {
      const checked = el.querySelector("input:checked");
      values[f.name] = checked && checked.value ? checked.value : null;
    } else values[f.name] = el.value || null;
  }
  return values;
}

function writeValues(values) {
  const set = (name, value) => {
    const f = BY_NAME[name];
    const el = document.getElementById(f.key);
    if (f.kind === "choice") {
      for (const radio of el.querySelectorAll("input")) radio.checked = radio.value === (value ?? "");
    } else if (f.kind === "decimal") el.value = value == null ? "" : typeof value === "string" ? value : number(value, 1);
    else el.value = value ?? "";
  };
  set("City", values.City);
  fillDistricts();
  set("District", values.District);
  fillAddress();
  for (const f of FIELDS) if (f.name !== "City" && f.name !== "District") set(f.name, values[f.name]);
}

const location = (values) => LOC.get(`${values.City}|${values.District}`);

// ---------------------------------------------------------------- validation (app/core/validation.py)

function validate(values) {
  const errors = {};
  const warnings = {};
  for (const f of FIELDS) {
    const value = values[f.name];
    if (value === null || value === undefined) {
      if (f.required) errors[f.name] = REF.schema.requiredMessage[f.name];
      continue;
    }
    const label = f.label.toLowerCase();
    if (f.kind === "decimal" && typeof value === "string") {
      errors[f.name] = `Nhập ${label} bằng số, ví dụ ${f.placeholder.replace(/^Ví dụ: /, "")}.`;
      continue;
    }
    if (f.kind === "decimal") {
      if (f.name === "Frontage") { if (value < 0) errors[f.name] = "Nhập mặt tiền từ 0 trở lên."; }
      else if (value <= 0) errors[f.name] = `Nhập ${label} lớn hơn 0.`;
    } else if (f.kind === "count") {
      if (typeof value === "string" || value < 1 || !Number.isInteger(value)) {
        errors[f.name] = `Nhập ${label} là số nguyên từ 1 trở lên.`;
      }
    }
    const range = REF.ranges[f.name];
    if (errors[f.name] || !range) continue;
    const [low, high] = range;
    if (!(low <= value && value <= high)) {
      const unit = f.unit ? ` ${f.unit}` : "";
      warnings[f.name] = `${f.label} nằm ngoài khoảng có trong dữ liệu (${number(low)} – ${number(high)}${unit}), nên kết quả có thể kém tin cậy.`;
    }
  }
  if (values.Ward && !errors.Ward) {
    const ward = location(values)?.wards.find((w) => w.label === values.Ward);
    const rows = ward ? ward.rows : 0;
    if (rows < REF.schema.fewWardRows) warnings.Ward = t("WARD_FEW_ROWS", { n: count(rows) });
  }
  return { errors, warnings };
}

// ---------------------------------------------------------------- estimating

function modelInput(values) {
  const loc = location(values);
  const key = (list, label) => (label ? list.find((o) => o.label === label)?.key ?? null : null);
  const input = { Ward: key(loc.wards, values.Ward), Street: key(loc.streets, values.Street), Project: key(loc.projects, values.Project) };
  for (const name of ["Area", "Frontage", "Access Road", "House direction", "Balcony direction", "Floors",
    "Bedrooms", "Bathrooms", "Legal status", "Furniture state", "City", "District"]) input[name] = values[name];
  return input;
}

function submit() {
  const values = readValues();
  const { errors, warnings } = validate(values);
  S.backup = null;
  S.attempted = true;
  S.arrived = true;
  if (Object.keys(errors).length) S.outcome = { kind: "invalid", snapshot: values };
  else if (!S.model) S.outcome = { kind: "unavailable", snapshot: values };
  else {
    try {
      const ty = predict(S.model, modelInput(values));
      if (!Number.isFinite(ty)) throw new Error("non-finite prediction");
      S.outcome = { kind: "result", snapshot: values, price: ty, interval: predictInterval(S.model, ty), warnings };
    } catch (err) {
      console.error(err);
      S.outcome = { kind: "error", snapshot: values };
    }
  }
  render();
  if (S.outcome.kind === "invalid") $("#error-summary")?.focus();
}

function reset() {
  const values = readValues();
  if (Object.values(values).some((v) => v !== null)) S.backup = { values, outcome: S.outcome, attempted: S.attempted };
  writeValues({});
  S.attempted = false;
  S.outcome = { kind: "initial" };
  render();
}

function undoReset() {
  if (!S.backup) return;
  writeValues(S.backup.values);
  ({ outcome: S.outcome, attempted: S.attempted } = S.backup);
  S.backup = null;
  render();
}

// ---------------------------------------------------------------- building the form

function fieldLabel(f) {
  const text = f.unit ? `${f.label} (${f.unit})` : f.label;
  return f.required ? `${esc(text)} <span class="req" aria-hidden="true">*</span>` : esc(text);
}

function options(list, placeholder) {
  return (placeholder !== undefined ? `<option value="">${esc(placeholder)}</option>` : "")
    + list.map((v) => `<option value="${esc(v.value ?? v)}">${esc(v.text ?? v)}</option>`).join("");
}

function fieldHtml(f) {
  const id = f.key;
  const help = [];
  if (REF.ranges[f.name]) {
    const [low, high] = REF.ranges[f.name];
    const unit = f.unit ? `${NBSP}${f.unit}` : "";
    help.push(t("RANGE_HELP", { low: number(low), high: number(high), unit }).replace(" – ", `${NBSP}–⁠${NBSP}`));
  }
  if (C.ADDRESS_HELP[f.kind]) help.push(C.ADDRESS_HELP[f.kind]);
  const helpHtml = help.map((h) => `<p class="help">${esc(h)}</p>`).join("");
  const describedBy = `${id}-help ${id}-err`;
  let control;
  const req = f.required ? ' aria-required="true"' : "";
  if (["city", "district", "ward", "street", "project", "direction"].includes(f.kind)) {
    let list = "";
    if (f.kind === "city") list = options([...new Set(REF.locations.map((l) => l.city))], f.placeholder);
    else if (f.kind === "direction") {
      list = options((REF.options[f.name] || []), UNKNOWN);
    }
    control = `<div class="select"><select id="${id}" name="${id}" aria-describedby="${describedBy}"${req}>${list}</select></div>`;
  } else if (f.kind === "decimal") {
    control = `<input id="${id}" name="${id}" type="text" inputmode="decimal" autocomplete="off" maxlength="12" placeholder="${esc(f.placeholder)}" aria-describedby="${describedBy}"${req}>`;
  } else if (f.kind === "count") {
    control = `<input id="${id}" name="${id}" type="number" inputmode="numeric" min="1" step="1" placeholder="${esc(f.placeholder)}" aria-describedby="${describedBy}">`;
  } else if (f.kind === "choice") {
    const choices = [["", UNKNOWN], ...(REF.options[f.name] || []).map((v) => [v, REF.schema.choiceLabels[f.name]?.[v] ?? v])];
    control = `<div class="radios" id="${id}" role="radiogroup" aria-labelledby="${id}-label">${choices.map(([v, text], i) =>
      `<label class="radio"><input type="radio" name="${id}" value="${esc(v)}"${i === 0 ? " checked" : ""}><span>${esc(text)}</span></label>`).join("")}</div>`;
    return `<div class="field" data-field="${f.name}"><p class="label" id="${id}-label">${fieldLabel(f)}</p>${control}
      <div id="${id}-help">${helpHtml}</div><p class="err" id="${id}-err" hidden></p></div>`;
  }
  return `<div class="field" data-field="${f.name}"><label class="label" for="${id}">${fieldLabel(f)}</label>${control}
    <div id="${id}-help">${helpHtml}</div><p class="err" id="${id}-err" hidden></p></div>`;
}

function buildForm() {
  let html = "";
  Object.entries(REF.schema.groups).forEach(([group, label], i) => {
    const fields = FIELDS.filter((f) => f.group === group);
    html += `<h2 class="h2${i === 0 ? " h2--first" : ""}">${esc(label)}</h2><div class="rows">`;
    let at = 0;
    const layout = LAYOUT[group];
    for (let r = 0; at < fields.length; r++) {
      const perRow = layout[Math.min(r, layout.length - 1)];
      html += `<div class="row row--${perRow}">${fields.slice(at, at + perRow).map(fieldHtml).join("")}</div>`;
      at += perRow;
    }
    html += "</div>";
  });
  $("#fields").innerHTML = html;
  fillDistricts();
  fillAddress();

  const form = $("#form");
  form.addEventListener("submit", (e) => { e.preventDefault(); submit(); });
  form.addEventListener("input", onEdit);
  form.addEventListener("change", (e) => {
    if (e.target.id === BY_NAME.City.key) { fillDistricts(); fillAddress(); }
    if (e.target.id === BY_NAME.District.key) fillAddress();
    onEdit();
  });
  $("#reset").addEventListener("click", () => (S.backup ? undoReset() : reset()));
}

/** A new city: its districts. A new district: its wards, streets and projects (they are different lists). */
function fillDistricts() {
  const city = document.getElementById(BY_NAME.City.key).value;
  const el = document.getElementById(BY_NAME.District.key);
  const list = REF.locations.filter((l) => l.city === city).map((l) => l.district);
  el.innerHTML = options(list, city ? BY_NAME.District.placeholder : "Chọn tỉnh / thành phố trước");
  el.disabled = !city;
}

function fillAddress() {
  const values = { City: document.getElementById(BY_NAME.City.key).value, District: document.getElementById(BY_NAME.District.key).value };
  const loc = location(values);
  for (const name of ["Ward", "Street", "Project"]) {
    const f = BY_NAME[name];
    const el = document.getElementById(f.key);
    const list = loc ? loc[{ Ward: "wards", Street: "streets", Project: "projects" }[name]].map((o) => o.label) : [];
    const placeholder = name === "Ward" ? (values.District ? f.placeholder : "Chọn quận / huyện trước") : UNKNOWN;
    el.innerHTML = options(list, placeholder);
    el.disabled = !values.District;
  }
}

function onEdit() {
  render();
}

// ---------------------------------------------------------------- the result panel

function recap(values) {
  return FIELDS.map((f) => {
    const v = values[f.name];
    if (v === null || v === undefined) return [f.label, UNKNOWN];
    if (f.kind === "decimal" || f.kind === "count") return [f.label, `${number(Number(v))}${f.unit ? ` ${f.unit}` : ""}`];
    return [f.label, REF.schema.choiceLabels[f.name]?.[v] ?? String(v)];
  });
}

function unknownNote(values) {
  const names = FIELDS.filter((f) => !f.required && (values[f.name] === null || values[f.name] === undefined)).map((f) => f.label);
  return names.length ? t("UNKNOWN_SOME", { n: names.length, names: names.join(", ") }) : C.UNKNOWN_NONE;
}

function bands(values) {
  const rec = Object.fromEntries(recap(values));
  const where = [values.Street, values.Ward, values.District, values.City].filter(Boolean).join(", ") || UNKNOWN;
  const structure = [["Floors", "tầng"], ["Bedrooms", "phòng ngủ"], ["Bathrooms", "phòng tắm"]]
    .filter(([n]) => values[n] !== null && values[n] !== undefined && typeof values[n] === "number")
    .map(([n, label]) => `${count(values[n])} ${label}`.replaceAll(" ", NBSP)).join(" · ") || UNKNOWN;
  const rows = [["Vị trí", where], ["Diện tích", rec[BY_NAME.Area.label]], ["Kết cấu", structure], ["Pháp lý", rec[BY_NAME["Legal status"].label]]];
  return `<div class="bands">${rows.map(([k, v]) => `<div class="band"><span>${esc(k)}</span><span>${esc(v)}</span></div>`).join("")}</div>`;
}

function below(ty) {
  // how many training prices are lower than ty (bisect_left over the sorted prices)
  const list = REF.priceBelow;
  let lo = 0, hi = list.length;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (list[mid][0] < ty) lo = mid + 1; else hi = mid; }
  return lo < list.length ? list[lo][1] : REF.nRows;
}

function market(ty, arrived, range) {
  const bins = REF.priceHist;
  const p = REF.price;
  const lo = bins[0][0], hi = bins.at(-1)[1];
  const at = (x) => Math.max(0, Math.min(100, ((x - lo) / (hi - lo)) * 100));
  const pin = at(ty);
  const from = S.pin ?? 0;
  S.pin = pin;
  const share = below(ty) / REF.nRows;
  let note;
  if (ty < p.min || ty > p.max) note = t("MARKET_OUTSIDE", { low: number(p.min), high: number(p.max) });
  else if (share < 0.005) note = C.MARKET_LOWEST;
  else note = t("MARKET_SHARE", { pct: percent(share) });
  const label = t("MARKET_LABEL", { n: count(REF.nRows) });
  const top = Math.max(...bins.map((b) => b[2]));
  const cells = bins.map(([a, b, n], k) => {
    const hit = (a <= ty && ty < b) || (k === bins.length - 1 && ty === b);
    return `<span class="bin${hit ? " bin--hit" : ""}" style="--h:${((n / top) * 100).toFixed(1)}%" title="${esc(t("MARKET_BIN", { low: number(a), high: number(b), n: count(n) }))}"></span>`;
  }).join("");
  // the estimate's 80% range, shaded behind the bars
  const band = range ? `<div class="market-range" style="left:${at(range.low).toFixed(2)}%;right:${(100 - at(range.high)).toFixed(2)}%"></div>` : "";
  return `<div class="market"><p class="k">${esc(label)}</p>
    <div class="market-plot${arrived ? " is-moving" : ""}" role="img" aria-label="${esc(label)}. ${esc(note)}." style="--pin:${pin.toFixed(2)}%;--from-pin:${from.toFixed(2)}%">
      ${band}<div class="market-bars">${cells}</div><div class="market-pin"></div></div>
    <div class="market-axis"><span style="left:${at(p.min).toFixed(2)}%">${esc(t("MARKET_AXIS", { value: number(p.min) }))}</span>
      <span style="right:${(100 - at(p.max)).toFixed(2)}%">${esc(t("MARKET_AXIS", { value: number(p.max) }))}</span></div>
    <p class="market-note">${esc(note)}</p></div>`;
}

function trust() {
  const ev = REF.evaluation;
  return `<div><p class="k">${esc(C.TRUST_LABEL)}</p><p class="fact-v">${esc(t("TRUST_VALUE", { mae: number(ev.test.MAE, 2, false) }))}</p>
    <p class="small">${esc(t("TRUST_TEXT", { n: count(ev.testRows) }))}</p></div>`;
}

function renderResult(values, errors) {
  const panel = $("#result");
  let kind = S.outcome.kind;
  if (kind === "invalid" && !Object.keys(errors).length) kind = "fixed";
  if (kind === "initial" && S.modelStatus === "failed") kind = "unavailable";
  const arrived = S.arrived;
  S.arrived = false;
  const stale = ["result", "error"].includes(kind) && JSON.stringify(S.outcome.snapshot) !== JSON.stringify(values);
  const notes = [stale ? C.STALE : "", ...Object.values(S.outcome.warnings || {})].filter(Boolean)
    .map((text) => `<p class="note">${icon("warning")}${esc(text)}</p>`).join("");
  panel.className = `panel panel--result panel--${kind}`;
  if (kind !== "result") {
    S.pin = null; // no estimate on screen: the next one's pin travels from the strip's start
    let [heading, body] = C.STATE_TEXT[kind];
    if (kind === "unavailable" && S.modelProblem) body = `${body} ${t("BANNER_DETAIL", { reason: S.modelProblem })}`;
    panel.innerHTML = `${notes}<h2 class="state-h">${icon(C.STATE_ICON[kind])}${esc(heading)}</h2><p class="p">${esc(body)}</p>`
      + (kind === "error" ? `<button type="button" class="btn-secondary" id="retry">${icon("refresh")}${esc(C.RETRY)}</button>` : "");
    $("#retry")?.addEventListener("click", submit);
    if (arrived && kind !== "invalid") announce(`${heading}. ${body}`);
    $("#recap").hidden = true;
    return;
  }
  const ty = S.outcome.price;
  const range = S.outcome.interval;
  const uncertainty = range
    ? `<p class="fact-v">${esc(t("UNCERTAINTY_INTERVAL", { low: price(range.low), high: price(range.high) }))}</p>
       <p class="small">${esc(t("UNCERTAINTY_INTERVAL_TEXT", { n: count(range.rows), coverage: percent(range.coverage) }))}</p>`
    : `<p class="fact-v absent">${esc(C.UNCERTAINTY_NONE)}</p><p class="small">${esc(C.UNCERTAINTY_NONE_TEXT)}</p>`;
  panel.innerHTML = `<div class="result${arrived ? " arrive" : ""}">
    <p class="tag">${icon(C.STATE_ICON.result)}${esc(C.REAL_TAG)}</p>${notes}
    <h2 class="k">${esc(C.RESULT_LABEL)}</h2>
    <p class="price">${esc(price(ty))}<span class="unit">${esc(C.PRICE_UNIT)}</span></p>
    <p class="words">${esc(priceWords(ty))}</p>
    <p class="small statement">${esc(C.REAL_STATEMENT)}</p>
    <div class="facts">
      <div><p class="k">${esc(C.UNCERTAINTY_LABEL)}</p>${uncertainty}</div>
      ${trust()}
      <div class="fact--wide"><p class="k">${esc(C.PROVENANCE_LABEL)}</p><p class="small">${esc(REF.provenance)}</p></div>
    </div>${market(ty, arrived, range)}</div>`;
  if (arrived) {
    const said = range ? ` ${C.UNCERTAINTY_LABEL}: ${t("UNCERTAINTY_INTERVAL", { low: price(range.low), high: price(range.high) })}.` : "";
    announce(`${C.RESULT_LABEL}: ${price(ty)} ${C.PRICE_UNIT}, ${priceWords(ty)}.${said} ${C.REAL_TAG}.`);
  }
  const recapPanel = $("#recap");
  recapPanel.hidden = false;
  recapPanel.innerHTML = `<p class="k">${esc(C.RECAP_LABEL)}</p>${bands(S.outcome.snapshot)}`;
}

function announce(text) {
  const live = $("#announcer");
  live.textContent = "";
  setTimeout(() => { live.textContent = text; }, 50);
}

// ---------------------------------------------------------------- the form's own state

function renderErrors(errors) {
  const shown = S.attempted ? errors : {};
  for (const f of FIELDS) {
    const err = document.getElementById(`${f.key}-err`);
    const message = shown[f.name];
    err.hidden = !message;
    err.innerHTML = message ? `${icon("error")}${esc(message)}` : "";
    const control = document.getElementById(f.key);
    control.toggleAttribute("aria-invalid", Boolean(message));
    control.closest(".field").classList.toggle("has-error", Boolean(message));
  }
  const summary = $("#error-summary");
  const names = FIELDS.filter((f) => shown[f.name]);
  summary.hidden = !names.length;
  if (names.length) {
    summary.innerHTML = `${icon("error")}<div><p><strong>${esc(t("SUMMARY_HEADING", { n: names.length }))}</strong></p><ul>${names.map((f) =>
      `<li><a href="#${f.key}" data-focus="${f.key}"><strong>${esc(f.label)}</strong></a>: ${esc(shown[f.name])}</li>`).join("")}</ul></div>`;
  }
}

function renderRing(values) {
  const required = FIELDS.filter((f) => f.required);
  const done = required.filter((f) => values[f.name] !== null && values[f.name] !== undefined).length;
  const deg = Math.round((360 * done) / required.length);
  const from = S.ringDeg;
  S.ringDeg = deg;
  $("#ring").innerHTML = `<div class="ring-arc" style="--deg:${deg}deg;--from:${from}deg" role="img" aria-label="Đã điền ${done} trên ${required.length} mục bắt buộc"></div>
    <div><p class="ring-n">${done}/${required.length}</p><p class="k">mục bắt buộc đã điền</p>${done ? `<p class="small">${esc(unknownNote(values))}</p>` : ""}</div>`;
}

function renderActions() {
  const submitBtn = $("#submit");
  const ready = S.modelStatus === "ready";
  submitBtn.disabled = !ready;
  submitBtn.textContent = S.modelStatus === "loading" ? LOADING_MODEL : C.SUBMIT;
  $("#reset").innerHTML = S.backup ? `${icon("undo")}${esc(C.UNDO)}` : esc(C.RESET);
  const blocked = $("#blocked");
  blocked.hidden = S.modelStatus !== "failed";
  blocked.innerHTML = `${icon("lock")}${esc(C.DISABLED_REASON)}`;
}

function renderBanner() {
  const banner = $("#banner");
  if (S.modelStatus !== "failed") { banner.hidden = true; return; }
  banner.hidden = false;
  banner.innerHTML = `${icon("cloud_off")}<div><p>${esc(C.BANNER_UNAVAILABLE)}</p><p class="small">${esc(t("BANNER_DETAIL", { reason: S.modelProblem }))}</p></div>`;
}

function render() {
  const values = readValues();
  const { errors } = validate(values);
  renderErrors(errors);
  renderRing(values);
  renderActions();
  renderBanner();
  renderResult(values, errors);
}

// ---------------------------------------------------------------- accuracy and data views

function table(headers, rows, cls = "") {
  return `<div class="table-wrap"><table class="table ${cls}"><thead><tr>${headers.map((h, i) => `<th scope="col"${i ? ' class="num"' : ""}>${esc(h)}</th>`).join("")}</tr></thead>
    <tbody>${rows.map((row) => `<tr>${row.map((cell, i) => (i ? `<td class="num">${esc(cell)}</td>` : `<th scope="row">${esc(cell)}</th>`)).join("")}</tr>`).join("")}</tbody></table></div>`;
}

function head(title, lead) {
  return `<header class="head"><h1 class="h1">${esc(title)}</h1><p class="lead">${esc(lead)}</p></header>`;
}

function buildAccuracy() {
  const ev = REF.evaluation;
  const band = REF.interval; // the 80% range (notebook 05)
  const mae = number(ev.test.MAE, 2, false);
  const median = REF.price.median;
  const candidates = [...REF.candidates.rows].sort((a, b) => a.mean_cv_MAE - b.mean_cv_MAE);
  const modelRows = [["cv", ev.cv], ["validation", ev.validation], ["test", ev.test], ["test_new", ev.testNew]]
    .filter(([, m]) => m && m.MAE !== undefined)
    .map(([k, m]) => [C.EVAL_MODEL_ROWS[k], number(m.MAE, 3, false), number(m.RMSE, 3, false), number(m.R2, 3, false)]);
  const top = Math.max(...candidates.map((c) => c.mean_cv_MAE)) * 1.18;
  const chart = candidates.map((c, i) => `<div class="cv-row${i === 0 ? " cv-row--best" : ""}"><span class="cv-name">${esc(c.model)}</span>
    <span class="cv-track"><span class="cv-bar" style="width:${((c.mean_cv_MAE / top) * 100).toFixed(1)}%"></span><span class="cv-val">${esc(number(c.mean_cv_MAE, 3, false))}</span></span></div>`).join("");
  const verdict = ev.passed ? C.EVAL_FINAL_PASS : C.EVAL_FINAL_FAIL;
  $("#view-do-chinh-xac").innerHTML = `${head(C.NAV[1], C.EVAL_INTRO)}
    <div class="split">
      <section class="panel"><p class="k">${esc(C.TRUST_LABEL)}</p><p class="figure">${esc(t("TRUST_VALUE", { mae }))}</p>
        <p class="p measure">${esc(t("ACC_TEXT", { n: count(ev.testRows), mae, median: price(median), share: percent(ev.test.MAE / median) }))}</p>
        ${band ? `<p class="p measure">${esc(t("ACC_INTERVAL", { n: count(band.testRows), coverage: percent(band.testCoverage), width: number(band.meanWidth, 1, false) }))}</p>` : ""}
        <p class="small">${esc(t("ACC_NOTE", { new: percent(ev.newShare), mae_new: number(ev.testNew.MAE ?? ev.test.MAE, 2, false) }))}</p></section>
      <section class="panel"><p class="k">${esc(C.EVAL_FINAL_LABEL)}</p><p class="ring-n">${esc(t("EVAL_FINAL_VALUE", { r2: number(ev.test.R2, 3, false) }))}</p>
        <p class="small">${esc(t("EVAL_FINAL_TEXT", { n: count(ev.testRows), verdict }))}</p></section>
    </div>
    <details class="details"><summary>${esc(t("TEAM_DETAILS", { n: candidates.length }))}</summary><div class="details-body">
      <h2 class="h2 h2--first">${esc(C.EVAL_MODEL_HEADING)}</h2>${table(C.EVAL_MODEL_COLUMNS, modelRows, "table--plain")}
      <p class="small">${esc(t("EVAL_SOURCE", { path: C.EVAL_MODEL_SOURCE }))}</p>
      ${band ? `<h2 class="h2">${esc(C.EVAL_INTERVAL_HEADING)}</h2>
      <p class="small">${esc(t("EVAL_INTERVAL_TEXT", { cal: count(band.calibrationRows), val: percent(band.validationCoverage),
        test: percent(band.testCoverage), test_new: percent(band.testNewCoverage), width: number(band.meanWidth, 1, false) }))}</p>
      <p class="small">${esc(t("EVAL_SOURCE", { path: band.source }))}</p>` : ""}
      <h2 class="h2">${esc(C.EVAL_CV_HEADING)}</h2>
      <p class="small">${esc(C.EVAL_CV_KIND)} ${REF.candidates.folds ? esc(t("EVAL_CV_FOLDS", { k: REF.candidates.folds })) : ""}</p>
      <div class="cv-chart" role="img" aria-label="${esc(C.EVAL_CHART_AXIS)}">${chart}<p class="cv-axis">${esc(C.EVAL_CHART_AXIS)}</p></div>
      ${table(C.EVAL_COLUMNS, candidates.map((c) => [c.model, number(c.mean_cv_MAE, 3, false), number(c.mean_cv_RMSE, 3, false), number(c.mean_cv_R2, 3, false)]), "table--best")}
      ${C.METRIC_HELP.map(([k, v]) => `<p class="small"><strong>${esc(k)}</strong>: ${esc(v)}</p>`).join("")}
      <p class="small">${esc(t("EVAL_SOURCE", { path: REF.candidates.source }))}</p>
    </div></details>`;
}

function histogram() {
  const bins = REF.priceHist;
  const W = 640, H = 330, L = 52, R = 12, T = 26, B = 46;
  const lo = Math.floor(bins[0][0]), hi = Math.ceil(bins.at(-1)[1]);
  const top = Math.max(...bins.map((b) => b[2]));
  const step = top > 1000 ? 200 : 100;
  const yMax = Math.ceil(top / step) * step;
  const x = (v) => L + ((v - lo) / (hi - lo)) * (W - L - R);
  const y = (v) => T + (1 - v / yMax) * (H - T - B);
  const p = REF.price;
  let svg = `<rect x="${x(p.q1).toFixed(1)}" y="${T}" width="${(x(p.q3) - x(p.q1)).toFixed(1)}" height="${H - T - B}" class="hist-band"/>`
    + `<text x="${((x(p.q1) + x(p.q3)) / 2).toFixed(1)}" y="${T - 8}" class="hist-band-label" text-anchor="middle">${esc(C.DATA_MIDDLE_LABEL)}</text>`;
  for (let v = 0; v <= yMax; v += step) {
    svg += `<line x1="${L}" x2="${W - R}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" class="hist-grid"/>`
      + `<text x="${L - 8}" y="${(y(v) + 4).toFixed(1)}" text-anchor="end" class="hist-tick">${esc(count(v))}</text>`;
  }
  for (let v = lo; v <= hi; v += 1) {
    svg += `<text x="${x(v).toFixed(1)}" y="${H - B + 18}" text-anchor="middle" class="hist-tick">${esc(number(v, 1, false))}</text>`;
  }
  svg += bins.map(([a, b, n]) => `<rect x="${(x(a) + 1).toFixed(1)}" y="${y(n).toFixed(1)}" width="${(x(b) - x(a) - 2).toFixed(1)}" height="${(y(0) - y(n)).toFixed(1)}" class="hist-bar"><title>${esc(`${number(a)} – ${number(b)} tỷ đồng: ${count(n)} căn`)}</title></rect>`).join("");
  svg += `<text x="${(L + W - R) / 2}" y="${H - 6}" text-anchor="middle" class="hist-title">${esc(C.DATA_HIST_X)}</text>`
    + `<text transform="translate(14 ${(T + H - B) / 2}) rotate(-90)" text-anchor="middle" class="hist-title">${esc(C.DATA_HIST_Y)}</text>`;
  return `<svg class="hist" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(C.DATA_HIST_HEADING)}">${svg}</svg>`;
}

function buildData() {
  const p = REF.price;
  const facts = [
    [C.DATA_FACTS.source, C.DATA_SOURCE],
    [C.DATA_FACTS.rows, count(REF.nRows)],
    [C.DATA_FACTS.range, t("DATA_RANGE", { low: number(p.min), high: number(p.max) })],
    [C.DATA_FACTS.middle, t("DATA_RANGE", { low: number(p.q1), high: number(p.q3) })],
  ];
  const missing = FIELDS.map((f) => [f.label, REF.missing[f.name] ?? 0]).filter(([, s]) => s >= 0.01)
    .sort((a, b) => b[1] - a[1]).map(([label, s]) => [label, percent(s)]);
  $("#view-du-lieu").innerHTML = `${head(C.NAV[2], C.DATA_INTRO)}
    <div class="split">
      <div class="stack">
        <section class="panel"><h2 class="h2 h2--first">${esc(C.DATA_HIST_HEADING)}</h2>${histogram()}</section>
        <section class="panel"><p class="k">${esc(C.DATA_LIMITS_HEADING)}</p><ul class="list">${C.DATA_LIMITS.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></section>
      </div>
      <div class="stack">
        <section class="panel panel--flush"><div class="bands bands--flush">${facts.map(([k, v]) => `<div class="band"><span>${esc(k)}</span><span>${esc(v)}</span></div>`).join("")}</div></section>
        <section class="panel"><p class="k">${esc(C.DATA_MISSING_HEADING)}</p>${table(C.DATA_MISSING_COLUMNS, missing)}</section>
      </div>
    </div>`;
}

// ---------------------------------------------------------------- tabs

function setupTabs() {
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  tabs.forEach((tab, i) => { tab.textContent = C.NAV[i]; tab.dataset.view = C.VIEW_IDS[i]; });
  const show = (view, focus = false) => {
    for (const tab of tabs) {
      const on = tab.dataset.view === view;
      tab.setAttribute("aria-selected", String(on));
      tab.tabIndex = on ? 0 : -1;
      document.getElementById(tab.getAttribute("aria-controls")).hidden = !on;
      if (on && focus) tab.focus();
    }
    const url = new URL(window.location.href);
    if (view === C.VIEW_IDS[0]) url.searchParams.delete("view"); else url.searchParams.set("view", view);
    history.replaceState(null, "", url);
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener("click", () => show(tab.dataset.view));
    tab.addEventListener("keydown", (e) => {
      const move = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (move) { e.preventDefault(); show(tabs[(i + move + tabs.length) % tabs.length].dataset.view, true); }
    });
  });
  const wanted = new URL(window.location.href).searchParams.get("view");
  show(C.VIEW_IDS.includes(wanted) ? wanted : C.VIEW_IDS[0]);
}

// ---------------------------------------------------------------- start

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.json();
}

async function start() {
  const modelLoad = fetchJson("data/model.json").then(loadModel);
  try {
    REF = await fetchJson("data/reference.json");
  } catch (err) {
    $("#app").innerHTML = `<div class="banner banner--unavailable" role="alert">${icon("error")}<div><p>${esc(LOAD_FAILED)}</p><p class="small">${esc(err.message)}</p></div></div>`;
    return;
  }
  C = REF.copy;
  FIELDS = REF.schema.fields;
  BY_NAME = Object.fromEntries(FIELDS.map((f) => [f.name, f]));
  UNKNOWN = REF.schema.unknown;
  LOC = new Map(REF.locations.map((l) => [`${l.city}|${l.district}`, l]));

  document.title = C.TITLE;
  $("#view-uoc-tinh .head").outerHTML = head(C.TITLE, C.LEAD);
  $("#legend").textContent = C.REQUIRED_LEGEND;
  $("#privacy").textContent = PRIVACY;
  setupTabs();
  buildForm();
  buildAccuracy();
  buildData();
  $("#error-summary").addEventListener("click", (e) => {
    const link = e.target.closest("[data-focus]");
    if (!link) return;
    e.preventDefault();
    const target = document.getElementById(link.dataset.focus);
    (target.matches("input, select") ? target : target.querySelector("input"))?.focus();
  });
  document.body.classList.remove("is-loading");
  render();

  try {
    S.model = await modelLoad;
    S.modelStatus = "ready";
  } catch (err) {
    console.error(err);
    S.modelStatus = "failed";
    S.modelProblem = `Không nạp được mô hình (${err.message}).`;
  }
  render();
}

start();
