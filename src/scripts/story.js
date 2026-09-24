import { SCENES } from "./story.config.js";

// Scroll-scrubbed keyframe engine. Each scene is a tall section with a sticky stage; progress p (0..1)
// is how far the section has scrolled, and every actor's pose is interpolated from its keyframes.
// An actor with a `skin` range crossfades its first child into its second across that range.
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const smooth = (p, a, b) => { const t = clamp((p - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const UNITS = { x: "left", y: "top", w: "width", h: "height" };

function apply(el, pose) {
  for (const k in UNITS) if (pose[k] != null) el.style[UNITS[k]] = pose[k] + "%";
  if (pose.o != null) el.style.opacity = pose.o;
  if (pose.r != null || pose.s != null)
    el.style.transform = (pose.r != null ? `rotate(${pose.r}deg) ` : "") + (pose.s != null ? `scale(${pose.s})` : "");
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
  let ticking = false;

  function render(p) {
    for (const a of actors) {
      if (!a.el) continue;
      apply(a.el, poseAt(a.kf, p));
      if (a.skin) { const k = smooth(p, a.skin[0], a.skin[1]); a.el.children[0].style.opacity = 1 - k; a.el.children[1].style.opacity = k; }
    }
  }
  function measure() {
    ticking = false;
    const r = sec.getBoundingClientRect(), total = sec.offsetHeight - window.innerHeight;
    const p = clamp(-r.top / total, 0, 1);
    render(reduce ? (p < 0.5 ? 0 : 1) : p);
  }
  window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(measure); } }, { passive: true });
  window.addEventListener("resize", measure);
  measure();
}

SCENES.forEach(mount);
