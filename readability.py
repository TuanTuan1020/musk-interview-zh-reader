# -*- coding: utf-8 -*-
import pathlib,json,re,html
root=pathlib.Path(__file__).parent
page=(root/'dist/index.html').read_text()
source=json.loads((root/'source.json').read_text()); z=json.loads((root/'translations.json').read_text())
starts=[0,21,32,58,74,101,129,153,195,220,234,257,284,374,394]
heads=re.findall(r'<header class="chapter-heading">.*?</header>',page,re.S)
reading=[];turncount=0
for k in range(14):
 turns=[]
 for i in range(starts[k],starts[k+1]):
  bits=re.split(r'(主持人插播：|主持人：|马斯克：)',z[i]); speaker=None
  for part in bits:
   if re.fullmatch(r'(主持人插播|主持人|马斯克)：',part):speaker=part[:-1]
   elif part:
    who=speaker or '对话'
    if turns and turns[-1]['speaker']==who:
     turns[-1]['pieces'].append((i+1,part))
    else:turns.append({'speaker':who,'pieces':[(i+1,part)]})
 blocks=[]
 for t in turns:
  turncount+=1
  paras=[];current=''
  continuous=''.join(part for idx,part in t['pieces'])
  sentences=re.findall(r'【[^】]*】|[^。！？【]+[。！？]?[”’」』]?|[。！？]',continuous)
  assert ''.join(sentences)==continuous
  for sentence in sentences:
   if current and len(current)+len(sentence)>220:
    paras.append(current);current=''
   current+=sentence
  if current:paras.append(current)
  body=''.join('<p>'+html.escape(text)+'</p>' for text in paras)
  body=re.sub(r'【(.*?)】',r'<span class="read-note">〔\1〕</span>',body)
  role='host' if t['speaker'].startswith('主持人') else 'guest'
  blocks.append(f'<div class="reading-turn {role}" data-index="{t["pieces"][0][0]}"><div class="turn-label">{t["speaker"]}</div><div class="turn-text">{body}</div></div>')
 reading.append(f'<section class="reading-chapter" id="read-chapter-{starts[k]}">{heads[k]}{"".join(blocks)}</section>')
page=page.replace('<article id="transcript"',f'<article id="reading" aria-label="中文连贯阅读">{"".join(reading)}</article><article id="transcript"')
page=page.replace('马斯克访谈<br>中文全文','马斯克访谈 · 中文全文').replace('中文</button>','舒适阅读</button>').replace('中文全文 · 按原稿顺序阅读','舒适阅读 · 连贯对话').replace('点击段落编号，可定位到该段','连续阅读 · 自动记住阅读位置')
style='''
/* Continuous conversation reading */
:root{--font:20px;--ink:#20251f;--muted:#626b61}.main{max-width:790px}.layout{max-width:1270px;grid-template-columns:222px minmax(0,1fr);gap:65px}.hero{padding:35px 0 25px}.hero h1{font-size:37px;letter-spacing:-1px;line-height:1.4}.hero .eyebrow{margin-bottom:14px}.hero-en{font-size:15px;margin-bottom:14px}.intro{font-size:15px;line-height:1.85}.stats{margin-top:18px}.editor-note{margin:18px 0;padding:12px 16px}.toolbar{gap:10px}.toolbar input{font-size:14px}.segmented button{font-size:13px;padding:7px 11px}.reading-status{font-size:12px;min-height:43px}.sidebar nav a{font-size:14px;padding-top:10px;padding-bottom:10px}.sidebar .side-footer{font-size:12px}.chapter-heading{margin-bottom:30px}.chapter-heading h2{font-size:29px}.chapter-heading .eyebrow span{display:none}.reading-chapter{padding-top:30px;scroll-margin-top:150px}.reading-chapter+.reading-chapter{margin-top:30px;border-top:1px solid var(--line);padding-top:40px}.reading-turn{margin:0 0 30px;scroll-margin-top:170px}.turn-label{font-size:13px;line-height:1.5;letter-spacing:1px;font-weight:650;margin-bottom:9px;color:#3c6156}.turn-text p{font-size:var(--font);line-height:1.95;letter-spacing:.2px;margin:0 0 18px;overflow-wrap:anywhere}.turn-text p:last-child{margin-bottom:0}.host{border-left:3px solid #c1d1c6;background:#edf1eb;padding:18px 22px;border-radius:0 6px 6px 0}.host .turn-label{color:#5a6c5f}.guest{padding:2px 0 2px 25px}.guest .turn-label{color:#1c5146}.read-note{color:#62695f;font-size:.76em;line-height:1.8}.read-note:before{content:' ';white-space:pre}#transcript{display:none}.bilingual #reading,.searching #reading{display:none}.bilingual #transcript,.searching #transcript{display:block}.passage{padding-left:32px}.zh .speaker{display:block;font-size:13px;margin:10px 0 6px;color:var(--accent)}.zh{font-size:var(--font);line-height:1.95}.en{font-size:16px;line-height:1.85;color:#60685f}.zh .uncertain{color:#6b6e60}.font-tools button{font-size:15px;min-width:34px;height:37px}.font-tools button:disabled{opacity:.3;cursor:default}.bottom{margin-top:30px}.back-top{position:fixed;bottom:25px;right:24px;border:1px solid var(--line);border-radius:30px;background:var(--paper);padding:12px 17px;font-size:13px;color:var(--accent);box-shadow:0 3px 15px #00000008;z-index:8}
@media(max-width:1100px){.layout{grid-template-columns:190px minmax(0,1fr);gap:35px}.sidebar nav a{font-size:13px}.toolbar{gap:6px}.segmented button{font-size:12px;padding:7px 8px}}
@media(max-width:760px){.layout{display:block;padding:0 20px}.hero{padding:25px 0 20px}.hero h1{font-size:30px;line-height:1.35;letter-spacing:-.7px}.hero .eyebrow{font-size:9px;margin-bottom:13px}.hero-en{font-size:13px}.intro{font-size:14px;line-height:1.9}.stats{font-size:11px;gap:13px}.stats strong{font-size:12px}.toolbar{display:grid;grid-template-columns:1fr auto;top:54px;padding:10px 0;gap:9px}.search-wrap{grid-column:1/-1;min-width:0}.segmented{width:max-content}.segmented button{font-size:13px;padding:7px 14px}.font-tools{position:static;pointer-events:auto;width:auto;justify-content:flex-end}.font-tools button{width:38px;height:34px;font-size:15px}.reading-status{padding-right:0;min-height:43px;font-size:11px;flex-wrap:wrap}.reading-status button{font-size:11px}.top-inner{padding:14px 20px}.sidebar{top:53px}.chapter-heading h2{font-size:25px}.reading-chapter{padding-top:22px;scroll-margin-top:190px}.reading-chapter+.reading-chapter{padding-top:30px}.reading-turn{margin-bottom:25px;scroll-margin-top:200px}.turn-label{font-size:12px;margin-bottom:8px}.host{padding:15px 16px}.guest{padding:0 3px 0 0}.turn-text p{font-size:var(--font);line-height:1.95;letter-spacing:0;margin-bottom:17px}.chapter-heading{margin-bottom:25px}.passage{scroll-margin-top:205px;padding-left:0}.para-number{position:static;display:block;margin:0 0 8px}.zh .speaker{font-size:13px}.en{font-size:16px}.editor-note{font-size:11px;margin:15px 0}.back-top{bottom:15px;right:15px;padding:10px 13px;font-size:12px}html{scroll-padding-top:190px}}
@media print{.back-top{display:none}.host{background:transparent;border-color:#bbb}.turn-text p{font-size:12pt}.guest{padding-left:0}.turn-label{font-size:10pt}}
'''
page=page.replace('</style>',style+'</style>')
page=page.replace('<script>','<a class="back-top" href="#top" aria-label="回到顶部">↑ 顶部</a><script>',1)
js='''
const $=s=>document.querySelector(s);
const rows=[...document.querySelectorAll('.passage')], rawSections=[...document.querySelectorAll('.chapter')], readSections=[...document.querySelectorAll('.reading-chapter')], turns=[...document.querySelectorAll('.reading-turn')], navs=[...document.querySelectorAll('[data-chapter]')];
const originals=rows.map(r=>({zh:r.querySelector('.zh').textContent,en:r.querySelector('.en').textContent}));
let query='',size=20,saved=1,mode=false;try{saved=+localStorage.getItem('musk-read-v1')||1;size=+localStorage.getItem('musk-size-v2')||20}catch(e){}size=Math.min(26,Math.max(17,size));
function setSize(){document.documentElement.style.setProperty('--font',size+'px');$('#smaller').disabled=size===17;$('#larger').disabled=size===26}setSize();
function text(node,value,q){let pos=0,idx;let lower=value.toLowerCase(),term=q.toLowerCase();if(!q){node.append(document.createTextNode(value));return}while((idx=lower.indexOf(term,pos))!==-1){node.append(document.createTextNode(value.slice(pos,idx)));let m=document.createElement('mark');m.textContent=value.slice(idx,idx+q.length);node.append(m);pos=idx+q.length}node.append(document.createTextNode(value.slice(pos)))}
function decorate(node,value,q){node.replaceChildren();for(let part of value.split(/(主持人插播：|主持人：|马斯克：|【[^】]*】)/g)){if(!part)continue;let s=document.createElement('span');if(/^(主持人插播|主持人|马斯克)：$/.test(part))s.className='speaker';else if(part.startsWith('【'))s.className='uncertain';text(s,part,q);node.append(s)}}
function paint(q){query=q.trim();document.body.classList.toggle('searching',!!query);let n=0;rows.forEach((r,i)=>{let a=originals[i],show=!query||(a.zh+' '+a.en).toLowerCase().includes(query.toLowerCase());r.hidden=!show;if(show){n++;decorate(r.querySelector('.zh'),a.zh,query);let e=r.querySelector('.en');e.replaceChildren();text(e,a.en,query)}});rawSections.forEach(s=>s.hidden=![...s.querySelectorAll('.passage')].some(r=>!r.hidden));$('#empty').style.display=n?'none':'block';$('#status').textContent=query?'找到 '+n+' 段相关内容':mode?'中英对照 · 保留原稿逐段对应':'舒适阅读 · 连贯对话';$('#resume').hidden=!!query||saved<=1;update()}
function closestTurn(i){return [...turns].reverse().find(t=>+t.dataset.index<=i)||turns[0]}
function resumeAt(i){let target=(mode||query)?document.getElementById('p-'+i):closestTurn(i);if(target)target.scrollIntoView({behavior:'smooth',block:'start'})}
$('#resume').onclick=()=>resumeAt(saved);if(saved>1)$('#resume').textContent='继续上次阅读 →';
let timer;$('#search').oninput=e=>{clearTimeout(timer);timer=setTimeout(()=>paint(e.target.value),100)};
function language(b){const visible=(mode?rows:turns).find(r=>!r.hidden&&r.getBoundingClientRect().bottom>190);const index=visible?+visible.dataset.index:1;const wasReading=window.scrollY>550;mode=b;document.body.classList.toggle('bilingual',b);$('#chinese').setAttribute('aria-pressed',String(!b));$('#bilingual').setAttribute('aria-pressed',String(b));paint($('#search').value);if(wasReading)resumeAt(index)}$('#chinese').onclick=()=>language(false);$('#bilingual').onclick=()=>language(true);
function font(d){size=Math.min(26,Math.max(17,size+d));setSize();try{localStorage.setItem('musk-size-v2',size)}catch(e){}}$('#smaller').onclick=()=>font(-1);$('#larger').onclick=()=>font(1);
$('#menu').onclick=()=>{let on=$('#sidebar').classList.toggle('open');$('#menu').setAttribute('aria-expanded',String(on))};navs.forEach(a=>a.onclick=e=>{e.preventDefault();if(query){$('#search').value='';paint('')}let id=(mode?'chapter-':'read-chapter-')+a.dataset.chapter;let target=document.getElementById(id);if(target){history.replaceState(null,'','#'+id);target.scrollIntoView({behavior:'smooth'})}$('#sidebar').classList.remove('open');$('#menu').setAttribute('aria-expanded','false')});
let scrolling=false;function update(){let h=document.documentElement;$('#progress').style.width=(h.scrollHeight>innerHeight?Math.min(100,window.scrollY/(h.scrollHeight-innerHeight)*100):0)+'%';if(!query){let list=mode?rawSections:readSections,active=list[0];for(let s of list)if(s.getBoundingClientRect().top<230)active=s;let id=active.id.replace('read-','');navs.forEach(a=>a.classList.toggle('active','chapter-'+a.dataset.chapter===id));let nearest=(mode?rows:turns).find(r=>r.getBoundingClientRect().bottom>190);if(nearest&&window.scrollY>500)try{localStorage.setItem('musk-read-v1',nearest.dataset.index)}catch(e){}}scrolling=false}window.addEventListener('scroll',()=>{if(!scrolling){requestAnimationFrame(update);scrolling=true}},{passive:true});
function download(){let blob=new Blob([fullText],{type:'text/plain;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='马斯克访谈中文全文.txt';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}document.querySelectorAll('[data-download]').forEach(b=>b.onclick=download);
paint('');if(/^#p-\\d+$/.test(location.hash)){language(true)}else if(/^#chapter-\\d+$/.test(location.hash)){const t=document.getElementById(location.hash.slice(1).replace('chapter-','read-chapter-'));if(t)t.scrollIntoView()}
'''
page=re.sub(r'const \$=s=>document.querySelector\(s\);.*?</script>',lambda m:js+'</script>',page,flags=re.S)
(root/'dist/index.html').write_text(page)
print('Reading edition:',turncount,'speaker turns; 394 source paragraphs preserved')
