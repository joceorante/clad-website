import json
from build import BASE_CSS, FONTS, nav, close

D_FONTS = FONTS.replace('&display=swap', '&family=Caveat:wght@500;600&display=swap')

D_CSS = r"""
.morph{position:relative;height:340vh}
.pin{position:sticky;top:calc(env(safe-area-inset-top,0px));height:100vh;display:flex;flex-direction:column;justify-content:center;gap:18px;padding-block:16px}
.pin .sec-head{padding-top:0}
.pin .sec-head h2{font-size:clamp(26px,3.2vw,40px)}
.stage{position:relative;height:auto;width:100%;max-width:960px;margin:0 auto;aspect-ratio:16/9;container-type:inline-size;font-size:clamp(9px,1.35cqw,13px)}
@media (max-width:700px){.stage{aspect-ratio:4/5}.pin{gap:12px}}
.frame{position:absolute;left:18%;top:8%;width:64%;height:84%;background:var(--bg);border:1px solid var(--line);border-radius:1.6em;box-shadow:var(--shadow);opacity:0}
.frame .hd{position:absolute;left:0;right:0;top:0;padding:1.3em 1.6em;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;gap:1em}
.frame .hd b{font-weight:600;font-size:1.25em;letter-spacing:-.01em}
.frame .hd span{font-family:var(--mono);font-size:.85em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.frame .lab{position:absolute;font-family:var(--mono);font-size:.8em;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.stamp{position:absolute;right:1.6em;bottom:1.3em;font-family:var(--mono);font-size:.85em;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);border-radius:999px;padding:.4em .9em;opacity:0;transform:translateY(.5em)}
/* scraps */
.scrap{position:absolute;will-change:transform,left,top,width,height}
.scrap .raw,.scrap .ui{position:absolute;inset:0;border-radius:.6em;overflow:hidden}
.scrap .ui{opacity:0}
/* raw skins */
.raw.bubble{background:var(--card);border-radius:1.2em 1.2em 1.2em .3em;padding:.5em;box-shadow:0 12px 28px -16px rgba(0,0,0,.5)}
.raw.bubble .pic{position:absolute;inset:.5em .5em 1.7em .5em;background:linear-gradient(160deg,var(--shape),var(--shape-2));border-radius:.6em}
.raw.bubble .pic::after{content:"";position:absolute;left:18%;right:18%;bottom:22%;height:12%;background:var(--shape-2);opacity:.7;border-radius:2px;transform:rotate(-3deg)}
.raw.bubble .ts{position:absolute;left:.7em;bottom:.35em;font-size:.75em;color:var(--muted)}
.raw.page{background:#FAFAF7;color:#2A2823;box-shadow:0 12px 28px -16px rgba(0,0,0,.5);border-radius:.25em}
.raw.page i{position:absolute;left:12%;right:12%;height:2px;background:#D8D6D0}
.raw.page .red{position:absolute;left:16%;top:38%;width:70%;height:24%;border:2px solid #D64B3C;border-radius:50% 45% 55% 40%;transform:rotate(-6deg);background:transparent}
.raw.page .red::after{content:"HH here";position:absolute;right:-1.2em;top:-1.6em;font-family:"Caveat",cursive;color:#D64B3C;font-size:1.2em;transform:rotate(8deg)}
.raw.paper{background:#F7F3E3;color:#2A2823;box-shadow:0 12px 28px -16px rgba(0,0,0,.5);border-radius:.2em;background-image:repeating-linear-gradient(transparent 0 1.55em,#D9D2B8 1.55em 1.6em);padding:.9em 1em .5em 1.4em;font-family:"Caveat",cursive;font-size:1.45em;line-height:1.6em;font-weight:600}
.raw.paper::before{content:"";position:absolute;left:.9em;top:0;bottom:0;width:1px;background:#E3B4B0}
.raw.paper .stain{position:absolute;right:6%;bottom:6%;width:34%;aspect-ratio:1;border-radius:50%;border:.5em solid rgba(150,105,50,.18);box-shadow:inset 0 0 0 .3em rgba(150,105,50,.06)}
.raw.text{background:var(--accent);color:#fff;border-radius:1.2em 1.2em .3em 1.2em;padding:.7em .9em;font-size:1.05em;line-height:1.35;box-shadow:0 12px 28px -16px rgba(0,0,0,.5)}
.raw.text small{display:block;opacity:.7;font-size:.75em;margin-top:.3em}
/* ui skins */
.ui.thumb{background:linear-gradient(160deg,var(--shape),var(--shape-2));border-radius:.6em}
.ui.thumb.pdf{background:var(--card);border:1px solid var(--line)}
.ui.thumb.pdf i{position:absolute;left:14%;right:14%;height:2px;background:var(--shape-2)}
.ui.thumb.pdf .red{position:absolute;left:18%;top:40%;width:64%;height:22%;border:2px solid var(--accent);border-radius:50% 45% 55% 40%}
.ui.fields{display:grid;grid-template-columns:1fr 1fr;gap:.6em;border-radius:0}
.ui.fields div{border:1px solid var(--line);border-radius:.6em;padding:.55em .8em;background:var(--bg);display:flex;flex-direction:column;justify-content:center}
.ui.fields small{font-family:var(--mono);font-size:.7em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.ui.fields b{font-weight:600;font-size:1.15em;font-variant-numeric:tabular-nums}
.ui.note{border:1px solid var(--line);border-radius:.6em;padding:.55em .8em;background:var(--bg);font-size:1em;display:flex;align-items:center;gap:.6em;color:var(--ink)}
.ui.note em{font-style:normal;font-family:var(--mono);font-size:.7em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);flex:none}
/* captions */
.caps{position:relative;height:3.2em;max-width:960px;margin:0 auto;width:100%;text-align:center}
.caps p{position:absolute;inset:0;margin:0;color:var(--muted);font-size:clamp(15px,1.5vw,18px);opacity:0;transform:translateY(6px);transition:opacity .35s,transform .35s}
.caps p.on{opacity:1;transform:none}
.caps p b{color:var(--ink);font-weight:600}
.hint{text-align:center;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
"""

# scraps: name, kind, start(x,y,w,h,rot), end(x,y,w,h), delay
# x,y,w,h in % of stage
SCRAPS = [
 ("p1","photo",( 1, 6,19,20,-9),(21.5,29,11.5,15),0.00),
 ("p2","photo",(72, 2,18,19, 7),(34.5,29,11.5,15),0.05),
 ("p3","photo",(79,50,17,18,-5),(47.5,29,11.5,15),0.10),
 ("pdf","pdf",(29, 1,20,30, 4),(63,29,15,15),0.13),
 ("sheet","sheet",( 6,54,25,36, 6),(21.5,55,56.5,14),0.18),
 ("txt","text",(46,66,27,20,-4),(21.5,75,56.5,10),0.22),
]

def scrap_html(name, kind):
    if kind=="photo":
        raw='<div class="raw bubble"><div class="pic"></div><span class="ts">Mon 4:52 PM</span></div>'
        ui='<div class="ui thumb"></div>'
    elif kind=="pdf":
        raw='<div class="raw page"><i style="top:14%"></i><i style="top:22%"></i><i style="top:30%"></i><i style="top:72%"></i><i style="top:80%"></i><div class="red"></div></div>'
        ui='<div class="ui thumb pdf"><i style="top:16%"></i><i style="top:26%"></i><i style="top:74%"></i><div class="red"></div></div>'
    elif kind=="sheet":
        raw='<div class="raw paper">1000&#8217; fiber placed<br>2 HH set &mdash; 4th &amp; Main<br>crew 3<div class="stain"></div></div>'
        ui='<div class="ui fields"><div><small>Fiber placed</small><b>1,000 FT</b></div><div><small>Hand holes</small><b>2 HH</b></div></div>'
    else:
        raw='<div class="raw text">done w/ 2 HH at 4th st, pics attached<small>Mon 4:55 PM</small></div>'
        ui='<div class="ui note"><em>Note</em>Both hand holes set at 4th &amp; Main. Photos attached.</div>'
    return f'<div class="scrap" data-s="{name}">{raw}{ui}</div>'

def build_d():
    scraps="".join(scrap_html(n,k) for (n,k,_,_,_) in SCRAPS)
    defs=json.dumps([{"s":list(s),"e":list(e),"d":d} for (_,_,s,e,d) in SCRAPS])
    return f'''<title>Clad Morph</title>
{D_FONTS}
<style>{BASE_CSS}{D_CSS}</style>
{nav()}
<section class="wrap hero">
  <div class="eyebrow">Field software for telecom, utility, and infrastructure contractors</div>
  <h1>Monday's work, the way it actually arrives.</h1>
  <p>Photos in a group chat. A marked-up PDF. A quantity sheet from the truck. Scroll to watch it become one update.</p>
  <div class="row"><button class="btn accent" type="button">Book a demo</button><button class="btn ghost" type="button">Scroll to see it</button></div>
</section>
<section class="wrap morph" id="morph">
  <div class="pin">
    <div class="sec-head"><div class="eyebrow">Capture</div><h2>Enter the work once.</h2></div>
    <div class="stage" id="stage">
      <div class="frame" id="frame">
        <div class="hd"><b>Field update · Mon, Sep 14</b><span>Crew 3 · 4th &amp; Main</span></div>
        <div class="lab" style="left:5.5%;top:21%">Photos</div>
        <div class="lab" style="left:70.5%;top:21%">As-built</div>
        <div class="lab" style="left:5.5%;top:52%">Quantities</div>
        <div class="lab" style="left:5.5%;top:75.5%">Notes</div>
        <div class="stamp" id="stamp">Ready for approval</div>
      </div>
      {scraps}
    </div>
    <div class="caps" id="caps">
      <p class="on">Six things, five places, <b>one Monday</b>.</p>
      <p>Clad gathers them into <b>a single field update</b>.</p>
      <p>Photos, redline, quantities, notes. <b>Entered once.</b> Tuesday, someone just approves it.</p>
    </div>
    <div class="hint" id="hint">Scroll</div>
  </div>
</section>
<section class="wrap">
  <div class="sec-head"><div class="eyebrow">Then</div><h2>That one update runs the rest of the week.</h2><p>Approval on Tuesday. Percent complete for the AT&amp;T check-in. The forecast. Next Monday's invoice, synced to QuickBooks. Sub bills matched against it. Nothing re-typed.</p></div>
</section>
{close()}
<script>
(function(){{
  var DEFS={defs};
  var sec=document.getElementById('morph'), frame=document.getElementById('frame'), stamp=document.getElementById('stamp');
  var caps=[].slice.call(document.querySelectorAll('#caps p')), hint=document.getElementById('hint');
  var els=[].slice.call(document.querySelectorAll('.scrap'));
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function clamp(v,a,b){{return Math.max(a,Math.min(b,v));}}
  function smooth(p,a,b){{var t=clamp((p-a)/(b-a),0,1);return t*t*(3-2*t);}}
  function ease(t){{return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}}
  function lerp(a,b,t){{return a+(b-a)*t;}}
  var END=0.72;
  function render(p){{
    els.forEach(function(el,i){{
      var d=DEFS[i], s=d.s, e=d.e;
      var t=ease(clamp((p-d.d)/(END-d.d),0,1));
      el.style.left=lerp(s[0],e[0],t)+'%'; el.style.top=lerp(s[1],e[1],t)+'%';
      el.style.width=lerp(s[2],e[2],t)+'%'; el.style.height=lerp(s[3],e[3],t)+'%';
      el.style.transform='rotate('+(s[4]*(1-t))+'deg)';
      el.style.zIndex= t<1 ? 5 : 3;
      var k=smooth(t,.55,.95);
      el.children[0].style.opacity=1-k; el.children[1].style.opacity=k;
    }});
    var f=smooth(p,.42,.7); frame.style.opacity=f;
    var st=smooth(p,.86,.98); stamp.style.opacity=st; stamp.style.transform='translateY('+(0.5-0.5*st)+'em)';
    var c = p<.34?0 : p<.8?1 : 2;
    caps.forEach(function(el,i){{el.classList.toggle('on',i===c);}});
    hint.style.opacity = p<.02 ? 1 : 0;
  }}
  var ticking=false;
  function measure(){{
    ticking=false;
    var r=sec.getBoundingClientRect(); var total=sec.offsetHeight-window.innerHeight;
    var p=clamp(-r.top/total,0,1);
    render(reduce?(p<.5?0:1):p);
  }}
  window.addEventListener('scroll',function(){{if(!ticking){{ticking=true;requestAnimationFrame(measure);}}}},{{passive:true}});
  window.addEventListener('resize',measure); measure();
}})();
</script>'''

open('d-morph.html','w').write(build_d()); print('built d')
