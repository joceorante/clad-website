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
    company = any(t in name for t in ("Underground", "Boring", "Civil", "Fiber", "Intrepid"))
    ini = "".join(w[0] for w in name.replace(".", "").split()[:2]).upper()
    return f'<span class="who {"co" if company else "person"}"><i>{ini}</i>{name}</span>'


# =====================================================================================
# 1. BILLING: daily updates -> invoice built from them -> synced to QuickBooks
# =====================================================================================
ICON_DOC = ('<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 1.5h5.5L13 5v9.5H4z"/>'
            '<path d="M9.5 1.5V5H13M6 8.5h5M6 11h5"/></svg>')
ICON_IMG = ('<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><rect x="1.5" y="2.5" width="13" height="11" rx="1.5"/>'
            '<circle cx="5.5" cy="6.2" r="1.3"/><path d="M2 12.5l4-4 3 3 2-2 3.5 3.5"/></svg>')
UPDATES = [  # date, item, completed by, avatar tint, attachments  (layout from Jocelyn's "Daily updates" frame)
    ("Mon Sep 14", "Mount NID at service address", "D. Alvarez", "cobalt", ["pdf", "img"]),
    ("Tue Sep 15", "UG pull fiber drop", "Ortiz Underground", "orange", ["pdf"]),
    ("Wed Sep 16", "1.25” Conduit", "Bell Boring", "gray", ["img"]),
]
INVOICE_LINES = [  # code, item, qty, amount (qty x contract rate)
    ("D02", "Mount NID at service address", "24", "$290.88"),
    ("D03", "UG pull fiber drop", "180", "$1,530.00"),
    ("GT-CON01", "1.25” Conduit", "271", "$2,200.52"),
]
INVOICE_TOTAL = 4021.40


def update_card(date, item, by, tint, att):
    ini = "".join(w[0] for w in by.replace(".", "").split()[:2]).upper()
    icons = "".join(ICON_DOC if a == "pdf" else ICON_IMG for a in att)
    return (f'<div class="card ucard"><div class="ut"><b class="item">{item}</b>'
            f'<span class="by"><i class="t-{tint}">{ini}</i>{by}</span></div><span class="att">{icons}</span></div>')


INVOICE_HTML = (
    '<div class="card invoice">'
    '<div class="vhd"><div><b>Invoice #487</b><span>Intrepid · Suffolk, VA - Z1.4</span></div></div>'
    '<div class="vdue"><span data-count="money">$0.00</span><small>due Oct 1, 2026</small></div>'
    '<div class="vth"><span>Description</span><span>Qty</span><span>Amount</span></div>'
    + "".join(
        f'<div class="row" style="--i:{i}"><span class="item"><em>{c}</em> {n}<small>From {UPDATES[i][0]} update</small></span><span>{q}</span><span>{a}</span></div>'
        for i, (c, n, q, a) in enumerate(INVOICE_LINES))
    + '<div class="vtot"><span>Amount due</span><b data-count="money">$0.00</b></div></div>')

QB_HTML = (
    '<div class="qbchip"><span class="qbi" aria-hidden="true">qb</span>'
    '<span class="txt"><b>Synced to QuickBooks</b><small>Invoice #487 · just now</small></span>'
    '<span class="ok" aria-hidden="true"></span></div>')

# step 1: cards cascade down and to the right, each overlapping the one above it (center x, y, tilt);
# the header lines up with the first card. ROW_Y is the invoice row each card lands on in step 2.
CARD_POS = [(40, 30, 0), (50, 50, 0), (60, 70, 0)]
ROW_Y = [44.5, 55, 65]  # measured centers of the invoice rows


def card_actor(i):
    x, y, r = CARD_POS[i]
    t0, land = .04 + i * .07, .52 + i * .06
    return {"id": f"u{i}", "kf": [
        kf(0, x=x, y=y + 10, w=60, s=.97, o=0, r=r), kf(t0, x=x, y=y + 10, w=60, s=.97, o=0, r=r),
        kf(t0 + .1, x=x, y=y, w=60, s=1, o=1, r=r), kf(land - .08, x=x, y=y, w=60, s=1, o=1, r=r),
        kf(land, x=50, y=ROW_Y[i], w=60, s=.5, o=0, r=0), kf(1, x=50, y=ROW_Y[i], w=60, s=.5, o=0, r=0)]}


billing = {
    "id": "billing", "name": "Billing", "accent": "orange", "title": "Bill accurately",
    "sub": "One system to prevent over- and under-billing",
    "feats": [
        ("Production tracking", "Collect daily production and documentation from the field"),
        ("Linked invoices & bills", "Tie your invoices and bills directly to approved production, so you only bill for work that’s done"),
        ("QBO integration", "Sync invoices with QuickBooks to speed up AR accounting and track retainage"),
    ],
    "html": (
        f'<div class="act" data-a="invoice">{INVOICE_HTML}</div>'
        + "".join(f'<div class="act" data-a="u{i}">{update_card(*u)}</div>' for i, u in enumerate(UPDATES))
        + f'<div class="act" data-a="qb">{QB_HTML}</div>'
    ),
    "actors": [
        # step 2: the invoice forms, and each update card flies into the line it becomes
        {"id": "invoice", "kf": [
            kf(0, x=50, y=48, w=64, s=.96, o=0, d=0, v=0), kf(.38, x=50, y=48, w=64, s=.96, o=0, d=0, v=0),
            kf(.46, x=50, y=45, w=64, s=1, o=1, d=0, v=0), kf(.66, x=50, y=45, w=64, s=1, o=1, d=1, v=INVOICE_TOTAL),
            kf(1, x=50, y=45, w=64, s=1, o=1, d=1, v=INVOICE_TOTAL)]},
        # step 1: field updates float in as loose cards
        *[card_actor(i) for i in range(3)],
        # step 3: a single sync chip lands under the invoice
        {"id": "qb", "kf": [
            kf(0, x=50, y=92, w=46, s=.7, o=0, d=0), kf(.72, x=50, y=92, w=46, s=.7, o=0, d=0),
            kf(.8, x=50, y=88, w=46, s=1, o=1, d=0), kf(.9, x=50, y=88, w=46, s=1, o=1, d=1),
            kf(1, x=50, y=88, w=46, s=1, o=1, d=1)]},
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
# Each as-built run gets its own color, and those colors carry into the report as its three series.
RUN_A, RUN_B, RUN_C = "#ff5900", "#4750ff", "#2f9e5b"  # BM60 bore run, UG-104-02 drop, UG-104-03 handhole
BP_SEG1 = "98,305 414,354.5"   # circle -> vertex (run A)
BP_SEG2 = "414,354.5 462,178"  # vertex -> right square (run B)
BP_SQUARES = [(251, 73, 31, RUN_C), (450, 161, 32, RUN_B)]  # x, y, size (stroke centerline), color
BP_CIRCLE = (98, 305, 16, RUN_A)
BP_LABELS = [  # box x, y, w, text, color; cascade order follows the line, the standalone square last
    (56, 340, 90, "BDO3-01", RUN_A),
    (227, 365, 154, "BM60(1)(1.25)-01", RUN_A),
    (414, 214, 105, "UG-104-02", RUN_B),
    (214, 122, 105, "UG-104-03", RUN_C),
]
BP_VIEW = "0 46 547 354"  # crop to a 16:10-ish landscape frame


def bp_label(i, x, y, w, text, color):
    return (f'<g class="lbl" style="--i:{i}"><rect class="lbox" x="{x}" y="{y}" width="{w}" height="28"/>'
            f'<rect x="{x + 8}" y="{y + 10}" width="8" height="8" rx="1.5" fill="{color}"/>'
            f'<text x="{x + 6 + w / 2:.1f}" y="{y + 19}" text-anchor="middle">{text}</text></g>')


def bp_ink():
    sq = "".join(f'<rect class="k" x="{x}" y="{y}" width="{n}" height="{n}"/>' for x, y, n, _ in BP_SQUARES)
    cx, cy, r, _ = BP_CIRCLE
    return f'<polyline points="{BP_SEG1} 462,178"/>{sq}<circle class="k" cx="{cx}" cy="{cy}" r="{r}"/>'


def bp_runs():
    (x1, y1, n1, c1), (x2, y2, n2, c2) = BP_SQUARES
    cx, cy, r, ca = BP_CIRCLE
    return (f'<polyline class="seg s1" pathLength="1" points="{BP_SEG1}" style="stroke:{RUN_A}"/>'
            f'<polyline class="seg s2" pathLength="1" points="{BP_SEG2}" style="stroke:{RUN_B}"/>'
            f'<circle class="mk ci" cx="{cx}" cy="{cy}" r="{r}" style="stroke:{ca}"/>'
            f'<rect class="mk sq2" x="{x2}" y="{y2}" width="{n2}" height="{n2}" style="stroke:{c2}"/>'
            f'<rect class="mk sq1" x="{x1}" y="{y1}" width="{n1}" height="{n1}" style="stroke:{c1}"/>')


BLUEPRINT_SVG = (
    f'<svg class="bpsvg" viewBox="{BP_VIEW}" aria-hidden="true">'
    '<rect width="547" height="456" fill="#fff"/>'
    + MAP_G
    # the black markup from the start frame, covered stroke by stroke as the colored runs draw over it
    + f'<g class="ink">{bp_ink()}</g>'
    + f'<g class="runs">{bp_runs()}</g>'
    + "".join(bp_label(i, *l) for i, l in enumerate(BP_LABELS))
    + '</svg>')

BLUEPRINT_HTML = (
    '<div class="card blueprint"><div class="chd"><b>As-built</b><span>Suffolk, VA · Zone 1.4 · Sheet 3 of 12</span>'
    '<em class="live">Live</em></div>' + BLUEPRINT_SVG + '</div>')

# weekly production report: one series per as-built run, in the run's color, then a dashed two-week forecast
SERIES = [(RUN_A, "BM60(1)(1.25)-01", [48, 55, 58, 50, 43, 22]),
          (RUN_B, "UG-104-02", [30, 38, 46, 44, 50, 53]),
          (RUN_C, "UG-104-03", [8, 14, 11, 20, 24, 30])]
FORECAST = {RUN_A: [28, 34], RUN_B: [55, 58], RUN_C: [35, 39]}
PW, PH, YMAX, FW = 600, 260, 60, 240


def pt(i, v):
    return (round(i * PW / 5, 1), round(PH - v / YMAX * PH, 1))


chart_svg = "".join(
    f'<line class="grid" x1="0" y1="{round(PH - i * 10 / YMAX * PH, 1)}" x2="{PW + FW}" y2="{round(PH - i * 10 / YMAX * PH, 1)}"/>'
    for i in range(7))
chart_svg += f'<rect class="fzone" x="{PW}" y="0" width="{FW}" height="{PH}"/><line class="today" x1="{PW}" y1="0" x2="{PW}" y2="{PH}"/>'
for color, _, vals in SERIES:
    pts = [pt(i, v) for i, v in enumerate(vals)]
    chart_svg += f'<polyline class="line" pathLength="1" points="{" ".join(f"{x},{y}" for x, y in pts)}" style="stroke:{color}"/>'
chart_svg += '<g class="fcast">'
for color, fv in FORECAST.items():
    fp = [pt(5 + i, v) for i, v in enumerate([dict((c, vs) for c, _, vs in SERIES)[color][-1]] + fv)]
    chart_svg += f'<polyline class="fline" points="{" ".join(f"{x},{y}" for x, y in fp)}" style="stroke:{color}"/>'
chart_svg += '</g>'

CHART_HTML = (
    '<div class="card report" role="img" aria-label="Weekly production report for the three as-built runs, with a two-week forecast">'
    '<div class="chd"><b>Weekly Production Report</b><span>Zone 1.4</span></div>'
    '<div class="plot"><div class="ylab">' + "".join(f'<span>${v}k</span>' for v in range(60, -1, -20)) + '</div>'
    f'<svg viewBox="0 0 {PW + FW} {PH}" preserveAspectRatio="none" aria-hidden="true">{chart_svg}</svg>'
    '<div class="xlab">' + "".join(f'<span>{d}</span>' for d in ["Mar 2", "Mar 16", "Mar 30"]) + '<span class="fx">Apr 20</span></div></div></div>')

pm = {
    "id": "pm", "name": "Project Management", "accent": "cobalt", "title": "Stay on top of every project",
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
            kf(0, x=50, y=50, w=70, s=1, o=1, d=0), kf(.05, x=50, y=50, w=70, s=1, o=1, d=0),
            kf(.22, x=50, y=50, w=70, s=1, o=1, d=1), kf(.32, x=50, y=50, w=70, s=1, o=1, d=1.8),
            kf(.36, x=50, y=50, w=70, s=1, o=1, d=1.8), kf(.48, x=50, y=40, s=.88, w=70, o=.35, d=1.8)]},
        # step 2: the report comes forward with the runs' colors and draws; step 3: the forecast extends it
        {"id": "chart", "kf": [
            kf(0, x=50, y=60, w=70, s=.96, o=0, d=0), kf(.38, x=50, y=60, w=70, s=.96, o=0, d=0),
            kf(.48, x=50, y=56, w=70, s=1, o=1, d=0), kf(.65, x=50, y=56, w=70, s=1, o=1, d=1),
            kf(.72, x=50, y=56, w=70, s=1, o=1, d=1), kf(.9, x=50, y=56, w=70, s=1, o=1, d=1.4),
            kf(1, x=50, y=56, w=70, s=1, o=1, d=1.4)]},
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
    '<div class="card tickets"><div class="chd"><b>Locate tickets</b><span class="filter"><em class="fa">Intrepid</em><em class="fb">All subcontractors</em></span></div>'
    '<div class="lth"><span>Ticket</span><span>Company</span><span>Status</span><span>Expires</span></div>'
    '<div class="rows"><div class="grp a">'
    + "".join(f'<div class="row" style="--j:{j}"><span class="tk"><b>{ad}</b><small>{t}</small></span>{avatar("Intrepid")}'
              f'<span class="st">{pill(a, "a")}{pill(b, "b")}</span><span class="ex">{ex}</span></div>'
              for j, (ad, t, (a, b), ex) in enumerate(MINE))
    + '</div><div class="grp b">'
    + "".join(f'<div class="row" style="--i:{i}"><span class="tk"><b>{ad}</b><small>{t}</small></span>{avatar(co)}'
              f'<span class="st">{pill(stt)}</span><span class="ex">{ex}</span></div>'
              for i, (ad, t, co, stt, ex) in enumerate(SUBS))
    + '</div></div></div>')

locates = {
    "id": "locates", "name": "Locates", "accent": "stoplight", "title": "Automate your 811 tickets",
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
            kf(0, x=50, y=50, w=62, s=1, o=1, d=0), kf(.04, x=50, y=50, w=62, s=1, o=1, d=0),
            kf(.24, x=50, y=50, w=62, s=1, o=1, d=1), kf(.3, x=50, y=50, w=62, s=1, o=1, d=1.3),
            kf(.36, x=50, y=50, w=62, s=1, o=1, d=1.3), kf(.48, x=50, y=36, w=62, s=.88, o=.35, d=1.3)]},
        # step 2: your tickets clear and renew; step 3: the view switches to subcontractor tickets
        {"id": "tickets", "kf": [
            kf(0, x=50, y=64, w=84, s=.96, o=0, d=0), kf(.38, x=50, y=64, w=84, s=.96, o=0, d=0),
            kf(.48, x=50, y=60, w=84, s=1, o=1, d=0), kf(.65, x=50, y=60, w=84, s=1, o=1, d=1),
            kf(.72, x=50, y=60, w=84, s=1, o=1, d=1), kf(.94, x=50, y=60, w=84, s=1, o=1, d=1.9),
            kf(1, x=50, y=60, w=84, s=1, o=1, d=1.9)]},
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
  <section class="scene" id="story-{sc["id"]}" data-scene="{sc["id"]}" style="--accent: var(--color-{sc["accent"]})">
    <div class="pin">
      <div class="head">
        <span class="label t-label"><i aria-hidden="true"></i>{sc["name"]}</span>
        <h3 class="t-title">{sc["title"]}</h3>
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
          "// r rotation (deg), o opacity, d draw progress (--draw), v a counted value. `at` and `steps` are scroll progress 0..1.\n")
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
