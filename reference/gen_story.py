"""Generates src/components/ProductStory.astro, src/scripts/story.config.js and src/scripts/story.js.
Run: python3 reference/gen_story.py
Scenes come from the Figma frames "Start state" (6:67) and "End state" (6:56). Every product surface is coded
HTML/SVG (abstracted from the Clad screenshots) so it can animate; only the analog artifacts stay as images."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SX, SW = 118, 1204
SH = SW * 9 / 16
def P(x=None, y=None, w=None, h=None, y0=0, **k):
    """Figma px -> stage %. y0 is the Figma y where this scene's stage starts."""
    d = {}
    if x is not None: d["x"] = round((x - SX) / SW * 100, 2)
    if y is not None: d["y"] = round((y - y0) / SH * 100, 2)
    if w is not None: d["w"] = round(w / SW * 100, 2)
    if h is not None: d["h"] = round(h / SH * 100, 2)
    d.update(k); return d

def img(src, alt, frame="photo"):
    return f'<figure class="mock {frame}"><img src="/assets/story/{src}" alt="{alt}" /></figure>'

def rows_reveal(items, step):
    """items: list of html strings; each gets --i so it reveals as --draw passes i*step."""
    return "".join(h.replace('class="r"', f'class="r" style="--i:{i}"', 1) for i, h in enumerate(items))

# =====================================================================================
# CAPTURE
# =====================================================================================
Y1 = 330

SPREADSHEET = (
  '<div class="ui sheet">'
  '<div class="sh1">CONCRETE VOLUME &amp; COST CALCULATOR</div>'
  '<div class="sh2">Slabs · Footings · Walls · Columns · Piers - volume, waste, trucks, bags, and cost</div>'
  '<div class="sh3">PROJECT INPUTS</div>'
  + "".join(f'<div class="kv"><span>{k}</span><b>{v}</b><span></span></div>' for k, v in
            [("Project Name","Riverside Medical - 2026-118"),("Waste / Over-Order Allowance","10%"),("Concrete Price per Cubic Yard","$168.00"),("Truck Capacity (cubic yards)","10")])
  + '<div class="sh3">POURS</div>'
  '<div class="th"><span>#</span><span>Description</span><span>Shape</span><span>Length (ft)</span><span>Width (ft)</span><span>Qty</span><span>Volume (cu yd)</span></div>'
  + "".join(f'<div class="tr"><span>{n}</span><span>{d}</span><span>{s}</span><span>{l}</span><span>{w}</span><span>{q}</span><span>{v}</span></div>' for n,d,s,l,w,q,v in
            [(1,"Level 1 slab on grade - east bay","Slab","120.00","60.00",1,"133.33"),(2,"Level 1 slab on grade - west bay","Slab","96.00","48.00",1,"85.33"),
             (3,"Perimeter strip footing","Footing","380.00","2.00",1,"28.15"),(4,"Interior spread footings 5' x 5'","Footing","5.00","5.00",12,"22.22"),(5,"Foundation wall - north","Wall","120.00","8.00",1,"29.63")])
  + '</div>')

# abstract aerial map + tool rail + quantity panel; the yellow bore path draws with --draw, quantity counts with v
MAP = (
  '<div class="ui map">'
  '<svg class="terrain" viewBox="0 0 600 400" preserveAspectRatio="none" aria-hidden="true">'
  '<rect width="600" height="400" fill="#8a9a63"/>'
  '<path d="M0 0h600v400H0z" fill="url(#g1)"/>'
  '<defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a9b477"/><stop offset=".5" stop-color="#7f9257"/><stop offset="1" stop-color="#b3a874"/></linearGradient></defs>'
  '<ellipse cx="200" cy="120" rx="140" ry="90" fill="#4e6a3a" opacity=".85"/><ellipse cx="300" cy="190" rx="90" ry="60" fill="#5c7a44" opacity=".8"/>'
  '<ellipse cx="480" cy="330" rx="130" ry="70" fill="#6a8a48" opacity=".7"/><ellipse cx="120" cy="330" rx="110" ry="50" fill="#c2b27a" opacity=".6"/>'
  '<path class="road" d="M90 0v400M0 395h600M90 60h510M420 0v180"/>'
  '<g class="lots" fill="#d9d2b8" opacity=".85">' + "".join(f'<rect x="{x}" y="{y}" width="16" height="12" rx="2"/>' for x, y in [(440,240),(470,232),(500,244),(530,236),(560,250),(450,280),(485,290),(520,282),(555,300),(440,320),(475,330),(510,322)]) + '</g>'
  '<polyline class="bore" pathLength="1" points="88,10 88,240 240,240 300,222"/>'
  '</svg>'
  '<div class="rail"><i class="t-search"></i><i class="t-rect"></i><i class="t-arrow on"></i><i class="t-text">T</i><i class="t-circle"></i></div>'
  '<div class="qpanel">'
  '<div class="qhd"><i class="arrow"></i><div><b>U-BOR04-18</b><span>Boring - 1.25”</span></div></div>'
  '<div class="qrow"><span>Quantity</span><em><span data-count="int">0</span></em><small>FT</small></div>'
  '<div class="qrow"><span>Sequential In</span><em class="wide">ABC-12839</em></div>'
  '<div class="qrow"><span class="ph"></span><em class="wide ph"></em></div>'
  '</div></div>')

PROD_ROWS = [
  ("D01","Aerial Drop",True,"-","0","0","LF"),("D02","Mount NID at service address",False,"80","42","0","EA"),
  ("D03","UG pull fiber drop from Terminal to Flowerpot",False,"2,300","900","0","LF"),("D04","Bury Drop Tail 12\" depth from flowerpot to NID",False,"1,230","582","0","LF"),
  ("D06","Mount NID at service address",True,"-","0","0","EA"),("D07","UG pull fiber drop from Terminal to Flowerpot",True,"-","0","0","LF"),
]
GEO_ROWS = [("GT-CON01","1.25\" Conduit (1)",False,"6,420","737",None,"LF"),("GT-CON02","1.25\" Conduit (2)",False,"6,420","400","0","LF"),("GT-FFP01","FP - 10\" Round",False,"80","2","0","EA")]
def prow(code, name, nb, bud, prog, new, unit):
    newcell = '<span class="inp"><span data-count="int">0</span></span>' if new is None else f'<span class="inp">{new}</span>'
    return f'<div class="r{" hi" if new is None else ""}"><span class="code">{code}</span><span class="name">{name}</span><span class="nb">{"Not Budgeted" if nb else ""}</span><span>{bud}</span><span>{prog}</span>{newcell}<span class="unit">{unit}</span></div>'
PRODUCTION = (
  '<div class="ui prod">'
  '<div class="phd"><b>Production</b><span class="btn2">Upload</span></div>'
  '<div class="gh"><span>Drop</span><span></span><span></span><span>Budgeted</span><span>Progress to Date</span><span>New Quantity</span><span></span></div>'
  + rows_reveal([prow(*r) for r in PROD_ROWS], .08)
  + '<div class="gh"><span>Geotech</span><span></span><span></span><span>Budgeted</span><span>Progress to Date</span><span>New Quantity</span><span></span></div>'
  + "".join(h.replace('class="r', f'style="--i:{6+i}" class="r', 1) for i, h in enumerate(prow(*r) for r in GEO_ROWS))
  + '</div>')

capture = {
  "id": "capture", "name": "Capture", "title": "Record everything you need from the field in a single place",
  "html": (
    f'<div class="act skin" data-a="sketch">{img("capture-sketch.png","Handwritten field sketch on paper")}<div class="mock app">{MAP}</div></div>'
    f'<div class="act skin" data-a="sheet"><div class="mock photo">{SPREADSHEET}</div><div class="mock app">{PRODUCTION}</div></div>'
    f'<div class="act" data-a="gmail"><div class="gmail">{img("capture-gmail.png","Gmail","icon")}<span class="badge">8,201</span></div></div>'
  ),
  "actors": [
    {"id": "sketch", "kf": [P(367, 344, 366, 244, Y1, at=.0, r=-2.5, d=0, v=0), P(367, 344, 366, 244, Y1, at=.18, r=-2.5, d=0, v=0), P(136, 417, 493.5, 329, Y1, at=.6, r=0, d=0, v=0), P(136, 417, 493.5, 329, Y1, at=.9, r=0, d=1, v=868)], "skin": [.34, .54]},
    {"id": "sheet",  "kf": [P(623, 523, 483, 193, Y1, at=.0, r=5, d=0, v=0), P(623, 523, 483, 193, Y1, at=.22, r=5, d=0, v=0), P(677, 405, 631, 350, Y1, at=.64, r=0, d=0, v=0), P(677, 405, 631, 350, Y1, at=.92, r=0, d=1, v=138)], "skin": [.4, .58]},
    {"id": "gmail",  "kf": [P(783, 344, 87, 87, Y1, at=.0, o=1, s=1), P(783, 344, 87, 87, Y1, at=.2, o=1, s=1), P(783, 300, 87, 87, Y1, at=.4, o=0, s=.85)]},
  ],
}

# =====================================================================================
# MANAGE
# =====================================================================================
Y2 = 1158
TAG = {"aerial":("Aerial","#e5484d"),"au":("Aerial & Underground","#3b82f6"),"ug":("Underground","#6b6b6b"),
       "att":("AT&T","#9b5de5"),"tx":("Texas","#f0782a"),"sa":("San Antonio","#f0782a"),"demo":("Demo","#e5484d")}
def tags(*keys): return '<div class="tags">'+"".join(f'<span class="tag" style="--c:{TAG[k][1]}">{TAG[k][0]}</span>' for k in keys)+'</div>' if keys else ''
def card(title, who, date=None, pct=None, *tg, count=False):
    meta = ""
    if date or pct is not None:
        n = f'<span data-count="pct">0%</span>' if count else f'{pct}%'
        meta = '<div class="meta">' + (f'<span class="date">{date}</span>' if date else '<span></span>') + (f'<span class="pct"><i class="ring" style="--v:{pct}"></i>{n}</span>' if pct is not None else '') + '</div>'
    return f'<div class="bcard"><div class="row"><span class="title">{title}</span><span class="who">{who}</span></div>{tags(*tg)}{meta}</div>'
def column(name, count, color, cards):
    return f'<div class="col"><div class="colhd"><i style="background:{color}"></i>{name}<span>{count}</span></div><div class="slot"></div>' + "".join(cards) + '</div>'
BOARD_HTML = (
  '<div class="board">'
  '<div class="toolbar"><span class="proj">All Projects <i class="chev"></i></span><span class="search">Search</span><span class="filter">Filter</span><span class="ico"></span></div>'
  '<div class="cols">'
  + column("Not Started", 188, "#8a8a8a", [card("14280 Oldia Ave","WD","Jul 31, 2026",0), card("25 Court St","JD",None,94,"aerial","au"), card("26 Saddleback Ridge Dr.","WD","Mar 21, 2026")])
  + column("Permitting", 13, "#3bb7e6", [card("123 Main St Project","WD",None,0), card("1378 El Sereno","MR",None,0,"ug"), card("1378 El Sereno","WD",None,0,"ug")])
  + column("Make Ready", 16, "#f0782a", [card("26 Saddleback Ridge Dr.","WD","Mar 21, 2026"), card("Campsite integration","JD",None,0,"att","tx"), card("Clean Test Nov 18","de","Dec 11, 2024",0,"sa","tx")])
  + '</div>'
  + '<div class="act hero" data-a="hero">' + card("10428 India Ave","WD","Aug 31, 2026",0,"demo","tx",count=True) + '</div>'
  '</div>')

SERIES = [("#4750ff",[28,35,52,55,45,47]),("#3cb043",[47,30,47,46,44,53]),("#e5533c",[48,55,58,50,43,22]),("#e64ca7",[0,0,0,12,28,45]),("#f2c230",[5,17,10,24,18,6])]
PW, PH, YMAX = 600, 260, 60
def pt(i, v): return (round(i * PW / 5, 1), round(PH - v / YMAX * PH, 1))
svg = "".join(f'<line class="grid" x1="0" y1="{round(PH - i*10/YMAX*PH,1)}" x2="{PW}" y2="{round(PH - i*10/YMAX*PH,1)}"/>' for i in range(7))
for color, vals in SERIES:
    pts = [pt(i, v) for i, v in enumerate(vals)]
    svg += f'<polyline class="line" pathLength="1" points="{" ".join(f"{x},{y}" for x,y in pts)}" style="stroke:{color}"/>'
    for i, (x, y) in enumerate(pts):
        svg += f'<line class="dot bg" x1="{x}" y1="{y}" x2="{x}" y2="{y}" style="--i:{i}"/><line class="dot" x1="{x}" y1="{y}" x2="{x}" y2="{y}" style="stroke:{color};--i:{i}"/>'
CHART_HTML = (
  '<div class="report"><div class="rhd">Projects <span>/</span> Insights <span>/</span> Weekly Production Report <i class="chev"></i></div>'
  '<div class="plot"><div class="ylab">' + "".join(f'<span>${v}k</span>' for v in range(60, -1, -10)) + '</div>'
  f'<svg viewBox="0 0 {PW} {PH}" preserveAspectRatio="none" aria-hidden="true">{svg}</svg>'
  '<div class="xlab">' + "".join(f'<span>{d}</span>' for d in ["Mar 2","Mar 9","Mar 16","Mar 23","Mar 30","Apr 6"]) + '</div></div></div>')

manage = {
  "id": "manage", "name": "Manage", "title": "Connect the dots on all the projects you manage",
  "html": (
    f'<div class="act" data-a="kanban">{BOARD_HTML}</div>'
    f'<div class="act" data-a="chart" role="img" aria-label="Weekly production report: five projects, March 2 to April 6">{CHART_HTML}</div>'
  ),
  "actors": [
    {"id": "kanban", "kf": [P(300, 1170, 841, 386, Y2, at=.0, s=1), P(300, 1170, 841, 386, Y2, at=.25, s=1), P(192, 1170, 841, 386, Y2, at=.62, s=round(408/841, 3))]},
    {"id": "chart",  "kf": [P(667, 1220, 643, 429, Y2, at=.0, o=0, d=0), P(667, 1220, 643, 429, Y2, at=.42, o=0, d=0), P(667, 1167, 643, 429, Y2, at=.62, o=1, d=0), P(667, 1167, 643, 429, Y2, at=.92, o=1, d=1)]},
    # three columns: lefts 1.2 / 34.2 / 67.1 (% of board); rests below the column headers, dips while travelling
    {"id": "hero",   "kf": [{"at":.0,"x":1.2,"y":23,"v":0},{"at":.08,"x":1.2,"y":23,"v":0},{"at":.16,"x":17.7,"y":34,"v":10},{"at":.24,"x":34.2,"y":23,"v":20},{"at":.36,"x":34.2,"y":23,"v":20},{"at":.45,"x":50.6,"y":34,"v":31},{"at":.54,"x":67.1,"y":23,"v":41}]},
  ],
}

# =====================================================================================
# BILL
# =====================================================================================
Y3 = 1968
LINES = [("D02","Mount NID at service address",24,"$12.12","$290.88"),("D03","UG pull fiber drop from Terminal to Flowerpot",180,"$8.50","$1,530.00"),
         ("D04","Bury Drop Tail 12\" depth from flowerpot to NID",322,"$9.60","$3,091.20"),("GT-CON01","1.25\" Conduit (1)",271,"$8.12","$2,200.52"),
         ("GT-CON02","1.25\" Conduit (2)",400,"$8.12","$3,248.00"),("GT-FFP01","FP - 10\" Round",2,"$25.00","$50.00")]
ITEMS = (
  '<div class="ui items"><div class="ihd">Items</div>'
  '<div class="ith"><span>Line Item</span><span>Qty</span><span>Rate</span><span>Amount</span></div>'
  + "".join(f'<div class="ir"><span><em>{c}</em> {n}</span><span class="q">{q}</span><span class="rate">{r}</span><span class="amt">{a}</span></div>' for c,n,q,r,a in LINES)
  + '<div class="isum"><span>Subtotal</span><span>$10,410.60</span></div><div class="isum adj"><span></span><span>+ Adjustment</span></div><div class="isum tot"><span>Total</span><span>$10,410.60</span></div>'
  '<div class="ift"><i class="trash"></i><span class="btn2">Back</span><span class="btn2 primary">Create</span></div></div>')
INVOICE = (
  '<div class="ui invoice">'
  '<div class="vhd"><b>Invoice</b><span class="logo">ACME</span></div>'
  '<div class="vmeta"><div><span>Invoice #</span><b>487</b></div><div><span>Invoice date</span><b>September 1, 2026</b></div><div><span>Date due</span><b>October 1, 2026</b></div></div>'
  '<div class="vaddr"><div><b>Acme Inc.</b>123 William Street<br>New York, New York 10038<br>United States</div><div><b>Bill to</b>Big TelCo<br>102 3rd Avenue<br>New York, New York 10003<br>United States</div></div>'
  '<div class="vdue"><span data-count="money">$0.00</span> USD due October 1, 2026</div>'
  '<div class="vproj"><b>Project:</b> Suffolk, VA - Z1.4<br><b>Work Dates:</b> 06/17/26, 06/22/26</div>'
  '<div class="vth"><span>Description</span><span>Qty</span><span>Rate</span><span>Amount</span></div>'
  + rows_reveal([f'<div class="r"><span>{c} {n}</span><span>{q}</span><span>{r}</span><span>{a}</span></div>' for c,n,q,r,a in LINES], .12)
  + '<div class="vtot"><span>Amount due (USD)</span><b data-count="money">$0.00</b></div></div>')

bill = {
  "id": "bill", "name": "Bill", "title": "Generate accurate invoices and eliminate over- or under-billing",
  "html": (
    f'<div class="act" data-a="items"><div class="mock app">{ITEMS}</div></div>'
    f'<div class="act" data-a="invoice"><div class="mock photo">{INVOICE}</div></div>'
  ),
  "actors": [
    {"id": "items",   "kf": [P(330, 1990, 560, 440, Y3, at=.0, o=1), P(330, 1990, 560, 440, Y3, at=.26, o=1), P(136, 2030, 540, 425, Y3, at=.55, o=.8)]},
    {"id": "invoice", "kf": [P(790, 2000, 512, 540, Y3, at=.0, o=0, d=0, v=0), P(790, 2000, 512, 540, Y3, at=.3, o=0, d=0, v=0), P(740, 1962, 512, 540, Y3, at=.56, o=1, d=0, v=0), P(740, 1962, 512, 540, Y3, at=.92, o=1, d=1, v=10410.60)]},
  ],
}

SCENES = [capture, manage, bill]

scenes_html = ""
for sc in SCENES:
    scenes_html += f'''
  <section class="scene" id="story-{sc["id"]}" data-scene="{sc["id"]}">
    <div class="pin">
      <div class="head"><span class="label">{sc["name"]}</span><h3>{sc["title"]}</h3></div>
      <div class="stage">{sc["html"]}</div>
    </div>
  </section>'''

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "story.css")).read()
astro = f'''---
/* Product story: three scroll-scrubbed scenes (Capture, Manage, Bill). GENERATED by reference/gen_story.py;
   styles in reference/story.css. Edit those, not this file. */
---
<div class="story container-wide" id="story" aria-label="How Clad works">{scenes_html}
</div>

<script src="../scripts/story.js"></script>

<style is:global>
{CSS}
</style>
'''
open(f"{ROOT}/src/components/ProductStory.astro", "w").write(astro)

config = "// Generated by reference/gen_story.py. Poses are % of the stage (or of the parent for nested actors); `at` is scroll progress 0..1.\n"
config += "export const SCENES = " + json.dumps([{"id": sc["id"], "actors": sc["actors"]} for sc in SCENES]) + ";\n"
open(f"{ROOT}/src/scripts/story.config.js", "w").write(config)

engine = r'''import { SCENES } from "./story.config.js";

// Scroll-scrubbed keyframe engine. Each scene is a tall section with a sticky stage; progress p (0..1)
// is how far the section has scrolled, and every actor's pose is interpolated from its keyframes.
// Pose keys: x y w h (%), r (deg), s (scale), o (opacity), d (draw 0..1 -> --draw), v (value -> [data-count] text).
// An actor with a `skin` range crossfades its first child into its second across that range.
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const smooth = (p, a, b) => { const t = clamp((p - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const UNITS = { x: "left", y: "top", w: "width", h: "height" };
const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
const fmt = (v, kind) => kind === "pct" ? Math.round(v) + "%" : kind === "money" ? money.format(v) : Math.round(v).toLocaleString("en-US");

function apply(el, pose) {
  for (const k in UNITS) if (pose[k] != null) el.style[UNITS[k]] = pose[k] + "%";
  if (pose.o != null) el.style.opacity = pose.o;
  if (pose.d != null) el.style.setProperty("--draw", pose.d);
  if (pose.v != null) { el.style.setProperty("--v", pose.v); el.querySelectorAll("[data-count]").forEach((t) => { t.textContent = fmt(pose.v, t.dataset.count); }); }
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
'''
open(f"{ROOT}/src/scripts/story.js", "w").write(engine)
print("generated")
