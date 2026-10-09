"""Generates src/components/ProductStory.astro, src/scripts/story.config.js and src/scripts/story.js.
Run: python3 reference/gen_story.py
Styles live in reference/story.css.

Layout: each scene pins a two-column frame centered in the viewport. Left: label, headline, subhead and three
stacked features. Right: a stage where the product UI animates. Scroll progress p (0..1) is split into three
steps; step i highlights feature i and plays its part of the animation, one thing at a time.

Actors are positioned by their CENTER in % of the stage (x, y), width w in % of the stage, and scale s.
Copy follows Jason's "Q3 2026 Marketing Site Content - Homepage" doc."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [0, .36, .69]  # where features 2 and 3 take over


def kf(at, **k):
    d = {"at": at}
    d.update(k)
    return d


def avatar(name):
    company = any(t in name for t in ("Underground", "Boring", "Civil", "Fiber"))
    ini = "".join(w[0] for w in name.replace(".", "").split()[:2]).upper()
    return f'<span class="who {"co" if company else "person"}"><i>{ini}</i>{name}</span>'


# =====================================================================================
# 1. BILLING: daily updates -> invoice built from them -> synced to QuickBooks
# =====================================================================================
UPDATES = [  # date, code, item, qty, completed by, attachments
    ("Mon Sep 14", "D02", "Mount NID at service address", "24 EA", "D. Alvarez", ["IMG", "IMG"]),
    ("Tue Sep 15", "D03", "UG pull fiber drop", "180 LF", "Ortiz Underground", ["PDF"]),
    ("Wed Sep 16", "GT-CON01", "1.25” Conduit", "271 LF", "Bell Boring", ["IMG"]),
]
INVOICE_LINES = [  # code, item, qty, amount (qty x contract rate)
    ("D02", "Mount NID at service address", "24", "$290.88"),
    ("D03", "UG pull fiber drop", "180", "$1,530.00"),
    ("GT-CON01", "1.25” Conduit", "271", "$2,200.52"),
]
INVOICE_TOTAL = 4021.40

UPDATES_HTML = (
    '<div class="card updates"><div class="chd"><b>Daily updates</b><span>Maple Run · Week of Sep 14</span></div>'
    + "".join(
        f'<div class="row" style="--i:{i}"><div class="l1"><span class="item"><em>{c}</em> {n}</span><span class="qty">{q}</span></div>'
        f'<div class="l2"><span class="date">{d}</span>{avatar(by)}<span class="att">{"".join(f"<i>{a}</i>" for a in att)}</span></div></div>'
        for i, (d, c, n, q, by, att) in enumerate(UPDATES))
    + '</div>')

INVOICE_HTML = (
    '<div class="card invoice">'
    '<div class="vhd"><div><b>Invoice #487</b><span>Big TelCo · Suffolk, VA - Z1.4</span></div><span class="logo">ACME</span></div>'
    '<div class="vdue"><span data-count="money">$0.00</span><small>due Oct 1, 2026</small></div>'
    '<div class="vth"><span>Description</span><span>Qty</span><span>Amount</span></div>'
    + "".join(
        f'<div class="row" style="--i:{i}"><span class="item"><em>{c}</em> {n}<small>Linked to {UPDATES[i][0]} update</small></span><span>{q}</span><span>{a}</span></div>'
        for i, (c, n, q, a) in enumerate(INVOICE_LINES))
    + '<div class="vtot"><span>Amount due</span><b data-count="money">$0.00</b></div></div>')

QB_HTML = (
    '<div class="qbchip"><span class="qbi" aria-hidden="true">qb</span>'
    '<span class="txt"><b>Synced to QuickBooks</b><small>Invoice #487 · just now</small></span>'
    '<span class="ok" aria-hidden="true"></span></div>')

billing = {
    "id": "billing", "name": "Billing", "title": "Bill accurately",
    "sub": "One system to prevent over- and under-billing",
    "feats": [
        ("Production tracking", "Collect daily production and documentation from the field"),
        ("Linked invoices & bills", "Tie your invoices and bills directly to approved production, so you only bill for work that’s done"),
        ("QBO integration", "Sync invoices with QuickBooks to speed up AR accounting and track retainage"),
    ],
    "html": (
        f'<div class="act" data-a="updates">{UPDATES_HTML}</div>'
        f'<div class="act" data-a="invoice">{INVOICE_HTML}</div>'
        f'<div class="act" data-a="qb">{QB_HTML}</div>'
    ),
    "actors": [
        # step 1: updates arrive one by one, centered
        {"id": "updates", "kf": [
            kf(0, x=50, y=46, w=78, s=1, o=1, d=0), kf(.04, x=50, y=46, w=78, s=1, o=1, d=0),
            kf(.28, x=50, y=46, w=78, s=1, o=1, d=1), kf(.36, x=50, y=46, w=78, s=1, o=1, d=1),
            kf(.48, x=50, y=20, w=78, s=.86, o=.45, d=1)]},
        # step 2: the invoice comes forward and fills from those updates
        {"id": "invoice", "kf": [
            kf(0, x=50, y=60, w=72, s=.96, o=0, d=0, v=0), kf(.38, x=50, y=60, w=72, s=.96, o=0, d=0, v=0),
            kf(.5, x=50, y=53, w=72, s=1, o=1, d=0, v=0), kf(.65, x=50, y=53, w=72, s=1, o=1, d=1, v=INVOICE_TOTAL),
            kf(1, x=50, y=53, w=72, s=1, o=1, d=1, v=INVOICE_TOTAL)]},
        # step 3: a single sync chip lands on the invoice
        {"id": "qb", "kf": [
            kf(0, x=50, y=94, w=50, s=.7, o=0, d=0), kf(.71, x=50, y=94, w=50, s=.7, o=0, d=0),
            kf(.8, x=50, y=92.5, w=50, s=1, o=1, d=0), kf(.9, x=50, y=92.5, w=50, s=1, o=1, d=1),
            kf(1, x=50, y=92.5, w=50, s=1, o=1, d=1)]},
    ],
}

# =====================================================================================
# 2. PROJECT MANAGEMENT: minimal blueprint -> redlines + labels -> report -> forecast
# =====================================================================================
# Blueprint traced from Jocelyn's start/end frames (reference/figma/blueprint-start.png, -end.png). The basemap
# is the start frame with its markup removed (reference/figma/blueprint-clean.py), traced to vector with potrace
# into reference/figma/blueprint-map.svg. Coordinates below are in that 547 x 456 frame.
import re
_map = open(os.path.join(HERE, "figma", "blueprint-map.svg")).read()
MAP_G = re.search(r"(<g transform=.*?</g>)", _map, re.S).group(1).replace('fill="#000000"', 'class="basemap"')
BP_LINE = "98,305 414,354.5 462,178"
BP_SQUARES = [(251, 73, 31), (450, 161, 32)]  # x, y, size (stroke centerline)
BP_CIRCLE = (98, 305, 16)
BP_LABELS = [  # box x, y, w, text; cascade order follows the line, the standalone square last
    (62, 340, 78, "BDO3-01"),
    (233, 365, 142, "BM60(1)(1.25)-01"),
    (420, 214, 93, "UG-104-02"),
    (220, 122, 93, "UG-104-03"),
]


def bp_label(i, x, y, w, text):
    return (f'<g class="lbl" style="--i:{i}"><rect class="lbox" x="{x}" y="{y}" width="{w}" height="28"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 19}" text-anchor="middle">{text}</text></g>')


def bp_marks(cls):
    sq = "".join(f'<rect class="{cls} sq" x="{x}" y="{y}" width="{n}" height="{n}"/>' for x, y, n in BP_SQUARES)
    cx, cy, r = BP_CIRCLE
    return f'{sq}<circle class="{cls} ci" cx="{cx}" cy="{cy}" r="{r}"/>'


BLUEPRINT_SVG = (
    '<svg class="bpsvg" viewBox="0 0 547 456" aria-hidden="true">'
    '<rect width="547" height="456" fill="#fff"/>'
    + MAP_G
    # the black markup from the start frame, covered stroke by stroke as the red redline draws over it
    + f'<g class="ink"><polyline points="{BP_LINE}"/>{bp_marks("k")}</g>'
    + f'<g class="red"><polyline class="redline" pathLength="1" points="{BP_LINE}"/>{bp_marks("r")}</g>'
    + "".join(bp_label(i, *l) for i, l in enumerate(BP_LABELS))
    + '</svg>')

BLUEPRINT_HTML = (
    '<div class="card blueprint"><div class="chd"><b>As-built</b><span>Suffolk, VA · Zone 1.4 · Sheet 3 of 12</span>'
    '<em class="live">Live</em></div>' + BLUEPRINT_SVG + '</div>')

# weekly production report: three series, then a dashed two-week forecast
SERIES = [("#3cb043", [47, 30, 47, 46, 44, 53]), ("#e5533c", [48, 55, 58, 50, 43, 22]), ("#f2c230", [5, 17, 10, 24, 18, 6])]
FORECAST = {"#3cb043": [53, 55, 58], "#e5533c": [22, 27, 31], "#f2c230": [6, 11, 15]}
PW, PH, YMAX, FW = 600, 260, 60, 240


def pt(i, v):
    return (round(i * PW / 5, 1), round(PH - v / YMAX * PH, 1))


chart_svg = "".join(
    f'<line class="grid" x1="0" y1="{round(PH - i * 10 / YMAX * PH, 1)}" x2="{PW + FW}" y2="{round(PH - i * 10 / YMAX * PH, 1)}"/>'
    for i in range(7))
chart_svg += f'<rect class="fzone" x="{PW}" y="0" width="{FW}" height="{PH}"/><line class="today" x1="{PW}" y1="0" x2="{PW}" y2="{PH}"/>'
for color, vals in SERIES:
    pts = [pt(i, v) for i, v in enumerate(vals)]
    chart_svg += f'<polyline class="line" pathLength="1" points="{" ".join(f"{x},{y}" for x, y in pts)}" style="stroke:{color}"/>'
    for i, (x, y) in enumerate(pts):
        chart_svg += (f'<line class="dot bg" x1="{x}" y1="{y}" x2="{x}" y2="{y}" style="--i:{i}"/>'
                      f'<line class="dot" x1="{x}" y1="{y}" x2="{x}" y2="{y}" style="stroke:{color};--i:{i}"/>')
chart_svg += '<g class="fcast">'
for color, fv in FORECAST.items():
    fp = [pt(5 + i, v) for i, v in enumerate(fv)]
    chart_svg += f'<polyline class="fline" points="{" ".join(f"{x},{y}" for x, y in fp)}" style="stroke:{color}"/>'
chart_svg += '</g>'

CHART_HTML = (
    '<div class="card report" role="img" aria-label="Weekly production report with a two-week forecast">'
    '<div class="chd"><b>Weekly Production Report</b><span>All projects</span><em class="flab">Forecast</em></div>'
    '<div class="plot"><div class="ylab">' + "".join(f'<span>${v}k</span>' for v in range(60, -1, -20)) + '</div>'
    f'<svg viewBox="0 0 {PW + FW} {PH}" preserveAspectRatio="none" aria-hidden="true">{chart_svg}</svg>'
    '<div class="xlab">' + "".join(f'<span>{d}</span>' for d in ["Mar 2", "Mar 16", "Mar 30"]) + '<span class="fx">Apr 20</span></div></div></div>')

pm = {
    "id": "pm", "name": "Project Management", "title": "Stay on top of every project",
    "sub": "Live progress, as-builts, and forecasts across all of your projects",
    "feats": [
        ("Digital as-builts", "Build GIS or PDF as-builts in real-time to visualize your construction progress"),
        ("Reporting", "Build and share custom reports"),
        ("Forecasting", "See where projects are headed ahead of time"),
    ],
    "html": (
        f'<div class="act" data-a="blueprint">{BLUEPRINT_HTML}</div>'
        f'<div class="act" data-a="chart">{CHART_HTML}</div>'
    ),
    "actors": [
        # step 1: blank blueprint, then the redline draws and its labels cascade in
        {"id": "blueprint", "kf": [
            kf(0, x=50, y=50, w=74, s=1, o=1, d=0), kf(.05, x=50, y=50, w=74, s=1, o=1, d=0),
            kf(.21, x=50, y=50, w=74, s=1, o=1, d=1), kf(.32, x=50, y=50, w=74, s=1, o=1, d=1.8),
            kf(.36, x=50, y=50, w=74, s=1, o=1, d=1.8), kf(.48, x=50, y=26, s=.72, w=74, o=.45, d=1.8)]},
        # step 2: the report comes forward and draws; step 3: the forecast extends it
        {"id": "chart", "kf": [
            kf(0, x=50, y=66, w=84, s=.96, o=0, d=0), kf(.38, x=50, y=66, w=84, s=.96, o=0, d=0),
            kf(.5, x=50, y=60, w=84, s=1, o=1, d=0), kf(.65, x=50, y=60, w=84, s=1, o=1, d=1),
            kf(.72, x=50, y=60, w=84, s=1, o=1, d=1), kf(.9, x=50, y=60, w=84, s=1, o=1, d=1.4),
            kf(1, x=50, y=60, w=84, s=1, o=1, d=1.4)]},
    ],
}

# =====================================================================================
# 3. LOCATES: AI-drafted ticket -> your tickets clear and renew -> subcontractor tickets
# =====================================================================================
FIELDS = [("Address", "1420 Maple Run Rd, Suffolk, VA"), ("Work type", "Directional boring · 1.25” conduit"), ("Dig start", "Mon, Sep 28")]
FORM_HTML = (
    '<div class="card aiform"><div class="ahd"><i class="spark" aria-hidden="true"></i><b>New locate ticket</b><span>Drafted by Clad AI from your work order</span></div>'
    + "".join(f'<div class="fld" style="--i:{i}"><span>{k}</span><em><span class="type">{v}</span></em></div>' for i, (k, v) in enumerate(FIELDS))
    + '<div class="cta"><span class="btn2 primary submit">Submit to 811</span><span class="sent"><i></i>Submitted · Ticket 2609-2211-04</span></div></div>')

MINE = [  # address, ticket, (status before, after), expires
    ("1420 Maple Run Rd", "2609-2211-04", ("Submitted", "Cleared"), "Oct 12"),
    ("Hwy 9 & Mill Rd", "2609-2208-02", ("Expires Fri", "Renewed"), "Oct 24"),
    ("71 Riverside Dr", "2609-2207-11", ("Pending", "Cleared"), "Oct 3"),
]
SUBS = [  # address, ticket, company, status, expires
    ("388 Cedar Loop", "2609-2210-17", "Ortiz Underground", "Cleared", "Oct 9"),
    ("902 Main St", "2609-2205-06", "Kline Civil", "Pending", "Oct 1"),
    ("14 Harbor Way", "2609-2212-09", "Bell Boring", "Submitted", "Oct 15"),
]


def pill(t, extra=""):
    cls = "ok" if t in ("Cleared", "Renewed") else "warn" if t.startswith("Expires") or t == "Pending" else "info"
    return f'<em class="spill {cls} {extra}">{t}</em>'


TICKETS_HTML = (
    '<div class="card tickets"><div class="chd"><b>Locate tickets</b><span class="filter"><em class="fa">Acme Fiber</em><em class="fb">All subcontractors</em></span></div>'
    '<div class="lth"><span>Ticket</span><span>Company</span><span>Status</span><span>Expires</span></div>'
    '<div class="rows"><div class="grp a">'
    + "".join(f'<div class="row" style="--j:{j}"><span class="tk"><b>{ad}</b><small>{t}</small></span>{avatar("Acme Fiber")}'
              f'<span class="st">{pill(a, "a")}{pill(b, "b")}</span><span class="ex">{ex}</span></div>'
              for j, (ad, t, (a, b), ex) in enumerate(MINE))
    + '</div><div class="grp b">'
    + "".join(f'<div class="row" style="--i:{i}"><span class="tk"><b>{ad}</b><small>{t}</small></span>{avatar(co)}'
              f'<span class="st">{pill(stt)}</span><span class="ex">{ex}</span></div>'
              for i, (ad, t, co, stt, ex) in enumerate(SUBS))
    + '</div></div></div>')

locates = {
    "id": "locates", "name": "Locates", "title": "Automate your 811 tickets",
    "sub": "AI 811 ticket management to submit and track your locate requests", "link": ("Learn more", "#locates"),
    "feats": [
        ("AI ticket submission", "Use AI to create and submit 811 tickets in bulk"),
        ("Automated tracking and renewals", "Visualize ticket status and keep tickets updated from a single dashboard"),
        ("Subcontractor visibility", "Monitor your subcontractors’ 811 tickets"),
    ],
    "html": (
        f'<div class="act" data-a="form">{FORM_HTML}</div>'
        f'<div class="act" data-a="tickets">{TICKETS_HTML}</div>'
    ),
    "actors": [
        # step 1: the form types itself out and submits
        {"id": "form", "kf": [
            kf(0, x=50, y=46, w=68, s=1, o=1, d=0), kf(.04, x=50, y=46, w=68, s=1, o=1, d=0),
            kf(.24, x=50, y=46, w=68, s=1, o=1, d=1), kf(.3, x=50, y=46, w=68, s=1, o=1, d=1.3),
            kf(.36, x=50, y=46, w=68, s=1, o=1, d=1.3), kf(.48, x=50, y=20, w=68, s=.84, o=.45, d=1.3)]},
        # step 2: your tickets clear and renew; step 3: the view switches to subcontractor tickets
        {"id": "tickets", "kf": [
            kf(0, x=50, y=66, w=90, s=.96, o=0, d=0), kf(.38, x=50, y=66, w=90, s=.96, o=0, d=0),
            kf(.5, x=50, y=60, w=90, s=1, o=1, d=0), kf(.65, x=50, y=60, w=90, s=1, o=1, d=1),
            kf(.72, x=50, y=60, w=90, s=1, o=1, d=1), kf(.94, x=50, y=60, w=90, s=1, o=1, d=1.9),
            kf(1, x=50, y=60, w=90, s=1, o=1, d=1.9)]},
    ],
}

SCENES = [billing, pm, locates]

# =====================================================================================
# output
# =====================================================================================
scenes_html = ""
for sc in SCENES:
    link = f'<a class="more" href="{sc["link"][1]}">{sc["link"][0]} <span aria-hidden="true">›</span></a>' if sc.get("link") else ""
    feats = "".join(
        f'<li data-step="{i}"{" class=is-active" if i == 0 else ""}><button type="button"><b>{t}</b><span>{d}</span></button></li>'
        for i, (t, d) in enumerate(sc["feats"]))
    scenes_html += f'''
  <section class="scene" id="story-{sc["id"]}" data-scene="{sc["id"]}">
    <div class="pin">
      <div class="head">
        <span class="label">{sc["name"]}</span>
        <h3>{sc["title"]}</h3>
        <p class="sub">{sc["sub"]}</p>
        {link}
        <ul class="feats">{feats}</ul>
      </div>
      <div class="stage">{sc["html"]}</div>
    </div>
  </section>'''

CSS = open(os.path.join(HERE, "story.css")).read()
astro = f'''---
/* Product story: three pinned scenes (Billing, Project Management, Locates), each three scroll steps.
   GENERATED by reference/gen_story.py; styles in reference/story.css. Edit those, not this file. */
---
<div class="story container-wide" id="story" aria-label="How Clad works">{scenes_html}
</div>

<script src="../scripts/story.js"></script>

<style is:global>
{CSS}
</style>
'''
open(f"{ROOT}/src/components/ProductStory.astro", "w").write(astro)

config = ("// Generated by reference/gen_story.py. x/y are actor centers in % of the stage, w is width %, s scale,\n"
          "// o opacity, d draw progress (--draw), v a counted value. `at` and `steps` are scroll progress 0..1.\n")
config += "export const SCENES = " + json.dumps(
    [{"id": sc["id"], "steps": STEPS, "actors": sc["actors"]} for sc in SCENES]) + ";\n"
open(f"{ROOT}/src/scripts/story.config.js", "w").write(config)

engine = r'''import { SCENES } from "./story.config.js";

// Scroll-scrubbed keyframe engine. Each scene is a tall section with a sticky frame; progress p (0..1)
// is how far the section has scrolled. Every actor's pose is interpolated from its keyframes, and the
// feature list highlights whichever step p is in. Clicking a feature scrolls to its step.
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
  if (pose.s != null) el.style.transform = `scale(${pose.s})`;
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
    const top = window.scrollY + sec.getBoundingClientRect().top + (cfg.steps[i] + 0.06) * total();
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
'''
open(f"{ROOT}/src/scripts/story.js", "w").write(engine)
print("generated")
