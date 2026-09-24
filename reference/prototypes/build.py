BASE_CSS = r"""
:root{
  --bg:#FFFFFF; --ink:#2A2823; --muted:#5E5B54; --line:#E8E7E3;
  --accent:#6D6AF0; --accent-ink:#FFFFFF;
  --card:#F2F2F0; --shape:#DCDCDA; --shape-2:#CFCFCC; --ph-text:#6E6B64;
  --shadow:0 40px 70px -30px rgba(30,28,20,.35),0 0 0 1px rgba(30,28,20,.05);
  --body:"Inter",system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#131314; --ink:#ECEBE7; --muted:#A5A29B; --line:#2A2A2C; --accent:#8A88FF;
    --card:#1F1F21; --shape:#2E2E31; --shape-2:#3A3A3E; --ph-text:#8E8B84;
    --shadow:0 40px 70px -30px rgba(0,0,0,.8),0 0 0 1px rgba(255,255,255,.06);
  }
}
:root[data-theme="dark"]{
  --bg:#131314; --ink:#ECEBE7; --muted:#A5A29B; --line:#2A2A2C; --accent:#8A88FF;
  --card:#1F1F21; --shape:#2E2E31; --shape-2:#3A3A3E; --ph-text:#8E8B84;
  --shadow:0 40px 70px -30px rgba(0,0,0,.8),0 0 0 1px rgba(255,255,255,.06);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding-inline:clamp(16px,4vw,40px)}
h1,h2,h3{margin:0;text-wrap:balance;letter-spacing:-.025em;line-height:1.1;font-weight:700}
button{font:inherit;cursor:pointer}
a{color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;color:var(--accent)}
.mono{font-family:var(--mono);font-size:11px;letter-spacing:.06em;font-weight:500}
.nav{display:flex;align-items:center;justify-content:space-between;padding-block:22px;gap:16px}
.logo{font-weight:700;font-size:22px;letter-spacing:-.03em;display:flex;align-items:center;gap:9px}
.logo i{width:18px;height:18px;background:var(--accent);display:inline-block;border-radius:4px 4px 4px 10px}
.nav-links{display:flex;gap:26px;font-size:15px;color:var(--muted)}
.nav-links a{text-decoration:none}
.btn{background:var(--ink);color:var(--bg);border:0;border-radius:8px;padding:10px 16px;font-weight:600;font-size:15px}
.btn.accent{background:var(--accent);color:var(--accent-ink)}
.btn.ghost{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--line)}
@media (max-width:700px){.nav-links{display:none}}
.hero{padding-block:clamp(40px,7vw,96px) clamp(32px,5vw,64px);text-align:center}
.hero h1{font-size:clamp(38px,5.6vw,72px);margin:14px auto 0;max-width:18ch}
.hero p{font-size:clamp(17px,1.5vw,20px);color:var(--muted);max-width:52ch;margin:20px auto 0}
.hero .row{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px;justify-content:center}
.ph{position:relative;background:var(--card);border-radius:22px;box-shadow:var(--shadow);display:grid;place-items:center;overflow:hidden}
.ph .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:500;color:var(--ph-text);background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:6px 12px;position:relative;z-index:1}
/* steps + sticky stage */
.story{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.35fr);gap:clamp(24px,5vw,72px);padding-block:clamp(16px,3vw,40px) clamp(24px,4vw,48px)}
.steps{display:flex;flex-direction:column}
.step{min-height:80vh;display:flex;flex-direction:column;justify-content:center;padding-block:8vh;opacity:.28;transition:opacity .4s}
.step.is-current{opacity:1}
.step .k{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;color:var(--muted)}
.step.is-current .k{color:var(--accent)}
.step h3{font-size:clamp(26px,2.6vw,36px);margin-top:12px;letter-spacing:-.02em}
.step p{font-size:16px;color:var(--muted);max-width:40ch;margin:14px 0 0}
.stage-wrap{position:sticky;top:calc(6vh + env(safe-area-inset-top,0px));height:88vh;align-self:start}
.stage{position:relative;height:100%}
.sec-head{text-align:center;max-width:760px;margin:0 auto;padding-top:clamp(40px,7vw,96px)}
.sec-head h2{font-size:clamp(28px,3.6vw,44px);margin-top:12px}
.sec-head p{color:var(--muted);font-size:17px;margin:14px auto 0;max-width:52ch}
.close{border-top:1px solid var(--line);margin-top:clamp(56px,9vw,120px);padding-block:clamp(48px,8vw,96px);text-align:center}
.close h2{font-size:clamp(30px,4vw,48px);max-width:20ch;margin:0 auto}
.close p{color:var(--muted);max-width:48ch;margin:14px auto 0}
.close .btn{margin-top:24px}
footer{padding-block:24px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
@media (max-width:900px){
  .story{grid-template-columns:1fr;gap:0}
  .stage-wrap{order:-1;position:sticky;top:calc(8px + env(safe-area-inset-top,0px));height:48vh;z-index:2;background:var(--bg);padding-bottom:10px}
  .step{min-height:62vh;padding-block:6vh}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition-duration:.01ms!important;transition-delay:0s!important;animation:none!important}}
"""

FONTS = '<meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">'

def nav():
    return '''<header class="wrap nav">
  <div class="logo"><i></i>Clad</div>
  <nav class="nav-links"><a href="#story">How it works</a><a href="#">Pricing</a><a href="#">Log in</a></nav>
  <button class="btn accent" type="button">Book a demo</button>
</header>'''

def close():
    return '''<section class="wrap close">
  <h2>From the field to the invoice, on one record.</h2>
  <p>See Clad on one of your live projects.</p>
  <button class="btn accent" type="button">Book a demo</button>
</section>
<footer class="wrap"><span>Clad · Prototype</span><span>Telecom · Utility · Infrastructure</span></footer>'''

STEP_JS = r"""
function stepDriver(steps, onChange){
  var current=-1, ticking=false;
  function measure(){
    ticking=false; var mid=window.innerHeight*0.5, best=0, bestD=Infinity;
    steps.forEach(function(s,k){var r=s.getBoundingClientRect();var d=Math.abs((r.top+r.bottom)/2-mid);if(d<bestD){bestD=d;best=k;}});
    if(best!==current){current=best; steps.forEach(function(s,k){s.classList.toggle('is-current',k===best);}); onChange(best);}
  }
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(measure);}},{passive:true});
  window.addEventListener('resize',measure); measure();
}
"""

# ---------------------------------------------------------------- A: the loop
A_STEPS = [
 ("Mon · Field","1,000 feet of fiber and two hand holes go in.","The crew logs quantities, photos, and the redline from the truck. That's the record. Everything after this reads from it."),
 ("Tue · Office","Someone checks it.","Tuesday morning you open the update, look at the photos and quantities, and approve. Nothing gets re-typed."),
 ("Wed · AT&T check-in","AT&T asks how far along you are.","Of 500 planned hand holes, 108 are in. Percent complete comes straight from approved production, not a spreadsheet you built the night before."),
 ("Wed · Forecast","You're behind.","Clad's forecast shows the gap to the target date and what closes it. In this case, one more crew member."),
 ("Next Mon · Invoice","Time to bill last week.","Select the week's approved updates. Clad builds the invoice and syncs it to QuickBooks."),
 ("Next Mon · Sub bills","Sub bills land in your inbox.","Clad ties each bill to the update it covers, so you pay for what was built and nothing else."),
 ("Fri · Report","Your boss wants all five projects.","One production report across every job you manage. Same record, one more view."),
]
A_MOCKS = ["Field update","Approval","Progress · 108 / 500 HH","Forecast","Invoice","Sub bill matching","Portfolio report"]
A_STAMPS = ["Approved · Tue 8:12 AM","Counted · 108 / 500 HH","In forecast · gap: 1 crew","Invoice #14 · synced to QuickBooks","Matched · 3 sub bills","In 5-project report"]
A_DAYS = ["Mon","Tue","Wed","Mon","Fri"]
A_STEP_TO_DAY = [0,1,2,2,3,3,4]

A_CSS = r"""
.stage.loop{display:flex;flex-direction:column;gap:14px}
.days{display:flex;align-items:center;gap:8px;position:relative;height:28px}
.days .track{position:absolute;left:0;right:0;top:50%;height:2px;background:var(--line);transform:translateY(-50%)}
.days .fill{position:absolute;left:0;top:50%;height:2px;background:var(--accent);transform:translateY(-50%);width:0;transition:width .6s cubic-bezier(.2,.7,.2,1)}
.days .d{position:relative;flex:1;display:flex;justify-content:center}
.days .d span{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);background:var(--bg);padding:4px 8px;border-radius:999px;border:1px solid var(--line);transition:color .3s,border-color .3s}
.days .d.on span{color:var(--ink);border-color:var(--accent)}
.days .d.past span{color:var(--muted);border-color:var(--accent)}
.frames{position:relative;flex:1;min-height:0}
.panel{position:absolute;inset:0;opacity:0;transform:translateY(24px) scale(.985);transition:opacity .5s,transform .6s cubic-bezier(.2,.7,.2,1);pointer-events:none}
.panel.is-active{opacity:1;transform:none}
.panel .ph{position:absolute;inset:0}
.record{position:absolute;left:clamp(12px,3%,28px);bottom:clamp(12px,3%,28px);width:min(300px,78%);background:var(--bg);border:1px solid var(--line);border-radius:14px;box-shadow:0 20px 40px -20px rgba(0,0,0,.35);padding:14px 16px;z-index:3;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.record .rk{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.record .rt{font-weight:600;font-size:15px;margin-top:4px;letter-spacing:-.01em}
.record .rs{color:var(--muted);font-size:12px;margin-top:2px}
.stamps{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
.stamps li{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11px;letter-spacing:.02em;color:var(--ink);opacity:0;transform:translateY(8px);transition:opacity .4s,transform .4s;max-height:0;overflow:hidden}
.stamps li::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent);flex:none}
.stamps li.on{opacity:1;transform:none;max-height:24px}
.stamps li.now{color:var(--accent)}
@media (max-width:900px){.record{width:min(260px,70%);padding:10px 12px}.record .rt{font-size:13px}.stamps li{font-size:10px}}
"""

def build_a():
    steps = "".join(f'<article class="step{" is-current" if i==0 else ""}"><div class="k">{k}</div><h3>{h}</h3><p>{p}</p></article>' for i,(k,h,p) in enumerate(A_STEPS))
    panels = "".join(f'<div class="panel{" is-active" if i==0 else ""}"><div class="ph"><span class="lbl">Mock · {m}</span></div></div>' for i,m in enumerate(A_MOCKS))
    days = "".join(f'<div class="d{" on" if i==0 else ""}"><span>{d}</span></div>' for i,d in enumerate(A_DAYS))
    stamps = "".join(f'<li>{s}</li>' for s in A_STAMPS)
    return f'''<title>Clad One Update</title>
{FONTS}
<style>{BASE_CSS}{A_CSS}</style>
{nav()}
<section class="wrap hero">
  <div class="eyebrow">Field software for telecom, utility, and infrastructure contractors</div>
  <h1>Enter the work once. Everything else follows.</h1>
  <p>One field update becomes the approval, the progress report, the forecast, the invoice, and the sub bill match. Scroll to follow a single Monday through the week.</p>
  <div class="row"><button class="btn accent" type="button">Book a demo</button><button class="btn ghost" type="button">Follow one update</button></div>
</section>
<section class="wrap story" id="story">
  <div class="steps">{steps}</div>
  <div class="stage-wrap"><div class="stage loop">
    <div class="days"><div class="track"></div><div class="fill" id="fill"></div>{days}</div>
    <div class="frames">
      {panels}
      <div class="record" id="record">
        <div class="rk">One update · Mon</div>
        <div class="rt">1,000 FT fiber · 2 hand holes</div>
        <div class="rs">Crew 3 · 6 photos · redline attached</div>
        <ul class="stamps" id="stamps">{stamps}</ul>
      </div>
    </div>
  </div></div>
</section>
{close()}
<script>
(function(){{
{STEP_JS}
  var steps=[].slice.call(document.querySelectorAll('.step'));
  var panels=[].slice.call(document.querySelectorAll('.panel'));
  var days=[].slice.call(document.querySelectorAll('.days .d'));
  var stamps=[].slice.call(document.querySelectorAll('#stamps li'));
  var fill=document.getElementById('fill');
  var map={A_STEP_TO_DAY};
  stepDriver(steps,function(i){{
    panels.forEach(function(p,k){{p.classList.toggle('is-active',k===i);}});
    var d=map[i];
    days.forEach(function(el,k){{el.classList.toggle('on',k===d);el.classList.toggle('past',k<d);}});
    fill.style.width=(d/(days.length-1)*100)+'%';
    stamps.forEach(function(s,k){{s.classList.toggle('on',k<i);s.classList.toggle('now',k===i-1);}});
  }});
}})();
</script>'''

# ---------------------------------------------------------------- B: admin's desk
B_STEPS = [
 ("Mon · Field","1,000 feet of fiber and two hand holes go in.","Without Clad: photos in a group chat, a marked-up PDF, a paper quantity sheet. With Clad: one update, entered once, from the truck."),
 ("Tue · Office","Someone has to check it.","Without: the admin re-types quantities into the tracking sheet and files the photos. With: you look at the photos and quantities and approve."),
 ("Wed · AT&T check-in","AT&T asks how far along you are.","Without: build the percent complete by hand in a slide. With: 108 of 500 hand holes, read straight from approved production."),
 ("Next Mon · Invoice","Time to bill last week.","Without: rebuild the quantities in QuickBooks, attach the photos, email it. With: select the week's updates. The invoice builds and syncs."),
 ("Next Mon · Sub bills","Sub bills land in your inbox.","Without: cross-check each PDF against the sheet. With: each bill ties to the update it covers."),
 ("Fri · Report","Your boss wants all five projects.","Without: five spreadsheets and a deck. With: one production report."),
]
# tiles: (step, kind, label, x%, y%, rot)
B_TILES = [
 (0,"photo","Group chat photos",4,6,-6),(0,"doc","Marked-up PDF",38,2,4),(0,"doc","Paper quantity sheet",66,10,-3),
 (1,"sheet","Tracking spreadsheet",8,34,3),(1,"photo","Photo folder",60,36,7),
 (2,"sheet","Progress slide",30,48,-5),
 (3,"doc","QuickBooks invoice",2,60,5),(3,"doc","Email to AT&T",50,58,-4),
 (4,"doc","Sub bill PDFs ×3",70,64,6),(4,"sheet","Reconciliation sheet",22,72,-2),
 (5,"sheet","5 spreadsheets",0,84,4),(5,"sheet","Update deck",48,82,-6),
]
B_REENTRY = [0,2,3,5,7,9]
B_STAMPS = ["Approved · Tue 8:12 AM","108 / 500 HH · shared","Invoice #14 · synced to QuickBooks","3 sub bills · matched","In 5-project report"]

B_CSS = r"""
.stage.split{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.side{position:relative;background:var(--card);border-radius:22px;box-shadow:var(--shadow);overflow:hidden;display:flex;flex-direction:column}
.side header{padding:14px 16px;display:flex;justify-content:space-between;align-items:baseline;gap:8px;border-bottom:1px solid var(--line);position:relative;z-index:2;background:var(--card)}
.side header b{font-size:13px;font-weight:600}
.side header .cnt{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);text-align:right;transition:color .3s}
.side.old header .cnt.hot{color:var(--ink)}
.side.new header b{color:var(--accent)}
.body{position:relative;flex:1}
.pile{position:absolute;inset:12px}
.tile{position:absolute;left:var(--x);top:var(--y);transform:rotate(var(--r)) translateY(30px) scale(.9);opacity:0;background:var(--shape);border-radius:8px;display:flex;align-items:flex-end;padding:8px;font-family:var(--mono);font-size:10px;letter-spacing:.02em;color:var(--ph-text);box-shadow:0 10px 24px -14px rgba(0,0,0,.5);transition:opacity .45s,transform .55s cubic-bezier(.2,.8,.2,1.1)}
.tile.on{opacity:1;transform:rotate(var(--r))}
.tile.photo{width:26%;aspect-ratio:1}
.tile.doc{width:22%;aspect-ratio:3/4}
.tile.sheet{width:34%;aspect-ratio:4/2.6}
.tile.photo::before{content:"";position:absolute;inset:6px 6px auto 6px;height:45%;background:var(--shape-2);border-radius:4px}
.tile.doc::before,.tile.sheet::before{content:"";position:absolute;inset:8px 8px auto 8px;height:5px;background:var(--shape-2);border-radius:2px;box-shadow:0 10px 0 var(--shape-2),0 20px 0 var(--shape-2)}
.one{position:absolute;inset:0;display:grid;place-items:center;padding:16px}
.rec{width:min(300px,92%);background:var(--bg);border:1px solid var(--line);border-radius:14px;box-shadow:0 20px 40px -20px rgba(0,0,0,.35);padding:14px 16px}
.rec .rk{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.rec .rt{font-weight:600;font-size:15px;margin-top:4px}
.rec .rs{color:var(--muted);font-size:12px;margin-top:2px}
.stamps{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
.stamps li{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11px;color:var(--ink);opacity:0;transform:translateY(8px);transition:opacity .4s,transform .4s;max-height:0;overflow:hidden}
.stamps li::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent);flex:none}
.stamps li.on{opacity:1;transform:none;max-height:24px}
.stamps li.now{color:var(--accent)}
.side.new .ghost{position:absolute;inset:0;display:grid;place-items:center;pointer-events:none}
.side.new .ghost span{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ph-text);border:1px solid var(--line);background:var(--bg);border-radius:999px;padding:6px 12px;transform:translateY(120px)}
@media (max-width:900px){.stage.split{gap:8px}.side header{padding:10px 12px}.side header b{font-size:12px}.rec{padding:10px 12px}.rec .rt{font-size:13px}.stamps li{font-size:10px}.tile{font-size:9px;padding:5px}}
"""

def build_b():
    steps = "".join(f'<article class="step{" is-current" if i==0 else ""}"><div class="k">{k}</div><h3>{h}</h3><p>{p}</p></article>' for i,(k,h,p) in enumerate(B_STEPS))
    tiles = "".join(f'<div class="tile {kind}{" on" if s==0 else ""}" data-step="{s}" style="--x:{x}%;--y:{y}%;--r:{r}deg">{lbl}</div>' for (s,kind,lbl,x,y,r) in B_TILES)
    stamps = "".join(f'<li>{s}</li>' for s in B_STAMPS)
    return f'''<title>Clad Admin Desk</title>
{FONTS}
<style>{BASE_CSS}{B_CSS}</style>
{nav()}
<section class="wrap hero">
  <div class="eyebrow">Field software for telecom, utility, and infrastructure contractors</div>
  <h1>The same week, with and without an admin re-typing it.</h1>
  <p>Every field update gets handled somewhere. Either it's re-entered into a spreadsheet, a slide, QuickBooks, and an email, or it's entered once. Scroll to watch the difference pile up.</p>
  <div class="row"><button class="btn accent" type="button">Book a demo</button><button class="btn ghost" type="button">See the week</button></div>
</section>
<section class="wrap story" id="story">
  <div class="steps">{steps}</div>
  <div class="stage-wrap"><div class="stage split">
    <div class="side old">
      <header><b>Without Clad</b><span class="cnt" id="cnt">0 re-entries · 1 handoff</span></header>
      <div class="body"><div class="pile">{tiles}</div></div>
    </div>
    <div class="side new">
      <header><b>With Clad</b><span class="cnt">Entered once</span></header>
      <div class="body"><div class="one"><div class="rec">
        <div class="rk">One update · Mon</div>
        <div class="rt">1,000 FT fiber · 2 hand holes</div>
        <div class="rs">Crew 3 · 6 photos · redline attached</div>
        <ul class="stamps" id="stamps">{stamps}</ul>
      </div></div><div class="ghost"><span>Mock · product view</span></div></div>
    </div>
  </div></div>
</section>
{close()}
<script>
(function(){{
{STEP_JS}
  var steps=[].slice.call(document.querySelectorAll('.step'));
  var tiles=[].slice.call(document.querySelectorAll('.tile'));
  var stamps=[].slice.call(document.querySelectorAll('#stamps li'));
  var cnt=document.getElementById('cnt'); var re={B_REENTRY};
  stepDriver(steps,function(i){{
    tiles.forEach(function(t,k){{ var s=+t.dataset.step; t.classList.toggle('on',s<=i); t.style.transitionDelay = (s===i? (k%3)*0.12+'s':'0s'); }});
    cnt.textContent=re[i]+' re-entr'+(re[i]===1?'y':'ies')+' · '+(i+1)+' handoff'+(i?'s':'');
    cnt.classList.toggle('hot',i>0);
    stamps.forEach(function(s,k){{s.classList.toggle('on',k<i);s.classList.toggle('now',k===i-1);}});
  }});
}})();
</script>'''

# ---------------------------------------------------------------- C: set pieces
C_CSS = r"""
.piece{padding-block:clamp(56px,9vw,120px) 0}
.piece .head{max-width:720px}
.piece h2{font-size:clamp(32px,4.4vw,56px);margin-top:12px}
.piece p.lead{font-size:clamp(17px,1.5vw,20px);color:var(--muted);max-width:50ch;margin:16px 0 0}
.piece .ph{display:block;margin-top:clamp(28px,4vw,48px);aspect-ratio:16/8.5;max-width:100%}
.piece .ph .lbl{position:absolute;top:16px;left:16px}
/* hints: gray-only abstractions that animate in */
.hint{position:absolute;opacity:0;transition:opacity .6s,transform .7s cubic-bezier(.2,.7,.2,1)}
.in .hint{opacity:1;transform:none}
/* blueprint */
.bp{background-image:linear-gradient(var(--shape) 1px,transparent 1px),linear-gradient(90deg,var(--shape) 1px,transparent 1px);background-size:36px 36px;background-position:center}
.bp .line{left:12%;top:58%;width:0;height:4px;background:var(--ph-text);border-radius:2px;opacity:1;transition:width 1.1s cubic-bezier(.2,.7,.2,1) .2s}
.in .bp .line{width:64%}
.bp .node{width:14px;height:14px;border-radius:50%;background:var(--accent);left:var(--x);top:calc(58% - 5px);transform:scale(0);transition-delay:var(--d)}
.in .bp .node{transform:scale(1)}
.bp .pulse{left:52%;top:calc(58% - 13px);width:30px;height:30px;border-radius:50%;border:2px solid var(--accent);opacity:0;animation:none}
.in .bp .pulse{animation:pulse 1.8s ease-out 1.2s infinite}
@keyframes pulse{0%{transform:scale(.4);opacity:.9}100%{transform:scale(1.6);opacity:0}}
.callout{left:55%;top:14%;width:min(280px,38%);background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:12px;box-shadow:0 20px 40px -20px rgba(0,0,0,.35);transform:translateY(14px);transition-delay:1.3s}
.callout .bar{height:8px;background:var(--shape);border-radius:4px;margin-top:8px}
.callout .bar:first-child{margin-top:0;width:60%;background:var(--shape-2)}
.callout .bar:nth-child(2){width:90%}.callout .bar:nth-child(3){width:75%}.callout .bar:nth-child(4){width:45%}
/* invoice */
.inv .sheet{left:50%;top:10%;width:min(420px,62%);transform:translate(-50%,10px);background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:16px;box-shadow:0 20px 40px -20px rgba(0,0,0,.35)}
.in .inv .sheet{transform:translate(-50%,0)}
.inv .row{display:grid;grid-template-columns:1fr 60px;gap:12px;padding:9px 0;border-top:1px solid var(--line);opacity:0;transform:translateX(-10px);transition:opacity .4s,transform .4s}
.inv .row:first-child{border-top:0}
.inv .row i{display:block;height:8px;background:var(--shape);border-radius:4px}
.inv .row i:last-child{background:var(--shape-2)}
.in .inv .row{opacity:1;transform:none}
.in .inv .row:nth-child(1){transition-delay:.3s}.in .inv .row:nth-child(2){transition-delay:.45s}.in .inv .row:nth-child(3){transition-delay:.6s}.in .inv .row:nth-child(4){transition-delay:.75s}
.inv .total{border-top:2px solid var(--ink);margin-top:6px;padding-top:10px;display:flex;justify-content:space-between;align-items:center}
.inv .total i{display:block;height:10px;width:70px;background:var(--shape-2);border-radius:4px}
.inv .total .tag{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);border-radius:999px;padding:3px 8px;opacity:0;transition:opacity .4s 1.2s}
.in .inv .total .tag{opacity:1}
.inv .pick{left:8%;top:22%;width:min(160px,22%);display:flex;flex-direction:column;gap:8px;transform:translateY(10px)}
.inv .pick i{display:block;height:34px;border-radius:8px;background:var(--shape);position:relative}
.inv .pick i::after{content:"";position:absolute;left:10px;top:12px;width:10px;height:10px;border-radius:3px;background:var(--accent)}
/* locates */
.loc .chat{left:50%;top:12%;width:min(400px,60%);transform:translateX(-50%);display:flex;flex-direction:column;gap:10px}
.loc .msg{max-width:78%;border-radius:14px;padding:10px 12px;background:var(--bg);border:1px solid var(--line);opacity:0;transform:translateY(10px);transition:opacity .45s,transform .45s}
.loc .msg.me{align-self:flex-end;background:var(--shape)}
.loc .msg i{display:block;height:8px;background:var(--shape);border-radius:4px;margin-top:6px}
.loc .msg.me i{background:var(--shape-2)}
.loc .msg i:first-child{margin-top:0}
.in .loc .msg{opacity:1;transform:none}
.in .loc .msg:nth-child(1){transition-delay:.2s}.in .loc .msg:nth-child(2){transition-delay:.7s}.in .loc .msg:nth-child(3){transition-delay:1.2s}.in .loc .msg:nth-child(4){transition-delay:1.7s}
.loc .status{left:50%;bottom:10%;transform:translateX(-50%);font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);border-radius:999px;padding:4px 10px;transition-delay:2.2s}
/* pillars */
.pillars{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,3vw,40px);margin-top:clamp(32px,4vw,56px)}
.pillars h3{font-size:18px;letter-spacing:-.02em}
.pillars ul{margin:10px 0 0;padding:0;list-style:none;color:var(--muted);font-size:15px;display:flex;flex-direction:column;gap:4px}
@media (max-width:760px){.pillars{grid-template-columns:1fr}.piece .ph{aspect-ratio:4/3.4}.callout{width:44%}.inv .sheet{width:80%}.inv .pick{display:none}.loc .chat{width:86%}}
"""

def build_c():
    return f'''<title>Clad Set Pieces</title>
{FONTS}
<style>{BASE_CSS}{C_CSS}</style>
{nav()}
<section class="wrap hero">
  <div class="eyebrow">Field software for telecom, utility, and infrastructure contractors</div>
  <h1>Built for the crews putting fiber in the ground.</h1>
  <p>Clad keeps one record of the work from the redline to the invoice. Three things it does that nothing else on your jobsite can.</p>
  <div class="row"><button class="btn accent" type="button">Book a demo</button><button class="btn ghost" type="button">See the three</button></div>
</section>

<section class="wrap piece" id="story">
  <div class="head"><div class="eyebrow">Connected blueprints</div><h2>Tap a line on the drawing. See what it cost, who built it, and when.</h2>
  <p class="lead">Redlines aren't a PDF in a folder. Every foot of fiber and every hand hole on the as-built is tied to the production, photos, and hours behind it.</p></div>
  <div class="ph bp reveal"><span class="lbl">Mock · Connected blueprint</span>
    <div class="hint line"></div>
    <div class="hint node" style="--x:12%;--d:.5s"></div><div class="hint node" style="--x:52%;--d:.9s"></div><div class="hint node" style="--x:75%;--d:1.1s"></div>
    <div class="hint pulse"></div>
    <div class="hint callout"><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div></div>
  </div>
</section>

<section class="wrap piece">
  <div class="head"><div class="eyebrow">Invoices that build themselves</div><h2>Select last week's approved updates. The invoice is done, and it's in QuickBooks.</h2>
  <p class="lead">Quantities, units, and rates come from the production you already approved. Retainage is tracked. Sub bills match against the same updates so you pay for what was built.</p></div>
  <div class="ph inv reveal"><span class="lbl">Mock · Invoice from production</span>
    <div class="hint pick"><i></i><i></i><i></i><i></i></div>
    <div class="hint sheet">
      <div class="row"><i></i><i></i></div><div class="row"><i></i><i></i></div><div class="row"><i></i><i></i></div><div class="row"><i></i><i></i></div>
      <div class="total"><i></i><span class="tag">Synced to QuickBooks</span></div>
    </div>
  </div>
</section>

<section class="wrap piece">
  <div class="head"><div class="eyebrow">AI-assisted locate calls</div><h2>Locates, handled.</h2>
  <p class="lead">Clad helps place and track locate requests for the work on your schedule, so the crew isn't waiting on a ticket Monday morning. <em>(Founder to confirm exact scope of this feature.)</em></p></div>
  <div class="ph loc reveal"><span class="lbl">Mock · Locate assistant</span>
    <div class="hint chat">
      <div class="msg me"><i style="width:70%"></i></div>
      <div class="msg"><i style="width:90%"></i><i style="width:60%"></i></div>
      <div class="msg me"><i style="width:40%"></i></div>
      <div class="msg"><i style="width:80%"></i><i style="width:50%"></i><i style="width:30%"></i></div>
    </div>
    <div class="hint status">Ticket placed · clears Thu</div>
  </div>
</section>

<section class="wrap">
  <div class="sec-head"><div class="eyebrow">What's in the box</div><h2>Capture, manage, bill.</h2></div>
  <div class="pillars">
    <div><h3>Capture</h3><ul><li>Digital as-builts</li><li>Production tracking</li><li>Custom forms</li></ul></div>
    <div><h3>Manage</h3><ul><li>Insights across projects</li><li>Forecasting</li><li>Schedules</li></ul></div>
    <div><h3>Bill</h3><ul><li>Production to invoice</li><li>Retainage</li><li>QuickBooks sync</li></ul></div>
  </div>
</section>
{close()}
<script>
(function(){{
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items=[].slice.call(document.querySelectorAll('.reveal'));
  if(reduce||!('IntersectionObserver' in window)){{ items.forEach(function(el){{el.classList.add('in');}}); return; }}
  var io=new IntersectionObserver(function(es){{ es.forEach(function(e){{ if(e.isIntersecting){{ e.target.classList.add('in'); io.unobserve(e.target);}} }}); }},{{threshold:.35}});
  items.forEach(function(el){{ io.observe(el); }});
}})();
</script>'''

open('a-one-update.html','w').write(build_a())
open('b-admin-desk.html','w').write(build_b())
open('c-set-pieces.html','w').write(build_c())
print('built')
