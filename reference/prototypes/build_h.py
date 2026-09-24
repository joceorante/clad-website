import json
from build import BASE_CSS, FONTS, nav, close
from build_g import G_CSS

WW, WH = 320, 220   # world size in stage units

H_CSS = r"""
.zoom{position:relative;height:900vh}
.zpin{position:sticky;top:calc(env(safe-area-inset-top,0px));height:100vh}
.zstage{position:absolute;inset:0;overflow:hidden;container-type:size}
.zworld{position:absolute;left:0;top:0;width:320%;height:220%;transform-origin:0 0;font-size:clamp(9px,1.05cqw,12.5px)}
.zworld svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.act{position:absolute;transform-origin:top left}
/* raw inputs (neutral) */
.raw,.ui{position:absolute;inset:0;border-radius:.7em;overflow:hidden}
.ui{opacity:0}
.raw.photo{background:linear-gradient(160deg,var(--shape),var(--shape-2));box-shadow:0 14px 30px -18px rgba(0,0,0,.55)}
.raw .lab{position:absolute;left:.6em;bottom:.5em;font-family:var(--mono);font-size:.72em;letter-spacing:.06em;color:var(--bg);background:rgba(0,0,0,.45);border-radius:.4em;padding:.15em .5em}
.raw.page{background:var(--card);border:1px solid var(--line)}
.raw.page::after{content:"";position:absolute;left:22%;top:34%;width:56%;height:26%;border:2px solid var(--accent);border-radius:50% 45% 55% 40%}
.raw.page .lab{color:var(--muted);background:transparent;padding-left:0}
.raw.memo{background:var(--bg);border:1px solid var(--line);padding:.7em .9em .9em;font-size:1em;line-height:1.35}
.raw.memo .lab{position:static;display:block;color:var(--muted);background:transparent;padding:0;margin-bottom:.3em}
.raw.msg{background:var(--card);border-radius:1.2em 1.2em 1.2em .3em;padding:.6em .9em .9em;font-size:.98em;line-height:1.35}
.raw.msg .lab{position:static;display:block;color:var(--muted);background:transparent;padding:0;margin-bottom:.25em}
.ui.thumb{background:linear-gradient(160deg,var(--shape),var(--shape-2));border-radius:.6em}
.ui.thumb.pdf{background:var(--card);border:1px solid var(--line)}
.ui.thumb.pdf::after{content:"";position:absolute;left:18%;top:38%;width:64%;height:24%;border:2px solid var(--accent);border-radius:50% 45% 55% 40%}
.ui.fields{display:grid;grid-template-columns:1fr 1fr;gap:.6em;border-radius:0;overflow:visible}
.ui.fields div{border:1px solid var(--line);border-radius:.6em;padding:.5em .8em;background:var(--bg)}
.ui.fields small{display:block;font-family:var(--mono);font-size:.7em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.ui.fields b{font-weight:600;font-size:1.1em;font-variant-numeric:tabular-nums}
.ui.note{border:1px solid var(--line);border-radius:.6em;padding:.5em .8em;background:var(--bg);display:flex;align-items:center;gap:.6em;font-size:.95em}
.ui.note em{font-style:normal;font-family:var(--mono);font-size:.7em;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
/* hero update card */
.hero-card{overflow:hidden}
.hero-card .body{opacity:0}
.hero-card .stamp{position:absolute;right:1.2em;bottom:1.1em}
/* small cards */
.sc{background:var(--bg);border:1px solid var(--line);border-radius:.8em;padding:.6em .8em;box-shadow:0 10px 24px -16px rgba(0,0,0,.5);font-size:1.15em;line-height:1.25;white-space:nowrap;overflow:hidden}
.sc b{display:block;font-family:var(--mono);font-size:.72em;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:500}
.sc span{display:block;font-weight:600;font-size:.98em;margin-top:.15em}
.sc i{position:absolute;right:.7em;top:.7em;width:.7em;height:.7em;border-radius:50%;background:var(--ok,#2FA36B);opacity:0;transform:scale(.4);transition:opacity .35s,transform .45s cubic-bezier(.2,.8,.2,1.3)}
.sc.ap i{opacity:1;transform:scale(1)}
.sc.loc{border-color:color-mix(in srgb,var(--accent) 45%,var(--line))}.sc.loc b{color:var(--accent)}
.sc.mat b{color:#B7791F}.sc.ven b{color:#1FA48C}
/* manage panel */
.panel{background:var(--bg);border:1px solid var(--line);border-radius:1.4em;box-shadow:var(--shadow);padding:1.4em 1.6em}
.panel .hd{display:flex;justify-content:space-between;align-items:baseline;gap:1em;padding-bottom:.9em;border-bottom:1px solid var(--line);margin-bottom:1.1em}
.panel .hd b{font-weight:600;font-size:1.25em}
.panel .tiles{grid-template-columns:1fr 1fr;gap:1em}
.panel .tile{box-shadow:none;background:var(--card);border:0}
.panel .tile .bar i{width:0}
.panel .chart .bars{height:8em}
.panel .chart .bars i{height:0}
.panel .fc{opacity:0}
/* stacks */
.stk-lab{font-family:var(--mono);font-size:1.1em;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.stamp2{font-family:var(--mono);font-size:1.5em;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--accent);border:.14em solid var(--accent);border-radius:.4em;padding:.25em .6em;white-space:nowrap;background:color-mix(in srgb,var(--bg) 85%,transparent)}
.stamp2.paid{color:#2FA36B;border-color:#2FA36B}
.stamp2.soft{color:var(--muted);border-color:var(--line);font-weight:500}
.qb{font-family:var(--mono);font-size:1.05em;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);white-space:nowrap}
/* fixed caption bar */
.bar-fixed{position:absolute;left:0;right:0;bottom:0;padding:clamp(40px,7vh,80px) clamp(16px,4vw,40px) clamp(16px,2.5vh,24px);background:linear-gradient(to top,var(--bg) 55%,transparent);pointer-events:none}
.bar-fixed .in{max-width:1120px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:clamp(20px,4vw,64px);align-items:end}
.capset{grid-area:1/1/2/3;display:grid;grid-template-columns:subgrid;opacity:0;transform:translateY(8px);transition:opacity .4s,transform .4s}
.capset.on{opacity:1;transform:none}
.capset .eb{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.capset h3{font-size:clamp(20px,2vw,28px);margin-top:8px;letter-spacing:-.02em}
.capset p{color:var(--muted);font-size:15px;margin:8px 0 0;max-width:46ch}
.feat{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.feat div{border-top:1px solid var(--line);padding-top:10px}
.feat b{display:block;font-size:13px;font-weight:600}
.feat span{display:block;font-size:12px;color:var(--muted);margin-top:3px;line-height:1.4}
.zhint{position:absolute;left:50%;top:14px;transform:translateX(-50%);font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);transition:opacity .3s}
.crew{margin-top:clamp(28px,4vw,48px);aspect-ratio:16/7;background:var(--card);border-radius:22px;display:grid;place-items:center;color:var(--ph-text)}
.crew span{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--line);border-radius:999px;padding:6px 12px;background:var(--bg)}
@media (max-width:900px){.bar-fixed .in{grid-template-columns:1fr}.capset{grid-area:auto;grid-template-columns:1fr}.feat{display:none}.capset p{font-size:14px}}
"""

def P(x=None,y=None,w=None,h=None,**k):
    d={}
    if x is not None: d["x"]=round(x/WW*100,3)
    if y is not None: d["y"]=round(y/WH*100,3)
    if w is not None: d["w"]=round(w/WW*100,3)
    if h is not None: d["h"]=round(h/WH*100,3)
    d.update(k); return d

# ---- capture ----
CARD=(33,34,34)  # left, top, width (height auto)
SLOTS={"p1":(35.2,42.5,6.8,5.1),"p2":(42.6,42.5,6.8,5.1),"p3":(50,42.5,6.8,5.1),"pdf":(57.4,42.5,6.8,5.1),"qty":(35.2,49.4,29.2,5.6),"txt":(35.2,56.6,29.2,3.9)}
STARTS={"p1":(9,18,13,9.7,-7),"p2":(72,14,12,9,5),"p3":(77,48,12,9,-4),"pdf":(27,9,10,7.6,3),"qty":(10,50,16,8.2,4),"txt":(52,62,18,6.6,-3)}
DELAY={"p1":.04,"p2":.07,"p3":.10,"pdf":.12,"qty":.15,"txt":.18}
RAW_HTML={
 "p1":'<div class="raw photo"><span class="lab">Photo · 2:14 PM</span></div><div class="ui thumb"></div>',
 "p2":'<div class="raw photo" style="background:linear-gradient(200deg,var(--shape-2),var(--shape))"><span class="lab">Photo · 3:05 PM</span></div><div class="ui thumb"></div>',
 "p3":'<div class="raw photo" style="background:linear-gradient(20deg,var(--shape),var(--shape-2))"><span class="lab">Photo · 4:40 PM</span></div><div class="ui thumb"></div>',
 "pdf":'<div class="raw page"><span class="lab">Redline · PDF</span></div><div class="ui thumb pdf"></div>',
 "qty":'<div class="raw memo"><span class="lab">Note · Crew 3</span>1,000 ft fiber placed<br>2 HH set at 4th &amp; Main</div><div class="ui fields"><div><small>Fiber placed</small><b>1,000 FT</b></div><div><small>Hand holes</small><b>2 HH</b></div></div>',
 "txt":'<div class="raw msg"><span class="lab">Text · 4:55 PM</span>Both HH set, pics attached</div><div class="ui note"><em>Note</em>Both hand holes set at 4th &amp; Main. Photos attached.</div>',
}
HERO_CARD='''<div class="act card hero-card" data-a="hero">
  <div class="hd"><b>Field update · Mon, Sep 14</b><span class="k">Crew 3</span></div>
  <div class="body act" data-a="herobody">
    <div class="thumbs"><i></i><i></i><i></i><i class="pdf"></i></div>
    <div class="fields"><div><small>Fiber placed</small><b>1,000 FT</b></div><div><small>Hand holes</small><b>2 HH</b></div></div>
    <div class="note"><em>Note</em>Both hand holes set at 4th &amp; Main. Photos attached.</div>
  </div>
  <span class="stamp tagpill act" data-a="stamp">Ready for approval</span>
</div>'''

# ---- manage: field of small cards ----
SMALL=[
 # x,y,label,value,type
 (8,14,"Mon · Crew 1","620 FT fiber",""),(8,24,"Mon · Crew 2","1 HH · 300 FT",""),(8,34,"Locate · 5th St","Cleared Thu","loc"),
 (8,64,"Tue · Crew 3","1,400 FT fiber",""),(8,74,"Tue · Crew 1","2 HH",""),(8,84,"Material","2 HH pulled · yard","mat"),
 (25,10,"Tue · Crew 2","900 FT fiber",""),(43,8,"Wed · Crew 3","3 HH",""),(61,10,"Wed · Crew 1","1,100 FT fiber",""),
 (74,20,"Wed · Crew 2","Splice · 48 ct",""),(74,30,"Locate · Maple Run","Requested","loc"),(74,66,"Thu · Crew 3","800 FT fiber",""),
 (74,76,"Thu · Crew 1","2 HH · 400 FT",""),(74,86,"Vendor","Ortiz Underground","ven"),(25,90,"Thu · Crew 2","1,300 FT fiber",""),
 (43,92,"Fri · Crew 3","3 HH · 800 FT",""),(61,90,"Fri · Crew 1","700 FT fiber",""),(92,8,"Fri · Crew 2","Restoration",""),
 (92,50,"Material","Fiber reel · 6,000 FT","mat"),(92,92,"Locate · Hwy 9","Cleared Mon","loc"),
]
SC_W, SC_H = 15, 6.6
STACKS=[(84,60),(114,60),(144,60),(174,60)]
PANEL='''<div class="act panel" data-a="panel">
  <div class="hd"><b>Maple Run · production</b><span class="k">Week of Sep 14</span></div>
  <div class="tiles"><div class="tile"><h5>Hand holes</h5><div class="big">108 <small>/ 500</small></div><div class="bar"><i class="act" data-a="b1"></i></div></div>
  <div class="tile"><h5>Fiber placed</h5><div class="big">41,200 <small>/ 180k FT</small></div><div class="bar"><i class="act" data-a="b2"></i></div></div></div>
  <div class="chart" style="margin-top:1em"><span class="k">Weekly production · HH</span>
    <div class="bars"><i class="act" data-a="k0"></i><i class="act" data-a="k1"></i><i class="act" data-a="k2"></i><i class="act" data-a="k3"></i><i class="act" data-a="k4"></i><i class="act now" data-a="k5"></i></div>
    <div class="fc act" data-a="fc"><span>At this pace: <b>Dec 2</b> · Target: Nov 14</span><span>Close the gap: <b>+1 crew</b></span></div></div>
</div>'''
INVOICE='''<div class="act card inv" data-a="invoice">
  <div class="hd"><b>Invoice #14 · AT&amp;T</b><span class="k">Sep 14–18</span></div>
  <div class="iline"><span>Mon · 1,000 FT fiber, 2 HH</span><b>$5,900</b></div><div class="iline"><span>Tue · 1,400 FT fiber</span><b>$5,880</b></div><div class="iline"><span>Wed · 3 HH</span><b>$2,550</b></div><div class="iline"><span>Thu · 800 FT fiber</span><b>$3,360</b></div>
  <div class="sum"><span class="k">Subtotal</span><span>$17,690</span></div><div class="sum"><span class="k">Retainage · 10%</span><span>−$1,769</span></div><div class="sum due"><span>Due</span><span>$15,921</span></div>
  <div class="foot" style="display:flex;justify-content:space-between;align-items:center;margin-top:.8em"><span class="k">3 sub bills matched</span><span class="tagpill">Synced to QuickBooks</span></div>
</div>'''

CAMERA=[  # (p, cx, cy, scale)
 (0.00, 50, 54, 1.0),(0.34, 50, 54, 1.0),
 (0.44, 96, 74, 0.5),(0.68, 96, 74, 0.5),
 (0.80, 182, 70, 0.44),(1.00, 182, 70, 0.44),
]

CAPS=[
 (0.0,"01 · Capture","The crew does the work. Clad keeps the record.","Photos, the redline, quantities, and a note leave the field the way they always have. Clad turns them into one field update, ready for approval.",
  [("Digital as-builts","PDF or GIS redlines tied to the production they document."),("Production tracking","Quantities logged against the project budget, offline first."),("Custom forms","Photos, bore logs, damages, whatever the job needs.")]),
 (0.36,"02 · Manage","Every update feeds the same picture.","Zoom out and Monday is one of dozens: every crew, every day, plus locates and material pulls. Approve them, and progress, forecast, and schedule update themselves.",
  [("Insights","Production, spend, and revenue across all your projects."),("Forecasting","The production you need to finish on time, and what closes the gap."),("Schedules","Milestones and locates against the plan.")]),
 (0.72,"03 · Bill","The week's updates become the invoice.","Approved updates gather by week. Each stack becomes an invoice, syncs to QuickBooks, and sub bills match against the updates they cover.",
  [("Production to invoice","Invoices built from approved work. Sub bills tied to production."),("Retainage","Tracked and released without a side spreadsheet."),("QuickBooks sync","Nothing re-keyed. More ERPs coming.")]),
]

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
    for(var i=0;i<kf.length-1;i++){ var a=kf[i],b=kf[i+1];
      if(p>=a.at&&p<=b.at){ var t=ease((p-a.at)/(b.at-a.at)), out={};
        for(var k in a){ if(k==='at')continue; out[k]=(typeof a[k]==='number'&&typeof b[k]==='number')?a[k]+(b[k]-a[k])*t:a[k]; }
        return out; } }
    return kf[kf.length-1];
  }
  window.__zoom=function(cfg){
    var sec=document.getElementById('zoom'), stage=sec.querySelector('.zstage'), world=sec.querySelector('.zworld'), svg=sec.querySelector('svg'), hint=sec.querySelector('.zhint');
    var actors=cfg.actors; actors.forEach(function(a){ a.el=world.querySelector('.act[data-a="'+a.id+'"]'); });
    var smalls=[].slice.call(world.querySelectorAll('.sc'));
    var caps=[].slice.call(sec.querySelectorAll('.capset'));
    var edges=[]; cfg.edges.forEach(function(e){ var el=document.createElementNS('http://www.w3.org/2000/svg','path'); el.setAttribute('class','edge'); el.setAttribute('pathLength','1'); el._e=e; svg.appendChild(el); edges.push(el); });
    function layoutEdges(){ var sw=stage.clientWidth, sh=stage.clientHeight; svg.setAttribute('viewBox','0 0 '+(cfg.WW/100*sw)+' '+(cfg.WH/100*sh));
      edges.forEach(function(el){ var e=el._e, x1=e[0]/100*sw,y1=e[1]/100*sh,x2=e[2]/100*sw,y2=e[3]/100*sh, dx=x2-x1, dy=y2-y1;
        el.setAttribute('d','M'+x1+' '+y1+' Q'+((x1+x2)/2-dy*.15)+' '+((y1+y2)/2+dx*.15)+' '+x2+' '+y2); }); }
    function camera(p){ var C=cfg.camera; if(p<=C[0][0]) return C[0]; for(var i=0;i<C.length-1;i++){ var a=C[i],b=C[i+1]; if(p>=a[0]&&p<=b[0]){ var t=smooth(p,a[0],b[0]); return [p,a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t,a[3]+(b[3]-a[3])*t]; } } return C[C.length-1]; }
    function render(p){
      var c=camera(p), sw=stage.clientWidth, sh=stage.clientHeight, s=c[3];
      world.style.transform='translate('+(sw/2-c[1]/100*sw*s)+'px,'+(sh/2-c[2]/100*sh*s)+'px) scale('+s+')';
      actors.forEach(function(a){ if(!a.el) return; apply(a.el,poseAt(a.kf,p));
        if(a.skin){ var k=smooth(p,a.skin[0],a.skin[1]); a.el.children[0].style.opacity=1-k; a.el.children[1].style.opacity=k; } });
      smalls.forEach(function(el){ el.classList.toggle('ap', p>=+el.dataset.ap); });
      edges.forEach(function(el){ el.classList.toggle('on', p>=el._e[4]); });
      var ci=0; cfg.capAt.forEach(function(th,i){ if(p>=th) ci=i; }); caps.forEach(function(el,i){ el.classList.toggle('on',i===ci); });
      hint.style.opacity=p<.02?1:0;
    }
    var ticking=false;
    function measure(){ ticking=false; var r=sec.getBoundingClientRect(), total=sec.offsetHeight-window.innerHeight; var p=clamp(-r.top/total,0,1); render(reduce?(p<.5?0:1):p); }
    window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(measure);}},{passive:true});
    window.addEventListener('resize',function(){layoutEdges();measure();}); layoutEdges(); measure();
  };
})();
"""

def build_h():
    actors=[]; html=""
    # capture scraps
    for sid,(sx,sy,sw,sh,sr) in STARTS.items():
        ex,ey,ew,eh=SLOTS[sid]; d=DELAY[sid]
        actors.append({"id":sid,"kf":[P(sx,sy,sw,sh,at=d,r=sr,o=1),P(ex,ey,ew,eh,at=.28,r=0,o=1),P(ex,ey,ew,eh,at=.33,r=0,o=1),P(ex,ey,ew,eh,at=.37,r=0,o=0)],"skin":[d+(.28-d)*.55,d+(.28-d)*.95]})
        html+=f'<div class="act" data-a="{sid}">{RAW_HTML[sid]}</div>'
    # hero card: frame fades in, static body appears as scraps fade, then joins stack 1 in bill
    cx,cy,cw=CARD
    sx0,sy0=STACKS[0]
    actors.append({"id":"hero","kf":[P(cx,cy,cw,at=.2,o=0,s=1),P(cx,cy,cw,at=.3,o=1,s=1),P(cx,cy,cw,at=.72,o=1,s=1),P(sx0-SC_W/2,sy0-SC_H/2,cw,at=.84,o=1,s=round(SC_W/cw,3))]})
    actors.append({"id":"herobody","kf":[{"at":.33,"o":0},{"at":.37,"o":1}]})
    actors.append({"id":"stamp","kf":[{"at":.30,"o":0},{"at":.34,"o":1},{"at":.5,"o":1},{"at":.56,"o":0}]})
    html+=HERO_CARD
    # small cards
    for i,(x,y,lab,val,typ) in enumerate(SMALL):
        pop=.36+(i%10)*.012+(i//10)*.02
        k=i%4; j=i//4
        sx,sy=STACKS[k]
        actors.append({"id":f"s{i}","kf":[P(x,y,SC_W,SC_H,at=pop,o=0,s=.85),P(x,y,SC_W,SC_H,at=pop+.05,o=1,s=1),P(x,y,SC_W,SC_H,at=.72,o=1,s=1),P(sx-SC_W/2+j*.7,sy-SC_H/2+j*.9+1,SC_W,SC_H,at=.84,o=1,s=1)]})
        html+=f'<div class="act sc {typ}" data-a="s{i}" data-ap="{pop+.14:.3f}"><b>{lab}</b><span>{val}</span><i></i></div>'
    # manage panel
    actors.append({"id":"panel","kf":[P(118,16,70,at=.42,o=0),P(118,10,70,at=.5,o=1)]})
    actors.append({"id":"b1","kf":[{"at":.52,"w":0},{"at":.64,"w":21.6}]})
    actors.append({"id":"b2","kf":[{"at":.55,"w":0},{"at":.66,"w":22.9}]})
    for i,h in enumerate([38,52,45,60,70,64]):
        actors.append({"id":f"k{i}","kf":[{"at":.54+i*.015,"h":0},{"at":.64+i*.015,"h":h}]})
    actors.append({"id":"fc","kf":[{"at":.64,"o":0},{"at":.68,"o":1}]})
    html+=PANEL
    # bill: stack labels, stamps, invoice
    weeks=["Week of Sep 14","Week of Sep 21","Week of Sep 28","Week of Oct 5"]
    stamps=[("Invoiced · #14",""),("Invoiced · #15",""),("Sent",""),("Draft","soft")]
    for k,(sx,sy) in enumerate(STACKS):
        actors.append({"id":f"w{k}","kf":[P(sx-SC_W/2,sy-SC_H/2-6,at=.82,o=0),P(sx-SC_W/2,sy-SC_H/2-5,at=.86,o=1)]})
        html+=f'<div class="act stk-lab" data-a="w{k}">{weeks[k]}</div>'
        actors.append({"id":f"st{k}","kf":[P(sx-8,sy+1,at=.86+k*.02,o=0,r=-8,s=1.3),P(sx-8,sy+1,at=.9+k*.02,o=1,r=-8,s=1)]})
        html+=f'<div class="act stamp2 {stamps[k][1]}" data-a="st{k}">{stamps[k][0]}</div>'
    for k in (0,1):
        sx,sy=STACKS[k]
        actors.append({"id":f"pd{k}","kf":[P(sx-4,sy+7,at=.94+k*.02,o=0,r=6,s=1.3),P(sx-4,sy+7,at=.97+k*.02,o=1,r=6,s=1)]})
        html+=f'<div class="act stamp2 paid" data-a="pd{k}">Paid</div>'
        actors.append({"id":f"qb{k}","kf":[P(sx-SC_W/2,sy+13,at=.92+k*.02,o=0),P(sx-SC_W/2,sy+12,at=.95+k*.02,o=1)]})
        html+=f'<div class="act qb" data-a="qb{k}">Synced · QuickBooks</div>'
    actors.append({"id":"invoice","kf":[P(205,26,84,at=.8,o=0),P(205,20,84,at=.88,o=1)]})
    html+=INVOICE
    # threads: a few small cards -> panel (manage), stack 1 -> invoice (bill)
    edges=[]
    for i in (7,8,9,10,17,18):
        x,y=SMALL[i][0],SMALL[i][1]
        edges.append([x+SC_W,y+SC_H/2,118,10+8+i*2,.5+ (i%6)*.015])
    edges.append([STACKS[0][0]+SC_W/2,STACKS[0][1],205,40,.88])
    edges.append([STACKS[1][0]+SC_W/2,STACKS[1][1],205,44,.9])
    caps_html=""
    for i,(t,eb,h,p,feats) in enumerate(CAPS):
        f="".join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in feats)
        caps_html+=f'<div class="capset{" on" if i==0 else ""}"><div><div class="eb">{eb}</div><h3>{h}</h3><p>{p}</p></div><div class="feat">{f}</div></div>'
    cfg={"WW":WW,"WH":WH,"actors":actors,"edges":edges,"camera":CAMERA,"capAt":[c[0] for c in CAPS]}
    return f'''<title>Clad Zoom Story</title>
{FONTS}
<style>{BASE_CSS}{G_CSS}{H_CSS}</style>
{nav()}
<section class="wrap hero">
  <div class="eyebrow">Field software for telecom, utility, and infrastructure contractors</div>
  <h1>Someone does the work. Clad keeps the record.</h1>
  <p>One field update becomes the approval, the forecast, the invoice, and the sub bill match. Scroll to follow a Monday from the trench to QuickBooks.</p>
  <div class="row"><button class="btn accent" type="button">Book a demo</button><button class="btn ghost" type="button">Follow one update</button></div>
  <div class="crew"><span>Photo · crew placing fiber</span></div>
</section>
<section class="zoom" id="zoom">
  <div class="zpin"><div class="zstage">
    <div class="zworld"><svg aria-hidden="true"></svg>{html}</div>
    <div class="zhint">Scroll</div>
    <div class="bar-fixed"><div class="in">{caps_html}</div></div>
  </div></div>
</section>
{close()}
<script>{ENGINE}
__zoom({json.dumps(cfg)});
</script>'''

open('h-zoom.html','w').write(build_h()); print('built h')
