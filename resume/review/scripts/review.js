// Shared behaviour for review pages in review/.
//
//   Pop-up:  a button with [data-lightbox] opens dialog.lightbox and shows the
//            button's <img> full size. Esc, the close button, or a click
//            anywhere closes it.
//   Contents: links in nav.toc are marked .active while their section is
//            on screen. Sections are the elements their hrefs point to.
//   Notes:   an element with [data-note] gets a hand-drawn mark from
//            rough-notation (scripts/rough-notation.iife.js, loaded first),
//            drawn the first time it scrolls into view.
//              data-note="highlight | underline | box | circle | bracket |
//                         strike-through | crossed-off"
//              data-note-tone="fail | warn | pass | accent | marker"
//                (default: marker for highlight, fail for the rest)
//            Reduced motion draws the marks without animation.

const dialog = document.querySelector("dialog.lightbox");
if (dialog) {
  const big = dialog.querySelector("img");
  document.querySelectorAll("[data-lightbox]").forEach((button) => {
    button.addEventListener("click", () => {
      const img = button.querySelector("img");
      big.src = img.currentSrc || img.src;
      big.alt = img.alt;
      dialog.showModal();
    });
  });
  // Any click closes: the image, the backdrop, or the close button.
  dialog.addEventListener("click", () => dialog.close());
}

const links = [...document.querySelectorAll("nav.toc a[href^='#']")];
const targets = links.map((a) => document.getElementById(a.hash.slice(1))).filter(Boolean);
if (targets.length) {
  const mark = () => {
    // The active section is the last one whose heading has passed the top third of the screen.
    const line = window.innerHeight / 3;
    let current = targets[0];
    for (const t of targets) if (t.getBoundingClientRect().top <= line) current = t;
    // At the bottom of the page, the last section is active even if it's short.
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 2) current = targets.at(-1);
    links.forEach((a) => a.classList.toggle("active", a.hash === "#" + current.id));
  };
  document.addEventListener("scroll", mark, { passive: true });
  window.addEventListener("resize", mark);
  mark();
}

const notes = document.querySelectorAll("[data-note]");
if (notes.length && window.RoughNotation) {
  const css = getComputedStyle(document.documentElement);
  const tones = {
    fail: css.getPropertyValue("--fail").trim(),
    warn: "#d48a00", // brighter than --warn so a thin stroke still reads as amber
    pass: css.getPropertyValue("--pass").trim(),
    accent: css.getPropertyValue("--accent").trim(),
    marker: "#ffe58a", // highlighter yellow; dark text stays above 12:1 on it
  };
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const draw = (el) => {
    const type = el.dataset.note;
    const tone = el.dataset.noteTone || (type === "highlight" ? "marker" : "fail");
    RoughNotation.annotate(el, {
      type,
      color: tones[tone] || tone,
      strokeWidth: type === "highlight" ? 1 : 1.6,
      padding: type === "circle" ? 6 : type === "box" ? 3 : type === "highlight" ? 1 : 2,
      iterations: type === "highlight" ? 1 : 2,
      multiline: true,
      animate: !still,
      animationDuration: 700,
    }).show();
  };
  // Draw each mark once, when it first comes into view.
  const seen = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { seen.unobserve(e.target); draw(e.target); }
  }, { rootMargin: "0px 0px -10% 0px" });
  notes.forEach((el) => seen.observe(el));
}
