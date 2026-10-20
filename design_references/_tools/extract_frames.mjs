// usage: node frames.mjs <video file> <outdir> <count>
import { spawn } from 'node:child_process';
import { mkdtempSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
const [video, outdir, countArg] = process.argv.slice(2);
const count = Number(countArg || 10);
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9388;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
mkdirSync(outdir, { recursive: true });
const profile = mkdtempSync(join(tmpdir(), 'lab-frames-'));
const page = join(profile, 'v.html');
writeFileSync(page, `<html><body style="margin:0;background:#000"><video id="v" muted preload="auto" style="display:block" src="${pathToFileURL(video).href}"></video></body></html>`);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--allow-file-access-from-files', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
let id = 0; const pending = new Map();
try {
  for (let i = 0; i < 80; i++) { try { if ((await fetch(`http://127.0.0.1:${PORT}/json/version`)).ok) break; } catch {} await sleep(150); }
  const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } };
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expr) => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;
  await send('Page.navigate', { url: pathToFileURL(page).href });
  await sleep(1500);
  const meta = await ev(`new Promise(r => { const v = document.getElementById('v'); const go = () => r({d: v.duration, w: v.videoWidth, h: v.videoHeight, err: v.error && v.error.code}); if (v.readyState >= 1) go(); else { v.onloadedmetadata = go; v.onerror = go; setTimeout(go, 8000); } })`);
  console.log(JSON.stringify(meta));
  if (!meta || !meta.w) throw new Error('video did not load');
  await send('Emulation.setDeviceMetricsOverride', { width: meta.w, height: meta.h, deviceScaleFactor: 1, mobile: false });
  for (let k = 0; k < count; k++) {
    const at = Math.min(meta.d - 0.05, (meta.d * (k + 0.5)) / count);
    await ev(`new Promise(r => { const v = document.getElementById('v'); v.onseeked = () => setTimeout(r, 250); v.currentTime = ${at}; setTimeout(r, 4000); })`);
    const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 80 });
    const name = join(outdir, `f${String(k).padStart(2, '0')}_${at.toFixed(1)}s.jpg`);
    writeFileSync(name, Buffer.from(shot.result.data, 'base64'));
  }
  ws.close();
} finally { chrome.kill(); await sleep(300); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
