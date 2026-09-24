import json
from build import BASE_CSS, FONTS, nav, close
from build_d import D_CSS, D_FONTS, SCRAPS, scrap_html

E_CSS = r"""
.scene{position:relative;height:330vh}
.act{position:absolute;transform-origin:top left}
.panel2{background:var(--bg);border:1px solid var(--line);border-radius:1.4em;box-shadow:var(--shadow)}
.panel2 .hd{padding:1.1em 1.4em;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;gap:1em}
.panel2 .hd b{font-weight:600;font-size:1.15em;letter-spacing:-.01em}
.panel2 .hd span,.k{font-family:var(--mono);font-size:.8em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.tagpill{font-family:var(--mono);font-size:.8em;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);border-radius:999px;padding:.35em .8em;white-space:nowrap;display:inline-block}
/* manage: board */
.board{width:84%;height:88%}
.board .cols{position:absolute;left:1.2em;right:1.2em;top:4.4em;bottom:1.2em;display:grid;grid-template-columns:1fr 1fr 1fr;gap:1em}
.board .col{background:var(--card);border-radius:1em;padding:.9em}
.board .col h4{margin:0 0 .8em;font-family:var(--mono);font-size:.8em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500}
.board .ghost{height:4.2em;border-radius:.7em;background:var(--shape);margin-bottom:.7em;opacity:.75}
.mini{width:29%;height:15.5em;background:var(--bg);border:1px solid var(--line);border-radius:.9em;padding:.9em 1em;box-shadow:0 16px 34px -18px rgba(0,0,0,.55);overflow:visible}
.mini .d{font-family:var(--mono);font-size:.75em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.mini .t{font-weight:600;font-size:1.05em;margin-top:.25em}
.mini .thumbs{display:flex;gap:.4em;margin-top:.6em}.mini .thumbs i{flex:1;aspect-ratio:4/3;background:var(--shape);border-radius:.4em}
.mini .row{position:absolute;left:1em;right:1em;display:flex;justify-content:space-between;font-size:.95em;font-variant-numeric:tabular-nums}
.mini .row span:last-child{color:var(--muted)}
.mini .total{position:absolute;left:1em;right:1em;bottom:.8em;border-top:1px solid var(--line);padding-top:.5em;display:flex;justify-content:space-between;font-weight:600;font-variant-numeric:tabular-nums}
.mini .tag{position:absolute;right:.8em;top:.8em}
.chip{position:absolute;background:var(--ink);color:var(--bg);border-radius:999px;padding:.3em .7em;font-family:var(--mono);font-size:.72em;white-space:nowrap;box-shadow:0 8px 20px -10px rgba(0,0,0,.6)}
/* manage: dashboard */
.tile{background:var(--bg);border:1px solid var(--line);border-radius:1.2em;padding:1.1em 1.3em;box-shadow:var(--shadow)}
.tile h5{margin:0;font-family:var(--mono);font-size:.78em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500}
.tile .big{font-weight:700;font-size:1.9em;letter-spacing:-.02em;margin-top:.25em;font-variant-numeric:tabular-nums;line-height:1.1}
.tile .big small{font-size:.5em;color:var(--muted);font-weight:500}
.tile .bar{position:absolute;left:1.3em;right:1.3em;bottom:1.2em;height:.6em;background:var(--card);border-radius:.3em}
.tile .bar i{position:absolute;left:0;top:0;bottom:0;background:var(--accent);border-radius:.3em}
.chart .bars{position:absolute;left:1.3em;right:1.3em;bottom:3.4em;top:4.4em;display:flex;align-items:flex-end;gap:.8em;border-bottom:1px solid var(--line)}
.chart .bars i{position:relative;flex:1;background:var(--shape);border-radius:.3em .3em 0 0}
.chart .bars i.now{background:var(--accent)}
.chart .fc{position:absolute;left:1.3em;right:1.3em;bottom:1em;display:flex;justify-content:space-between;gap:1em;font-size:.9em;color:var(--muted)}
.chart .fc b{color:var(--accent);font-weight:600}
/* bill */
.list{width:34%;height:84%}.inv{width:52%;height:84%}
.urow{position:absolute;inset:0;display:flex;align-items:center;gap:.7em;background:var(--card);border-radius:.7em;padding:0 .9em;font-size:.92em;white-space:nowrap;overflow:hidden}
.urow .cb{width:1.05em;height:1.05em;border-radius:.3em;background:var(--accent);flex:none;position:relative}
.urow .cb::after{content:"";position:absolute;left:.3em;top:.12em;width:.28em;height:.55em;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}
.urow b{margin-left:auto;font-weight:600;font-variant-numeric:tabular-nums}
.iline{position:absolute;inset:0;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);font-size:.95em;font-variant-numeric:tabular-nums;white-space:nowrap;overflow:hidden}
.iline b{font-weight:600}
.sum{display:flex;justify-content:space-between;align-items:center;font-size:.95em;font-variant-numeric:tabular-nums;white-space:nowrap}
.sum.due{border-top:2px solid var(--ink);font-weight:700;font-size:1.1em}
.sum .k{font-size:.75em}
.sub{position:absolute;inset:0}
.sub .doc{position:absolute;inset:0;background:#FAFAF7;color:#2A2823;border-radius:.3em;box-shadow:0 12px 28px -16px rgba(0,0,0,.5);padding:1em .9em;font-family:"Caveat",cursive;font-size:1.3em;line-height:1.3}
.sub .doc i{display:block;height:2px;background:#D8D6D0;margin-top:.6em}
.sub .match{position:absolute;inset:0;display:flex;justify-content:space-between;align-items:center;gap:.8em;background:var(--card);border-radius:.7em;padding:0 .9em;font-size:.92em;white-space:nowrap;overflow:hidden}
.sub .match b{font-weight:600;font-variant-numeric:tabular-nums}
"""

def caps_html(caps):
    return '<div class="caps">' + "".join(f'<p{" class=on" if i==0 else ""}>{c}</p>' for i,c in enumerate(caps)) + '</div>'

def scene(id_, eyebrow, title, stage_html, caps, hint=False):
    return f'''<section class="wrap scene" id="{id_}">
  <div class="pin">
    <div class="sec-head"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2></div>
    <div class="stage">{stage_html}</div>
    {caps_html(caps)}
    {'<div class="hint">Scroll</div>' if hint else ''}
  </div>
</section>'''

# ---------- Scene 1: capture (from D) ----------
S1_HTML = '''<div class="frame act" data-a="frame">
  <div class="hd"><b>Field update · Mon, Sep 14</b><span>Crew 3 · 4th &amp; Main</span></div>
  <div class="lab" style="left:5.5%;top:21%">Photos</div><div class="lab" style="left:70.5%;top:21%">As-built</div>
  <div class="lab" style="left:5.5%;top:52%">Quantities</div><div class="lab" style="left:5.5%;top:75.5%">Notes</div>
  <div class="stamp act" data-a="stamp">Ready for approval</div>
</div>''' + "".join(scrap_html(n,k).replace('class="scrap"', f'class="scrap act" data-a="{n}"') for (n,k,_,_,_) in SCRAPS)

def s1_actors():
    A=[]
    for (n,k,s,e,d) in SCRAPS:
        A.append({"id":n,"kf":[{"at":d,"x":s[0],"y":s[1],"w":s[2],"h":s[3],"r":s[4]},{"at":.72,"x":e[0],"y":e[1],"w":e[2],"h":e[3],"r":0}],"skin":[d+(.72-d)*.55,d+(.72-d)*.95]})
    A.append({"id":"frame","kf":[{"at":.42,"x":18,"y":8,"w":64,"h":84,"o":0},{"at":.7,"x":18,"y":8,"w":64,"h":84,"o":1}]})
    A.append({"id":"stamp","kf":[{"at":.86,"o":0},{"at":.98,"o":1}]})
    return A
S1_CAPS=["Six things, five places, <b>one Monday</b>.","Clad gathers them into <b>a single field update</b>.","Photos, redline, quantities, notes. <b>Entered once.</b>"]

# ---------- Scene 2: manage ----------
S2_HTML = '''<div class="act panel2 board" data-a="board">
  <div class="hd"><b>Approvals · Maple Run fiber build</b><span>Week of Sep 14</span></div>
  <div class="cols">
    <div class="col"><h4>Submitted</h4><div class="ghost"></div><div class="ghost" style="height:15.5em;opacity:0"></div><div class="ghost"></div></div>
    <div class="col"><h4>Approved</h4><div class="ghost"></div><div class="ghost"></div></div>
    <div class="col"><h4>Invoiced</h4><div class="ghost"></div><div class="ghost"></div><div class="ghost"></div></div>
  </div>
  <div class="act mini" data-a="card">
    <div class="d">Mon Sep 14 · Crew 3</div><div class="t">4th &amp; Main</div>
    <div class="thumbs"><i></i><i></i><i></i></div>
    <div class="row" style="top:7.6em"><span>Fiber placed</span><span>1,000 FT</span></div>
    <div class="row" style="top:9.4em"><span>Hand holes</span><span>2 HH</span></div>
    <div class="total act" data-a="total"><span>Production</span><span>$5,900</span></div>
    <span class="tag tagpill act" data-a="tag">Approved</span>
    <div class="chip act" data-a="chip1" style="top:7.2em">× $4.20 / FT = $4,200</div>
    <div class="chip act" data-a="chip2" style="top:9.0em">× $850 / HH = $1,700</div>
  </div>
</div>
<div class="act tile" data-a="t1" style="width:30%;height:27%"><h5>Hand holes</h5><div class="big">108 <small>/ 500</small></div><div class="bar"><i class="act" data-a="b1"></i></div></div>
<div class="act tile" data-a="t2" style="width:28%;height:27%"><h5>Fiber placed</h5><div class="big">41,200 <small>/ 180,000 FT</small></div><div class="bar"><i class="act" data-a="b2"></i></div></div>
<div class="act tile chart" data-a="chart" style="width:60%;height:52%"><h5>Weekly production · HH</h5>
  <div class="bars"><i class="act" data-a="k0"></i><i class="act" data-a="k1"></i><i class="act" data-a="k2"></i><i class="act" data-a="k3"></i><i class="act" data-a="k4"></i><i class="act now" data-a="k5"></i></div>
  <div class="fc act" data-a="fc"><span>At this pace: <b>Dec 2</b> · Target: Nov 14</span><span>Close the gap: <b>+1 crew</b></span></div>
</div>'''

def s2_actors():
    A=[
     {"id":"board","kf":[{"at":0,"x":8,"y":6,"s":1},{"at":.56,"x":8,"y":6,"s":1},{"at":.74,"x":4,"y":8,"s":.34}]},
     {"id":"card","kf":[{"at":0,"x":3.2,"y":19},{"at":.1,"x":3.2,"y":19},{"at":.28,"x":35.6,"y":19}]},
     {"id":"tag","kf":[{"at":.3,"o":0},{"at":.36,"o":1}]},
     {"id":"chip1","kf":[{"at":.38,"x":115,"o":0},{"at":.5,"x":30,"o":1}]},
     {"id":"chip2","kf":[{"at":.42,"x":115,"o":0},{"at":.54,"x":30,"o":1}]},
     {"id":"total","kf":[{"at":.52,"o":0},{"at":.58,"o":1}]},
     {"id":"t1","kf":[{"at":.6,"x":36,"y":16,"o":0},{"at":.74,"x":36,"y":8,"o":1}]},
     {"id":"t2","kf":[{"at":.64,"x":68,"y":16,"o":0},{"at":.78,"x":68,"y":8,"o":1}]},
     {"id":"chart","kf":[{"at":.68,"x":36,"y":48,"o":0},{"at":.82,"x":36,"y":40,"o":1}]},
     {"id":"b1","kf":[{"at":.76,"w":0},{"at":.94,"w":21.6}]},
     {"id":"b2","kf":[{"at":.8,"w":0},{"at":.96,"w":22.9}]},
     {"id":"fc","kf":[{"at":.92,"o":0},{"at":1,"o":1}]},
    ]
    H=[38,52,45,60,70,64]
    for i,h in enumerate(H):
        A.append({"id":f"k{i}","kf":[{"at":.8+i*.02,"h":0},{"at":.92+i*.02,"h":h}]})
    return A
S2_CAPS=["Tuesday morning. Review the photos and quantities, <b>approve</b>.","Every quantity is priced from the contract. Monday is now <b>$5,900 of production</b>.","Wednesday's AT&amp;T check-in: <b>108 of 500</b> hand holes. The forecast says one more crew hits the date."]

# ---------- Scene 3: bill ----------
ROWS=[("Mon","1,000 FT fiber · 2 HH","$5,900"),("Tue","1,400 FT fiber","$5,880"),("Wed","3 HH","$2,550"),("Thu","800 FT fiber","$3,360")]
S3_HTML = '''<div class="act panel2 list" data-a="list"><div class="hd"><b>Approved</b><span>Week of Sep 14</span></div></div>
<div class="act panel2 inv" data-a="inv"><div class="hd"><b>Invoice #14 · AT&amp;T</b><span>Sep 14–18</span></div></div>''' + "".join(
 f'<div class="act" data-a="r{i}"><div class="urow"><i class="cb"></i><span>{d} · {q}</span><b>{amt}</b></div><div class="iline"><span>{d} Sep {14+i} · {q}</span><b>{amt}</b></div></div>' for i,(d,q,amt) in enumerate(ROWS)) + '''
<div class="act sum" data-a="s0"><span class="k">Subtotal</span><span>$17,690</span></div>
<div class="act sum" data-a="s1"><span class="k">Retainage · 10%</span><span>−$1,769</span></div>
<div class="act sum due" data-a="s2"><span>Due</span><span>$15,921</span></div>
<span class="act tagpill" data-a="qb">Synced to QuickBooks</span>
<div class="act sub" data-a="sub"><div class="doc">Ortiz Underground<br>Inv 0231 — $4,100<br><small>1400ft fiber, Tue</small><i></i><i></i></div><div class="match"><span>Sub bill · Ortiz Underground · $4,100</span><span class="tagpill">Matched to Tue</span></div></div>'''

def s3_actors():
    A=[
     {"id":"list","kf":[{"at":0,"x":4,"y":8,"o":1},{"at":.5,"x":4,"y":8,"o":1},{"at":.6,"x":4,"y":8,"o":.5}]},
     {"id":"inv","kf":[{"at":0,"x":44,"y":8,"o":1}]},
     {"id":"s0","kf":[{"at":.48,"x":46.5,"y":53,"w":47,"h":5,"o":0},{"at":.56,"x":46.5,"y":51,"w":47,"h":5,"o":1}]},
     {"id":"s1","kf":[{"at":.52,"x":46.5,"y":59,"w":47,"h":5,"o":0},{"at":.6,"x":46.5,"y":57,"w":47,"h":5,"o":1}]},
     {"id":"s2","kf":[{"at":.56,"x":46.5,"y":66,"w":47,"h":7,"o":0},{"at":.64,"x":46.5,"y":64,"w":47,"h":7,"o":1}]},
     {"id":"qb","kf":[{"at":.64,"x":46.5,"y":86,"o":0},{"at":.72,"x":46.5,"y":85,"o":1}]},
     {"id":"sub","kf":[{"at":.7,"x":72,"y":96,"w":18,"h":26,"r":6,"o":0},{"at":.76,"x":70,"y":92,"w":18,"h":26,"r":6,"o":1},{"at":.92,"x":46.5,"y":75,"w":47,"h":6,"r":0,"o":1}],"skin":[.84,.92]},
    ]
    for i in range(4):
        A.append({"id":f"r{i}","kf":[{"at":.08+i*.07,"x":6,"y":21+i*14,"w":30,"h":10.5},{"at":.3+i*.07,"x":46.5,"y":22+i*7,"w":47,"h":6}],"skin":[.14+i*.07,.28+i*.07]})
    return A
S3_CAPS=["Next Monday. Select the week's <b>approved updates</b>.","The invoice builds itself. <b>Retainage held.</b> Synced to QuickBooks.","Sub bills tie to the update they cover, so you <b>pay for what was built</b>."]

ENGINE = r"""
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
  function smooth(p,a,b){var t=clamp((p-a)/(b-a),0,1);return t*t*(3-2*t);}
  function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}
  var UNITS={x:'left',y:'top',w:'width',h:'height'};
  function apply(el,pose){
    for(var k in UNITS){ if(pose[k]!=null) el.style[UNITS[k]]=pose[k]+'%'; }
    if(pose.o!=null) el.style.opacity=pose.o;
    if(pose.r!=null||pose.s!=null) el.style.transform=(pose.r!=null?'rotate('+pose.r+'deg) ':'')+(pose.s!=null?'scale('+pose.s+')':'');
  }
  function poseAt(kf,p){
    if(p<=kf[0].at) return kf[0];
    if(p>=kf[kf.length-1].at) return kf[kf.length-1];
    for(var i=0;i<kf.length-1;i++){
      var a=kf[i],b=kf[i+1];
      if(p>=a.at&&p<=b.at){
        var t=ease((p-a.at)/(b.at-a.at)), out={};
        for(var k in a){ if(k==='at')continue; out[k]=(typeof a[k]==='number'&&typeof b[k]==='number')?a[k]+(b[k]-a[k])*t:a[k]; }
        return out;
      }
    }
    return kf[kf.length-1];
  }
  function Scene(id,actors,caps){
    var sec=document.getElementById(id); if(!sec) return;
    var stage=sec.querySelector('.stage');
    actors.forEach(function(a){ a.el=stage.querySelector('[data-a="'+a.id+'"]'); });
    var capEls=[].slice.call(sec.querySelectorAll('.caps p')), hint=sec.querySelector('.hint');
    function render(p){
      actors.forEach(function(a){
        if(!a.el) return;
        apply(a.el,poseAt(a.kf,p));
        if(a.skin){ var k=smooth(p,a.skin[0],a.skin[1]); a.el.children[0].style.opacity=1-k; a.el.children[1].style.opacity=k; }
      });
      var c=0; caps.forEach(function(th,i){ if(p>=th) c=i+1; });
      capEls.forEach(function(el,i){ el.classList.toggle('on',i===c); });
      if(hint) hint.style.opacity=p<.02?1:0;
    }
    var ticking=false;
    function measure(){
      ticking=false;
      var r=sec.getBoundingClientRect(), total=sec.offsetHeight-window.innerHeight;
      var p=clamp(-r.top/total,0,1);
      render(reduce?(p<.5?0:1):p);
    }
    window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(measure);}},{passive:true});
    window.addEventListener('resize',measure); measure();
  }
  window.Scene=Scene;
})();
"""

def build_e():
    return f'''<title>Clad Full Story</title>
{D_FONTS}
<style>{BASE_CSS}{D_CSS}{E_CSS}
.scrap .raw,.scrap .ui{{transition:none}}
.sub .doc,.sub .match{{}}
</style>
{nav()}
<section class="wrap hero">
  <div class="eyebrow">Field software for telecom, utility, and infrastructure contractors</div>
  <h1>Enter the work once. Everything else follows.</h1>
  <p>One field update becomes the approval, the priced production, the progress report, the invoice, and the sub bill match. Scroll to follow one Monday through the week.</p>
  <div class="row"><button class="btn accent" type="button">Book a demo</button><button class="btn ghost" type="button">Follow one update</button></div>
</section>
{scene("capture","01 · Capture","Intuitive tools to collect the data you need from the field.",S1_HTML,S1_CAPS,hint=True)}
{scene("manage","02 · Manage","Know where projects stand, and where they're heading.",S2_HTML,S2_CAPS)}
{scene("bill","03 · Bill","Eliminate over- and under-billing.",S3_HTML,S3_CAPS)}
{close()}
<script>{ENGINE}
Scene('capture',{json.dumps(s1_actors())},[.34,.8]);
Scene('manage',{json.dumps(s2_actors())},[.36,.6]);
Scene('bill',{json.dumps(s3_actors())},[.47,.73]);
</script>'''

open('e-full-story.html','w').write(build_e()); print('built e')
