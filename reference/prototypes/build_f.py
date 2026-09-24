import json, math
from build import BASE_CSS, FONTS, nav, close

F_CSS = r"""
:root{--c1:#6D6AF0;--c2:#1FA48C;--c3:#E08A1E}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--c1:#8A88FF;--c2:#3DC4AB;--c3:#F2A544}}
:root[data-theme="dark"]{--c1:#8A88FF;--c2:#3DC4AB;--c3:#F2A544}
.orbit{position:relative;height:520vh}
.pin{position:sticky;top:calc(env(safe-area-inset-top,0px));height:100vh;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(260px,.9fr);gap:clamp(20px,4vw,64px);align-items:center;padding-block:16px}
.wheel{position:relative;width:100%;max-width:640px;aspect-ratio:1;margin:0 auto;container-type:inline-size;font-size:clamp(9px,1.9cqw,13px)}
.wheel svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.ring{fill:none;stroke:var(--line);stroke-width:.35}
.tick{stroke:var(--line);stroke-width:.35}
.day{font-family:var(--mono);font-size:2.4px;letter-spacing:.3px;fill:var(--muted);text-anchor:middle;text-transform:uppercase}
.rlab{font-family:var(--mono);font-size:2px;dominant-baseline:middle;letter-spacing:.35px;fill:var(--muted);text-transform:uppercase;stroke:var(--bg);stroke-width:1.4;paint-order:stroke;stroke-linejoin:round}
.rlab.c1{fill:var(--c1)}.rlab.c2{fill:var(--c2)}.rlab.c3{fill:var(--c3)}
.sweep{stroke:var(--ink);stroke-width:.35;stroke-linecap:round;opacity:.55}
.sweep-dot{fill:var(--ink)}
.edge{fill:none;stroke:var(--ink);stroke-width:.4;stroke-linecap:round;opacity:0;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .9s cubic-bezier(.2,.7,.2,1),opacity .3s}
.edge.on{opacity:.35;stroke-dashoffset:0}
.hub{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);text-align:center;width:34%}
.hub .k{font-family:var(--mono);font-size:.8em;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.hub b{display:block;font-weight:700;font-size:1.35em;letter-spacing:-.02em;line-height:1.1;margin-top:.2em}
.hub .wk{font-family:var(--mono);font-size:.85em;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);margin-top:.5em;font-variant-numeric:tabular-nums}
.node{position:absolute;width:0;height:0;z-index:1}.node.lit{z-index:2}.node.now{z-index:3}
.node i{position:absolute;left:-.45em;top:-.45em;width:.9em;height:.9em;border-radius:50%;background:var(--shape-2);border:2px solid var(--bg);box-shadow:0 0 0 1px var(--line);transition:transform .35s cubic-bezier(.2,.8,.2,1.2),background .3s}
.node span{position:absolute;top:-.85em;white-space:nowrap;font-size:.95em;font-weight:500;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:.25em .7em;opacity:0;transform:translateY(.4em);transition:opacity .35s,transform .35s;line-height:1.2}
.node.L span{right:1em}.node.R span{left:1em}
.node.T span,.node.B span{left:50%;transform:translate(-50%,.4em)}.node.T span{top:auto;bottom:.9em}.node.B span{top:.9em}
.node.T.lit span,.node.B.lit span{transform:translate(-50%,0)}
.node.lit i{background:var(--nc);transform:scale(1.25)}
.node.lit span{opacity:1;transform:none}
.node.past span{opacity:.55;color:var(--muted)}
.node.now i{transform:scale(1.7);box-shadow:0 0 0 .45em color-mix(in srgb,var(--nc) 22%,transparent)}
.node.now span{border-color:var(--nc);font-weight:600}
.node.c1{--nc:var(--c1)}.node.c2{--nc:var(--c2)}.node.c3{--nc:var(--c3)}
/* caption column */
.side{position:relative;display:grid;grid-template-rows:auto auto;padding-bottom:28px}
.cap{grid-area:1/1;opacity:0;transform:translateY(10px);transition:opacity .35s,transform .35s}
.cap.on{opacity:1;transform:none}
.cap .eb{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.cap .eb b{font-weight:500;color:var(--cc)}
.cap h3{font-size:clamp(24px,2.4vw,34px);margin-top:10px;letter-spacing:-.02em}
.cap p{color:var(--muted);font-size:16px;margin:12px 0 0;max-width:38ch}
.legend{grid-row:2;display:flex;gap:16px;flex-wrap:wrap;margin-top:22px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.legend span{display:flex;align-items:center;gap:6px}.legend i{width:8px;height:8px;border-radius:50%}
.hint{position:absolute;bottom:0;left:0;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
@media (max-width:900px){
  .pin{grid-template-columns:1fr;align-content:start;gap:12px;padding-top:12px}
  .wheel{max-width:min(92vw,52vh)}
  .side{min-height:11em}.cap h3{font-size:22px}.cap p{font-size:15px}.legend{display:none}
  .node span{font-size:.9em}
}
@media (prefers-reduced-motion:reduce){.edge{transition:none}}
"""

DAYS=["Mon","Tue","Wed","Thu","Fri"]
RING={"c":22,"m":33,"b":44}
RINGCLS={"c":"c1","m":"c2","b":"c3"}
# nodes: id, t (days, 0 = W1 Mon), ring, label
NODES=[
 ("n1",0.0,"c","Logged · 1,000 FT · 2 HH","L"),
 ("n2",1.0,"m","Approved","R"),
 ("n3",2.0,"m","AT&T check-in · 108 / 500 HH","R"),
 ("n4",2.45,"m","Forecast · +1 crew","L"),
 ("n5",3.0,"c","Logged · 1,400 FT","R"),
 ("n6",4.0,"c","Logged · 3 HH · 800 FT","L"),
 ("n7",5.0,"b","Invoice #14 → QuickBooks","R"),
 ("n8",5.4,"b","3 sub bills matched","R"),
 ("n9",6.0,"c","Crew 4 starts · 900 FT","B"),
 ("n10",7.15,"m","AT&T check-in · 131 / 500 HH","B"),
 ("n11",8.0,"c","Logged · 4 HH · 1,200 FT","L"),
 ("n12",9.25,"m","5-project report","R"),
]
EDGES=[("n1","n2"),("n2","n3"),("n3","n4"),("n4","n9"),("n1","n7"),("n5","n7"),("n6","n7"),("n7","n8"),("n9","n10"),("n3","n10"),("n10","n12"),("n11","n12"),("n8","n12")]
CAPS=[
 (0.0,"Week 1 · Monday","Capture","c1","1,000 feet of fiber and two hand holes go in.","The crew logs quantities, photos, and the redline from the truck. The inner ring turns every day. This is the one record everything else reads from."),
 (1.0,"Week 1 · Tuesday","Manage","c2","Someone checks it.","You open Monday's update, look at the photos and quantities, and approve. Nothing gets re-typed."),
 (2.0,"Week 1 · Wednesday","Manage","c2","AT&T asks how far along you are.","Of 500 planned hand holes, 108 are in. Percent complete comes straight from approved production."),
 (2.45,"Week 1 · Wednesday","Manage","c2","You're behind.","Clad's forecast shows the gap to the target date and what closes it: one more crew. Meanwhile the crew keeps logging Thursday and Friday."),
 (5.0,"Week 2 · Monday","Bill","c3","Time to bill last week.","Select the week's approved updates. Clad builds the invoice and syncs it to QuickBooks. The outer ring turns every two weeks; this is its first stop."),
 (5.45,"Week 2 · Monday","Bill","c3","Sub bills land in your inbox.","Clad ties each bill to the update it covers, so you pay for what was built."),
 (6.0,"Week 2 · Tuesday","Capture","c1","The fix from last Wednesday shows up in the field.","Crew 4 starts. Their first update lands on the same inner ring, and the loop keeps going."),
 (7.0,"Week 2 · Wednesday","Manage","c2","AT&T asks again. 131 of 500.","Back on pace. Same check-in, same view, one week of production later."),
 (9.0,"Week 2 · Friday","Manage","c2","Your boss wants all five projects.","One production report across every job you manage. Every node on this wheel feeds it."),
]

def polar(t, ring, week_offset=True):
    ang = -90 + 72*t
    w = int(t//5)
    r = RING[ring] + (3.2*w if week_offset else 0)
    a = math.radians(ang)
    return 50 + r*math.cos(a), 50 + r*math.sin(a), ang

def build_f():
    pos={}
    nodes_html=""
    for (nid,t,ring,label,side) in NODES:
        x,y,ang=polar(t,ring)
        pos[nid]=(x,y)
        nodes_html+=f'<div class="node {RINGCLS[ring]} {side}" data-t="{t}" style="left:{(x+4)/1.08:.2f}%;top:{(y+4)/1.08:.2f}%"><i></i><span>{label}</span></div>'
    edges_svg=""
    for (a,b) in EDGES:
        x1,y1=pos[a]; x2,y2=pos[b]
        mx,my=(x1+x2)/2,(y1+y2)/2
        # pull the control point toward the hub so edges bow inward and cross like a web
        cx,cy=50+(mx-50)*0.55, 50+(my-50)*0.55
        edges_svg+=f'<path class="edge" data-a="{a}" data-b="{b}" pathLength="1" d="M{x1:.2f} {y1:.2f} Q{cx:.2f} {cy:.2f} {x2:.2f} {y2:.2f}"/>'
    rings_svg="".join(f'<circle class="ring" cx="50" cy="50" r="{r}"/>' for r in RING.values())
    ticks=""
    for i,d in enumerate(DAYS):
        a=math.radians(-90+72*i)
        x1,y1=50+46.5*math.cos(a),50+46.5*math.sin(a); x2,y2=50+48*math.cos(a),50+48*math.sin(a)
        tx,ty=50+50.6*math.cos(a),50+50.6*math.sin(a)+0.8
        ticks+=f'<line class="tick" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/><text class="day" x="{tx:.2f}" y="{ty:.2f}">{d}</text>'
    # ring labels along the upper-left of each ring
    rlabs="<defs>"
    for ring in RING:
        r=RING[ring]-1.7
        rlabs+=f'<path id="rp-{ring}" d="M{50-r:.2f} 50 A{r:.2f} {r:.2f} 0 1 1 {50+r:.2f} 50 A{r:.2f} {r:.2f} 0 1 1 {50-r:.2f} 50"/>'
    rlabs+="</defs>"
    for ring,txt,cls in (("c","Capture · daily","c1"),("m","Manage · weekly","c2"),("b","Bill · every 2 weeks","c3")):
        rlabs+=f'<text class="rlab {cls}"><textPath href="#rp-{ring}" startOffset="37.5%" text-anchor="middle">{txt}</textPath></text>'
    caps_html="".join(f'<div class="cap{" on" if i==0 else ""}" style="--cc:var(--{c})"><div class="eb">{wk} · <b>{pillar}</b></div><h3>{h}</h3><p>{p}</p></div>' for i,(t,wk,pillar,c,h,p) in enumerate(CAPS))
    cap_ts=[c[0] for c in CAPS]
    node_ts={n[0]:n[1] for n in NODES}
    return f'''<title>Clad Orbit</title>
{FONTS}
<style>{BASE_CSS}{F_CSS}</style>
{nav()}
<section class="wrap hero">
  <div class="eyebrow">Field software for telecom, utility, and infrastructure contractors</div>
  <h1>Capture, manage, bill. Not in that order.</h1>
  <p>The field logs every day. Approvals and check-ins happen through the week. Billing comes around every two weeks. One record keeps all three cycles in sync. Scroll to turn two weeks on one project.</p>
  <div class="row"><button class="btn accent" type="button">Book a demo</button><button class="btn ghost" type="button">Turn the wheel</button></div>
</section>
<section class="wrap orbit" id="orbit">
  <div class="pin">
    <div class="wheel" id="wheel">
      <svg viewBox="-4 -4 108 108" aria-hidden="true">
        {rings_svg}{ticks}{rlabs}
        <g id="edges">{edges_svg}</g>
        <g id="sweep"><line class="sweep" x1="50" y1="50" x2="50" y2="3.5"/><circle class="sweep-dot" cx="50" cy="3.5" r=".9"/></g>
      </svg>
      {nodes_html}
      <div class="hub"><div class="k">Maple Run</div><b>Fiber build · 500 HH</b><div class="wk" id="wk">Week 1 · Mon</div></div>
    </div>
    <div class="side">
      {caps_html}
      <div class="legend"><span><i style="background:var(--c1)"></i>Capture · daily</span><span><i style="background:var(--c2)"></i>Manage · weekly</span><span><i style="background:var(--c3)"></i>Bill · every 2 weeks</span></div>
      <div class="hint" id="hint">Scroll to advance the week</div>
    </div>
  </div>
</section>
{close()}
<script>
(function(){{
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var sec=document.getElementById('orbit'), sweep=document.getElementById('sweep'), wk=document.getElementById('wk'), hint=document.getElementById('hint');
  var nodes=[].slice.call(document.querySelectorAll('.node')), edges=[].slice.call(document.querySelectorAll('.edge')), caps=[].slice.call(document.querySelectorAll('.cap'));
  var NT={json.dumps(node_ts)}, CT={json.dumps(cap_ts)}, DAYS={json.dumps(DAYS)};
  var TOTAL=10;
  function clamp(v,a,b){{return Math.max(a,Math.min(b,v));}}
  function render(p){{
    var t=p*TOTAL, lit={{}}, last=null, lastT=-1;
    nodes.forEach(function(n){{
      var nt=+n.dataset.t, on=t>=nt;
      n.classList.toggle('lit',on);
      if(on && nt>lastT){{lastT=nt;last=n;}}
    }});
    nodes.forEach(function(n){{ n.classList.toggle('now',n===last); n.classList.toggle('past',n.classList.contains('lit')&&n!==last&&(t-(+n.dataset.t))>2.5); }});
    edges.forEach(function(e){{ e.classList.toggle('on', t>=NT[e.dataset.a] && t>=NT[e.dataset.b]); }});
    var ang=-90+72*Math.min(t,TOTAL)+90; sweep.setAttribute('transform','rotate('+ang+' 50 50)');
    var w=Math.min(2,Math.floor(t/5)+1), d=DAYS[clamp(Math.floor(t%5),0,4)];
    wk.textContent='Week '+w+' · '+(t>=TOTAL?'Fri':d);
    var c=0; CT.forEach(function(th,i){{ if(t>=th) c=i; }});
    caps.forEach(function(el,i){{ el.classList.toggle('on',i===c); }});
    hint.style.opacity=p<.02?1:0;
  }}
  var ticking=false;
  function measure(){{
    ticking=false;
    var r=sec.getBoundingClientRect(), total=sec.offsetHeight-window.innerHeight;
    var p=clamp(-r.top/total,0,1);
    render(reduce?(p<.5?0:1):p);
  }}
  window.addEventListener('scroll',function(){{if(!ticking){{ticking=true;requestAnimationFrame(measure);}}}},{{passive:true}});
  window.addEventListener('resize',measure); measure();
}})();
</script>'''

open('f-orbit.html','w').write(build_f()); print('built f')
