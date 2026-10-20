// Batch prediction with web/public/model.js, for tests/test_web_model.py.
//   node web/scripts/predict.mjs <model.json> <rows.json> <out.json>
// rows.json is a list of model inputs; out.json gets, per row, the price and each component's prediction.
import { readFileSync, writeFileSync } from "node:fs";
import { loadModel, predict, predictInterval, predictParts } from "../public/model.js";

const [modelPath, rowsPath, outPath] = process.argv.slice(2);
const model = loadModel(JSON.parse(readFileSync(modelPath, "utf8")));
const rows = JSON.parse(readFileSync(rowsPath, "utf8"));
const out = rows.map((row) => {
  const price = predict(model, row);
  const range = predictInterval(model, price);
  return { price, ...predictParts(model, row), low: range?.low ?? null, high: range?.high ?? null };
});
writeFileSync(outPath, JSON.stringify(out));
console.log(`${rows.length} rows predicted`);
