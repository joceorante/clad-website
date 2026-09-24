import json, sys, os
sys.path.insert(0, os.getcwd())
from build_e import s2_actors, s3_actors, S2_HTML, S3_HTML, S2_CAPS, S3_CAPS
from build_h import DELAY, RAW_HTML
from build_h import STARTS as _S, SLOTS as _L, CARD as _C
CARD=(30,22,40)
STARTS={"p1":(5,8,16,17,-7),"p2":(77,6,15,16,5),"p3":(80,58,15,16,-4),"pdf":(24,4,11,14,3),"qty":(5,60,20,14,4),"txt":(54,82,22,10,-3)}
def _conv(sl):
    x,y,w,h=sl; return (30+(x-33)*40/34, 22+(y-34)*1.15, w*40/34, h*1.15)
SLOTS={k:_conv(v) for k,v in _L.items()}

ROOT = "/Users/jocelynorante/Desktop/clad-site"

# ---- scene 1: capture (neutral raw inputs -> one field update) ----
def s1_actors():
    A=[]
    for sid,(sx,sy,sw,sh,sr) in STARTS.items():
        ex,ey,ew,eh=SLOTS[sid]; d=DELAY[sid]
        A.append({"id":sid,"kf":[
            {"at":d,"x":sx,"y":sy,"w":sw,"h":sh,"r":sr,"o":1},
            {"at":.66,"x":ex,"y":ey,"w":ew,"h":eh,"r":0,"o":1},
            {"at":.74,"x":ex,"y":ey,"w":ew,"h":eh,"r":0,"o":1},
            {"at":.8,"x":ex,"y":ey,"w":ew,"h":eh,"r":0,"o":0}],
            "skin":[d+(.66-d)*.55, d+(.66-d)*.95]})
    cx,cy,cw=CARD
    A.append({"id":"hero","kf":[{"at":.5,"x":cx,"y":cy,"w":cw,"o":0},{"at":.64,"x":cx,"y":cy,"w":cw,"o":1}]})
    A.append({"id":"herobody","kf":[{"at":.74,"o":0},{"at":.8,"o":1}]})
    A.append({"id":"stamp","kf":[{"at":.86,"o":0},{"at":.94,"o":1}]})
    return A

S1_HTML = "".join(f'<div class="act" data-a="{sid}">{RAW_HTML[sid]}</div>' for sid in STARTS) + '''
<div class="act card hero-card" data-a="hero">
  <div class="hd"><b>Field update · Mon, Sep 14</b><span class="k">Crew 3</span></div>
  <div class="body act" data-a="herobody">
    <div class="thumbs"><i></i><i></i><i></i><i class="pdf"></i></div>
    <div class="fields"><div><small>Fiber placed</small><b>1,000 FT</b></div><div><small>Hand holes</small><b>2 HH</b></div></div>
    <div class="note"><em>Note</em>Both hand holes set at 4th &amp; Main. Photos attached.</div>
  </div>
  <span class="stamp tagpill act" data-a="stamp">Ready for approval</span>
</div>'''
S1_CAPS=["Photos, a redline, quantities, a note. <b>Six things, one Monday.</b>","Clad gathers them into <b>a single field update</b>.","Entered once, from the truck. <b>Ready for approval.</b>"]

# neutral sub-bill document instead of the handwritten one
S3 = S3_HTML.replace('<div class="doc">Ortiz Underground<br>Inv 0231 — $4,100<br><small>1400ft fiber, Tue</small><i></i><i></i></div>',
                     '<div class="doc"><span class="k">Sub bill · PDF</span><b>Ortiz Underground</b><span>Inv 0231 · $4,100</span><i></i><i></i></div>')

SCENES=[
 {"id":"capture","num":"01","name":"Capture","accent":"cobalt","ink":"paper",
  "title":"Intuitive tools to collect the data you need from the field.","html":S1_HTML,"actors":s1_actors(),"caps":S1_CAPS,"capAt":[.3,.76]},
 {"id":"manage","num":"02","name":"Manage","accent":"orange","ink":"paper",
  "title":"Know where projects stand, and where they’re heading.","html":S2_HTML,"actors":s2_actors(),"caps":S2_CAPS,"capAt":[.36,.6]},
 {"id":"bill","num":"03","name":"Bill","accent":"stoplight","ink":"tar",
  "title":"Eliminate over- and under-billing.","html":S3,"actors":s3_actors(),"caps":S3_CAPS,"capAt":[.47,.73]},
]

def caps_html(caps):
    return "".join(f'<p class="cap{" on" if i==0 else ""}">{c}</p>' for i,c in enumerate(caps))

scenes_html=""
for sc in SCENES:
    scenes_html+=f'''
  <section class="scene" id="story-{sc["id"]}" data-scene="{sc["id"]}" style="--accent: var(--color-{sc["accent"]}); --accent-ink: var(--color-{sc["ink"]})">
    <div class="pin">
      <div class="head">
        <span class="pill num">{sc["num"]} · {sc["name"]}</span>
        <h3>{sc["title"]}</h3>
      </div>
      <div class="stage">{sc["html"]}</div>
      <div class="caps">{caps_html(sc["caps"])}</div>
    </div>
  </section>'''

astro = f'''---
/* Product story: three scroll-scrubbed scenes (Capture, Manage, Bill).
   Keyframes live in src/scripts/story.config.js; the engine in src/scripts/story.js.
   Ported from reference/prototypes/build_e.py and restyled to the Clad tokens. */
---
<div class="story container-wide" id="story" aria-label="How Clad works">{scenes_html}
</div>

<script src="../scripts/story.js"></script>

<style is:global>
  .story {{ margin-top: 148px; margin-bottom: 86px; }}
  .story .scene {{ position: relative; height: 320vh; }}
  .story .pin {{
    position: sticky; top: calc(72px + 20px); height: calc(100vh - 72px - 40px);
    display: flex; flex-direction: column; gap: 18px;
  }}
  .story .head {{ display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }}
  .story .head .num {{ color: var(--accent); border-color: var(--accent); }}
  .story .head h3 {{ font-size: clamp(20px, 2vw, 28px); line-height: 1.2; letter-spacing: -0.5px; font-weight: 600; }}
  .story .stage {{
    position: relative; flex: 1; min-height: 0; overflow: hidden;
    aspect-ratio: 16 / 9; width: auto; max-width: 100%; align-self: center;
    background: var(--color-tar) url("/assets/grid.svg") -505px -573px / 2214px 2211px no-repeat;
    border: 1px solid var(--color-tar); border-radius: var(--radius-lg);
    container-type: size; font-size: clamp(9px, 1.25cqw, 15px); color: var(--color-tar);
    --muted: color-mix(in srgb, var(--color-tar) 55%, white); --line: color-mix(in srgb, var(--color-tar) 18%, white);
    --card: color-mix(in srgb, var(--color-tar) 5%, white); --shape: color-mix(in srgb, var(--color-tar) 14%, white); --shape-2: color-mix(in srgb, var(--color-tar) 26%, white);
    --shadow: 0 30px 60px -30px rgb(0 0 0 / .7);
  }}
  .story .caps {{ position: relative; min-height: 2.6em; font-size: clamp(15px, 1.4vw, 18px); line-height: 1.4; color: var(--muted-page, #6b6858); }}
  .story .cap {{ position: absolute; inset: 0; margin: 0; opacity: 0; transform: translateY(6px); transition: opacity .35s, transform .35s; }}
  .story .cap.on {{ opacity: 1; transform: none; }}
  .story .cap b {{ color: var(--color-tar); font-weight: 600; }}

  /* ---- shared mock primitives (Paper cards on the Tar stage) ---- */
  .story .act {{ position: absolute; transform-origin: top left; }}
  .story .k {{ font-family: var(--font-mono); font-size: .78em; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }}
  .story .tagpill {{ font-family: var(--font-mono); font-size: .78em; letter-spacing: .1em; text-transform: uppercase; color: var(--accent); border: 1px solid var(--accent); border-radius: 999px; padding: .3em .8em; white-space: nowrap; display: inline-block; background: var(--color-paper); }}
  .story .card, .story .panel2 {{ background: var(--color-paper); border: 1px solid var(--line); border-radius: var(--radius-md); box-shadow: var(--shadow); }}
  .story .card {{ padding: 1.2em 1.4em; }}
  .story .card .hd, .story .panel2 .hd {{ display: flex; justify-content: space-between; align-items: baseline; gap: 1em; padding-bottom: .9em; border-bottom: 1px solid var(--line); margin-bottom: 1em; }}
  .story .panel2 .hd {{ padding: 1.1em 1.4em; margin: 0; }}
  .story .card .hd b, .story .panel2 .hd b {{ font-weight: 600; font-size: 1.15em; letter-spacing: -.01em; }}

  /* scene 1: raw inputs and the update card */
  .story .raw, .story .ui {{ position: absolute; inset: 0; border-radius: .7em; overflow: hidden; }}
  .story .ui {{ opacity: 0; }}
  .story .raw.photo {{ background: linear-gradient(160deg, var(--shape), var(--shape-2)); box-shadow: var(--shadow); }}
  .story .raw .lab {{ position: absolute; left: .6em; bottom: .5em; font-family: var(--font-mono); font-size: .72em; letter-spacing: .06em; color: var(--color-paper); background: rgb(0 0 0 / .45); border-radius: .4em; padding: .15em .5em; }}
  .story .raw.page {{ background: var(--color-paper); border: 1px solid var(--line); }}
  .story .raw.page::after {{ content: ""; position: absolute; left: 22%; top: 34%; width: 56%; height: 26%; border: 2px solid var(--color-orange); border-radius: 50% 45% 55% 40%; }}
  .story .raw.page .lab {{ color: var(--muted); background: transparent; padding-left: 0; }}
  .story .raw.memo {{ background: var(--color-paper); border: 1px solid var(--line); padding: .7em .9em .9em; font-size: 1em; line-height: 1.35; }}
  .story .raw.memo .lab, .story .raw.msg .lab {{ position: static; display: block; color: var(--muted); background: transparent; padding: 0; margin-bottom: .3em; }}
  .story .raw.msg {{ background: var(--card); border-radius: 1.2em 1.2em 1.2em .3em; padding: .6em .9em .9em; font-size: .98em; line-height: 1.35; }}
  .story .ui.thumb {{ background: linear-gradient(160deg, var(--shape), var(--shape-2)); border-radius: .6em; }}
  .story .ui.thumb.pdf {{ background: var(--card); border: 1px solid var(--line); }}
  .story .ui.thumb.pdf::after {{ content: ""; position: absolute; left: 18%; top: 38%; width: 64%; height: 24%; border: 2px solid var(--color-orange); border-radius: 50% 45% 55% 40%; }}
  .story .ui.fields {{ display: grid; grid-template-columns: 1fr 1fr; gap: .6em; border-radius: 0; overflow: visible; }}
  .story .ui.fields div, .story .fields div {{ border: 1px solid var(--line); border-radius: .6em; padding: .5em .8em; background: var(--color-paper); }}
  .story .ui.fields small, .story .fields small {{ display: block; font-family: var(--font-mono); font-size: .7em; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }}
  .story .ui.fields b, .story .fields b {{ font-weight: 600; font-size: 1.1em; font-variant-numeric: tabular-nums; }}
  .story .ui.note, .story .note {{ border: 1px solid var(--line); border-radius: .6em; padding: .5em .8em; background: var(--color-paper); display: flex; align-items: center; gap: .6em; font-size: .95em; }}
  .story .ui.note em, .story .note em {{ font-style: normal; font-family: var(--font-mono); font-size: .7em; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }}
  .story .hero-card {{ overflow: hidden; padding-bottom: 3.8em; }}
  .story .hero-card .body {{ position: static; opacity: 0; }}
  .story .hero-card .stamp {{ position: absolute; right: 1.2em; bottom: 1.1em; }}
  .story .thumbs {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: .6em; }}
  .story .thumbs i {{ aspect-ratio: 4/3; border-radius: .6em; background: linear-gradient(160deg, var(--shape), var(--shape-2)); }}
  .story .thumbs i.pdf {{ background: var(--card); border: 1px solid var(--line); position: relative; }}
  .story .thumbs i.pdf::after {{ content: ""; position: absolute; left: 18%; top: 38%; width: 64%; height: 24%; border: 2px solid var(--color-orange); border-radius: 50% 45% 55% 40%; }}
  .story .fields {{ display: grid; grid-template-columns: 1fr 1fr; gap: .6em; margin-top: 1em; }}
  .story .note {{ margin-top: .6em; }}

  /* scene 2: approvals board -> dashboard */
  .story .board {{ width: 84%; height: 88%; }}
  .story .board .cols {{ position: absolute; left: 1.2em; right: 1.2em; top: 4.4em; bottom: 1.2em; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1em; }}
  .story .board .col {{ background: var(--card); border-radius: .9em; padding: .9em; }}
  .story .board .col h4 {{ margin: 0 0 .8em; font-family: var(--font-mono); font-size: .78em; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 500; }}
  .story .board .ghost {{ height: 4.2em; border-radius: .7em; background: var(--shape); margin-bottom: .7em; opacity: .75; }}
  .story .mini {{ width: 29%; height: 15.5em; background: var(--color-paper); border: 1px solid var(--line); border-radius: .9em; padding: .9em 1em; box-shadow: 0 16px 34px -18px rgb(0 0 0 / .55); }}
  .story .mini .d {{ font-family: var(--font-mono); font-size: .75em; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }}
  .story .mini .t {{ font-weight: 600; font-size: 1.05em; margin-top: .25em; }}
  .story .mini .thumbs {{ margin-top: .6em; gap: .4em; grid-template-columns: repeat(3, 1fr); }}
  .story .mini .row {{ position: absolute; left: 1em; right: 1em; display: flex; justify-content: space-between; font-size: .95em; font-variant-numeric: tabular-nums; }}
  .story .mini .row span:last-child {{ color: var(--muted); }}
  .story .mini .total {{ position: absolute; left: 1em; right: 1em; bottom: .8em; border-top: 1px solid var(--line); padding-top: .5em; display: flex; justify-content: space-between; font-weight: 600; font-variant-numeric: tabular-nums; }}
  .story .mini .tag {{ position: absolute; right: .8em; top: .8em; }}
  .story .chip {{ position: absolute; background: var(--color-tar); color: var(--color-paper); border-radius: 999px; padding: .3em .7em; font-family: var(--font-mono); font-size: .72em; white-space: nowrap; box-shadow: 0 8px 20px -10px rgb(0 0 0 / .6); }}
  .story .tile {{ background: var(--color-paper); border: 1px solid var(--line); border-radius: 1em; padding: 1.1em 1.3em; box-shadow: var(--shadow); }}
  .story .tile h5 {{ margin: 0; font-family: var(--font-mono); font-size: .78em; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 500; }}
  .story .tile .big {{ font-weight: 700; font-size: 1.9em; letter-spacing: -.02em; margin-top: .25em; font-variant-numeric: tabular-nums; line-height: 1.1; }}
  .story .tile .big small {{ font-size: .5em; color: var(--muted); font-weight: 500; }}
  .story .tile .bar {{ position: absolute; left: 1.3em; right: 1.3em; bottom: 1.2em; height: .6em; background: var(--card); border-radius: .3em; }}
  .story .tile .bar i {{ position: absolute; left: 0; top: 0; bottom: 0; background: var(--accent); border-radius: .3em; }}
  .story .chart .bars {{ position: absolute; left: 1.3em; right: 1.3em; bottom: 3.4em; top: 4.4em; display: flex; align-items: flex-end; gap: .8em; border-bottom: 1px solid var(--line); }}
  .story .chart .bars i {{ position: relative; flex: 1; background: var(--shape); border-radius: .3em .3em 0 0; }}
  .story .chart .bars i.now {{ background: var(--accent); }}
  .story .chart .fc {{ position: absolute; left: 1.3em; right: 1.3em; bottom: 1em; display: flex; justify-content: space-between; gap: 1em; font-size: .9em; color: var(--muted); }}
  .story .chart .fc b {{ color: var(--color-tar); font-weight: 600; }}

  /* scene 3: approved updates -> invoice */
  .story .list {{ width: 34%; height: 84%; }} .story .inv {{ width: 52%; height: 84%; }}
  .story .urow {{ position: absolute; inset: 0; display: flex; align-items: center; gap: .7em; background: var(--card); border-radius: .7em; padding: 0 .9em; font-size: .92em; white-space: nowrap; overflow: hidden; }}
  .story .urow .cb {{ width: 1.05em; height: 1.05em; border-radius: .3em; background: var(--accent); flex: none; position: relative; }}
  .story .urow .cb::after {{ content: ""; position: absolute; left: .3em; top: .12em; width: .28em; height: .55em; border: solid var(--accent-ink); border-width: 0 2px 2px 0; transform: rotate(45deg); }}
  .story .urow b {{ margin-left: auto; font-weight: 600; font-variant-numeric: tabular-nums; }}
  .story .iline {{ position: absolute; inset: 0; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--line); font-size: .95em; font-variant-numeric: tabular-nums; white-space: nowrap; overflow: hidden; }}
  .story .iline b {{ font-weight: 600; }}
  .story .sum {{ display: flex; justify-content: space-between; align-items: center; font-size: .95em; font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--color-paper); }}
  .story .sum .k {{ font-size: .75em; color: var(--color-paper); opacity: .7; }}
  .story .sum.due {{ border-top: 2px solid var(--color-paper); font-weight: 700; font-size: 1.1em; }}
  .story .inv .sum, .story .inv .sum .k {{ color: var(--color-tar); }}
  .story .sub {{ position: absolute; inset: 0; }}
  .story .sub .doc {{ position: absolute; inset: 0; background: var(--color-paper); border: 1px solid var(--line); border-radius: .5em; box-shadow: var(--shadow); padding: .9em .9em; display: flex; flex-direction: column; gap: .35em; font-size: .95em; }}
  .story .sub .doc b {{ font-weight: 600; }}
  .story .sub .doc i {{ display: block; height: 2px; background: var(--shape); margin-top: .4em; }}
  .story .sub .match {{ position: absolute; inset: 0; display: flex; justify-content: space-between; align-items: center; gap: .8em; background: var(--card); border-radius: .7em; padding: 0 .9em; font-size: .92em; white-space: nowrap; overflow: hidden; }}
  .story .sub .match b {{ font-weight: 600; font-variant-numeric: tabular-nums; }}
  .story .stamp {{ background: var(--color-paper); }}

  @media (max-width: 900px) {{
    .story {{ margin-top: 72px; margin-bottom: 56px; }}
    .story .scene {{ height: 260vh; }}
    .story .pin {{ top: calc(64px + 12px); height: calc(100vh - 64px - 24px); gap: 12px; }}
    .story .head h3 {{ font-size: 18px; }}
    .story .stage {{ font-size: clamp(7px, 1.7cqw, 10px); aspect-ratio: 4 / 3; flex: none; width: 100%; height: auto; }}
    .story .pin {{ justify-content: flex-start; }}
    .story .caps {{ font-size: 14px; min-height: 3.4em; }}
  }}
</style>
'''
# fix: sums in bill scene sit on the invoice card (paper), so their text must be tar. Those are absolutely positioned over the stage, not inside .inv; use scene-scoped override.
astro = astro.replace('''  .story .sum {{ display: flex; justify-content: space-between; align-items: center; font-size: .95em; font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--color-paper); }}
  .story .sum .k {{ font-size: .75em; color: var(--color-paper); opacity: .7; }}
  .story .sum.due {{ border-top: 2px solid var(--color-paper); font-weight: 700; font-size: 1.1em; }}
  .story .inv .sum, .story .inv .sum .k {{ color: var(--color-tar); }}''',
'''  .story .sum {{ display: flex; justify-content: space-between; align-items: center; font-size: .95em; font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--color-tar); }}
  .story .sum .k {{ font-size: .75em; }}
  .story .sum.due {{ border-top: 2px solid var(--color-tar); font-weight: 700; font-size: 1.1em; }}''')
open(f"{ROOT}/src/components/ProductStory.astro","w").write(astro.replace('{{','{').replace('}}','}'))

config = "// Generated from reference/prototypes via /tmp/gen_story.py. Poses are % of the stage; `at` is scroll progress 0..1.\n"
config += "export const SCENES = " + json.dumps([{"id":sc["id"],"actors":sc["actors"],"capAt":sc["capAt"]} for sc in SCENES]) + ";\n"
open(f"{ROOT}/src/scripts/story.config.js","w").write(config)

engine = '''import { SCENES } from "./story.config.js";

// Scroll-scrubbed keyframe engine. Each scene is a tall section with a sticky stage; progress p (0..1)
// is how far the section has scrolled, and every actor's pose is interpolated from its keyframes.
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
  const caps = Array.from(sec.querySelectorAll(".cap"));
  let ticking = false;

  function render(p) {
    for (const a of actors) {
      if (!a.el) continue;
      apply(a.el, poseAt(a.kf, p));
      if (a.skin) { const k = smooth(p, a.skin[0], a.skin[1]); a.el.children[0].style.opacity = 1 - k; a.el.children[1].style.opacity = k; }
    }
    let c = 0; cfg.capAt.forEach((th, i) => { if (p >= th) c = i + 1; });
    caps.forEach((el, i) => el.classList.toggle("on", i === c));
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
'''
open(f"{ROOT}/src/scripts/story.js","w").write(engine)
print("generated", len(astro), "chars")
