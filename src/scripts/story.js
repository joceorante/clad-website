import { SCENES } from "./story.config.js";

// Scroll-scrubbed keyframe engine. Each scene is a tall section with a sticky frame; progress p (0..1)
// is how far the section has scrolled. Every actor's pose is interpolated from its keyframes, and the
// feature list highlights whichever step p is in. Clicking a feature scrolls to where its step has finished.
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
const fmt = (v, kind) => kind === "pct" ? Math.round(v) + "%" : kind === "money" ? money.format(v) : Math.round(v).toLocaleString("en-US");

function apply(el, pose) {
  if (pose.x != null) el.style.left = pose.x + "%";
  if (pose.y != null) el.style.top = pose.y + "%";
  if (pose.w != null) el.style.width = pose.w + "%";
  if (pose.o != null) el.style.opacity = pose.o;
  if (pose.s != null || pose.r != null) el.style.transform = `rotate(${pose.r || 0}deg) scale(${pose.s ?? 1})`;
  if (pose.d != null) el.style.setProperty("--draw", pose.d);
  if (pose.v != null) el.querySelectorAll("[data-count]").forEach((t) => { t.textContent = fmt(pose.v, t.dataset.count); });
}

function poseAt(kf, p) {
  if (p <= kf[0].at) return kf[0];
  if (p >= kf[kf.length - 1].at) return kf[kf.length - 1];
  for (let i = 0; i < kf.length - 1; i++) {
    const a = kf[i], b = kf[i + 1];
    if (p >= a.at && p <= b.at) {
      const t = ease((p - a.at) / (b.at - a.at)), out = {};
      for (const k in a) { if (k === "at") continue; out[k] = typeof a[k] === "number" && typeof b[k] === "number" ? a[k] + (b[k] - a[k]) * t : a[k]; }
      return out;
    }
  }
  return kf[kf.length - 1];
}

function mount(cfg) {
  const sec = document.getElementById(`story-${cfg.id}`);
  if (!sec) return;
  const stage = sec.querySelector(".stage");
  const actors = cfg.actors.map((a) => ({ ...a, el: stage.querySelector(`.act[data-a="${a.id}"]`) }));
  const feats = Array.from(sec.querySelectorAll(".feats li"));
  let current = -1;
  const total = () => sec.offsetHeight - window.innerHeight;

  function render(p) {
    for (const a of actors) if (a.el) apply(a.el, poseAt(a.kf, p));
    let s = 0;
    cfg.steps.forEach((t, i) => { if (p >= t) s = i; });
    if (s !== current) { current = s; feats.forEach((li, i) => li.classList.toggle("is-active", i === s)); }
  }
  function measure() {
    const p = clamp(-sec.getBoundingClientRect().top / total(), 0, 1);
    render(reduce ? (p < 0.5 ? 0 : 1) : p);
  }
  feats.forEach((li, i) => li.querySelector("button")?.addEventListener("click", () => {
    const top = window.scrollY + sec.getBoundingClientRect().top + cfg.rest[i] * total();
    window.scrollTo({ top, behavior: reduce ? "auto" : "smooth" });
  }));
  // scroll events are already delivered once per frame, so render directly
  window.addEventListener("scroll", measure, { passive: true });
  window.addEventListener("resize", measure);
  measure();
}

SCENES.forEach(mount);

// Each pinned frame is a full viewport tall with its content centered, which leaves empty space above the
// first scene and below the last before they pin. Pull the story up and the next section in by that slack
// so the gaps to the neighbouring sections stay a fixed size.
const story = document.getElementById("story");
function trimSlack() {
  if (!story) return;
  const scenes = story.querySelectorAll(".scene");
  if (!scenes.length) return;
  const slack = (sc) => {
    const pin = sc.querySelector(".pin");
    const h = Math.max(...Array.from(pin.children, (c) => c.offsetHeight));
    return Math.max(0, (pin.clientHeight - h) / 2);
  };
  const gap = window.innerWidth <= 900 ? 64 : 112;
  story.style.marginTop = `${gap - slack(scenes[0])}px`;
  story.style.marginBottom = `${gap - slack(scenes[scenes.length - 1])}px`;
}
trimSlack();
window.addEventListener("resize", trimSlack);
document.fonts?.ready.then(trimSlack);
