// Accessibility fixes Streamlit's own markup cannot express from Python. Injected once per page by
// widgets.enhance_accessibility(); it re-applies itself whenever Streamlit re-renders, so every rerun is covered.
// What it does, all on elements Streamlit already rendered:
//   - declares the page Vietnamese (Streamlit ships lang="en", so screen readers used an English voice);
//   - names Streamlit's English-labelled controls in Vietnamese;
//   - turns the visible "*" of a required field into aria-required, instead of a spoken "star";
//   - ties each field's range hint and error to its input (aria-describedby, aria-invalid);
//   - lets the error summary's links move focus to their field;
//   - announces a new estimate or failure through one polite live region.
(() => {
  if (window.__repA11y) { window.__repA11y(); return; }

  const NAMES = {
    "Clear value": "Xoá giá trị", "Open": "Mở danh sách", "Close": "Đóng danh sách",
    "Increment": "Tăng", "Decrement": "Giảm",
    "Show data": "Xem dữ liệu", "Copy Vega-Lite spec": "Sao chép mô tả biểu đồ",
    "Fullscreen": "Toàn màn hình", "Close fullscreen": "Thoát toàn màn hình",
    "Scroll tabs left": "Cuộn tab sang trái", "Scroll tabs right": "Cuộn tab sang phải",
  };

  const live = document.createElement("div");
  live.id = "rep-live";
  live.className = "lab-sr";
  live.setAttribute("role", "status");
  live.setAttribute("aria-live", "polite");
  document.body.appendChild(live);
  let announced = "";

  function run() {
    document.documentElement.lang = "vi";

    for (const el of document.querySelectorAll("[aria-label]")) {
      const vi = NAMES[el.getAttribute("aria-label")];
      if (vi) el.setAttribute("aria-label", vi);
    }
    for (const el of document.querySelectorAll('input[placeholder="Choose an option"]')) el.placeholder = "Chọn";

    for (const el of document.querySelectorAll("input[aria-label]")) {
      const m = el.getAttribute("aria-label").match(/^(.*?)\s*\\?\*$/);
      if (m) {
        el.setAttribute("aria-label", m[1]);
        el.setAttribute("aria-required", "true");
      }
    }

    // reset what an earlier run tied, then tie each note (hint, error) to the field rendered just before it
    for (const el of document.querySelectorAll("input[data-rep-note]")) {
      el.removeAttribute("aria-describedby");
      el.removeAttribute("aria-invalid");
      el.removeAttribute("data-rep-note");
    }
    let n = 0;
    for (const note of document.querySelectorAll(".lab-note")) {
      const box = note.closest('[data-testid="stElementContainer"]');
      const input = box && box.previousElementSibling && box.previousElementSibling.querySelector("input");
      if (!input) continue;
      note.id = note.id || "rep-note-" + n++;
      input.setAttribute("aria-describedby", note.id);
      input.setAttribute("aria-invalid", note.querySelector(".lab-err") ? "true" : "false");
      input.setAttribute("data-rep-note", "");
    }

    const a = document.querySelector("[data-announce]");
    if (a) {
      const key = a.getAttribute("data-announce-id") + "|" + a.getAttribute("data-announce");
      if (key !== announced) {
        announced = key;
        live.textContent = "";
        setTimeout(() => { live.textContent = a.getAttribute("data-announce"); }, 80);
      }
    }
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[data-focus]");
    if (!link) return;
    const input = document.querySelector(".st-key-" + link.dataset.focus + " input");
    if (!input) return;
    event.preventDefault();
    const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    input.scrollIntoView({ block: "center", behavior: calm ? "auto" : "smooth" });
    input.focus({ preventScroll: true });
  });

  let queued = false;
  new MutationObserver(() => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => { queued = false; run(); });
  }).observe(document.body, { subtree: true, childList: true, attributes: true, attributeFilter: ["aria-label", "placeholder"] });

  window.__repA11y = run;
  run();
})();
