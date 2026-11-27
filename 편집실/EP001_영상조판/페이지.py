from pathlib import Path
import html, json, math, os, shutil, subprocess,tempfile
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];C=P/'컷';C.mkdir(exist_ok=True)
titles=[s.split('\n',1)[0] for s in ('\n\n'.join((P/f'원고_{x}.md').read_text().strip() for x in ['앞','중간','뒤'])).split('## ')[1:]]
outline=[[v.split('|',3) for v in block.splitlines()] for block in (P/'컷대사.txt').read_text().strip().split('\n\n')]
glabels={'opening':['A  50,000원','B  30,000원','C  20,000원'],'after':['A  40,000원','B  30,000원','C  20,000원'],'impact':['A  10,000원','B  6,000원','C  4,000원'],'daily':['출발 10만 원','하락 뒤 9만 원','반등 뒤 9만 8천 원'],'account':['펀드만 50%','A 직접 보유 58.33%','현금 보유 41.67%'],'reported':['엔비디아 8.4%','나머지 순자산 91.6%'],'reset':['A  45,000원','B  27,000원','C  18,000원']}
scene=[[1,0,0,2,2,4],[1,2,1,0,4,5],[2,2,4,0,4,2,5],[3,3,3,4,1,0,3],[2,4,2,0,1,0,2],[4,4,4,2,4,1,1,5],[5,2,0,1,4,2,3],[5,4,2,4,0,1,5]]
css="""@font-face{font-family:'Jalnan Gothic TTF';src:local('Jalnan Gothic TTF'),url('file:///home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf') format('truetype');font-weight:100 900}*{box-sizing:border-box;font-synthesis:none}html,body{margin:0;width:1280px;height:720px;overflow:hidden}body{background:radial-gradient(ellipse at 30% 14%,#fffdf5,#f1e3c9);color:#302e2a;font:700 19px 'Jalnan Gothic TTF',sans-serif;padding:18px 28px}.mast{display:flex;justify-content:space-between;align-items:center;font-size:15px;color:#705b47;letter-spacing:1px}h1{font:900 37px/1.17 'Jalnan Gothic TTF',sans-serif;letter-spacing:-2px;margin:8px 0 10px;border-bottom:2px solid #524940;padding-bottom:7px}mark{color:inherit;background:linear-gradient(transparent 55%,#ffe99e 55%)}.spread{height:405px;display:grid;gap:7px;grid-template-columns:43fr 57fr;grid-template-rows:1fr 1fr;grid-template-areas:'a proof' 'b proof'}.s1{grid-template-columns:57fr 43fr;grid-template-areas:'proof a' 'proof b'}.s2{grid-template-columns:25fr 52fr 23fr;grid-template-rows:1fr;grid-template-areas:'a proof b'}.s3{grid-template-columns:.98fr 1.05fr 1.14fr;grid-template-rows:1fr 1.04fr;grid-template-areas:'a a b' 'proof proof b'}.s4{grid-template-columns:1.30fr .8fr 1fr;grid-template-rows:1.18fr .82fr;grid-template-areas:'a proof proof' 'a b b'}.panel{border:3px solid #3b3229;border-radius:9px;position:relative;min-height:0;min-width:0;overflow:hidden;background:#fffdf5}.a{grid-area:a}.b{grid-area:b}.panel>img.art{width:100%;height:100%;object-fit:cover;object-position:center 44%}.s2 .a .art{object-position:22% center}.s2 .b .art{object-position:73% center}.talk{position:absolute;left:9px;top:7px;max-width:93%;background:#fffdf6;border:2.3px solid #352b25;border-radius:24px 18px 17px 6px;font:900 20px/1.2 'Jalnan Gothic TTF',sans-serif;padding:5px 10px;box-shadow:2px 3px #79553f3b}.talk:after{content:'';display:block;position:absolute;left:20px;bottom:-7px;width:11px;height:11px;background:#fffdf6;border-bottom:2px solid #352b25;border-right:2px solid #352b25;transform:rotate(40deg)}.b .talk{top:auto;bottom:7px;left:auto;right:7px}.b .talk:after{display:none}.proof{grid-area:proof;display:flex;flex-direction:column;padding:8px 13px;background:linear-gradient(160deg,#fff,#f7f4eb 67%,#ece1c8)}.proof h2{font-size:23px;margin:0 0 4px;line-height:1.22;color:#78332f}.proof small{font-size:15px;color:#5e5d58}.model{flex:1;min-height:0;object-fit:contain;width:100%;background:radial-gradient(ellipse at 25% 10%,#f7f6f0,#eaece9)}.legend{display:flex;justify-content:space-evenly;gap:6px;padding-top:4px;font-size:16px}.legend b{padding:3px 5px;border-bottom:3px solid #d18c46}.legend b:nth-child(2){border-color:#78a5bf}.legend b:nth-child(3){border-color:#74ac94}.paper{flex:1;display:flex;align-items:center;justify-content:space-evenly;gap:10px;background:repeating-linear-gradient(0deg,#f8edce 0px 31px,#f3e5c3 32px 33px);margin-top:5px}.ticket{border:1px solid #bda77c;padding:11px 13px;background:#fff7d9;transform:rotate(-2deg);text-align:center;box-shadow:2px 5px #83663b29;max-width:55%}.ticket:nth-child(2){background:#e9efe6;transform:rotate(2deg)}.ticket label{font-size:16px;display:block;margin-bottom:5px}.ticket b{font-size:23px}.footnote{margin-top:8px;font-size:19px;line-height:1.35;padding-bottom:7px;border-bottom:1px solid #9f947e}.footnote strong{color:#8e2737}.source{font-size:13px;color:#665c50;margin-top:5px}.cap{position:absolute;bottom:0;left:0;right:0;height:121px;background:#19343a}.story .spread{grid-template-columns:.64fr 1.36fr;grid-template-areas:'a b' 'proof b'}.story .proof{justify-content:center;background:#fff3d3}.story .talk{font-size:21px}.doc .spread{grid-template-columns:.75fr 1.25fr;grid-template-areas:'a proof' 'b proof'}.doc .proof img{object-fit:contain;min-height:0;flex:1;width:100%}.vert{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;gap:13px}.vert img{height:100%;object-fit:contain}.vert b{font-size:22px;color:#7d4736}.poster .cap{display:none}.poster .spread{height:475px}.poster h1{font-size:41px}.poster .footnote{font-size:20px}.poster .source{font-size:15px}"""
def crop_source():
 im=Image.open(P/'팩트시트2쪽.png').convert('RGB')
 sx,sy=im.width/612,im.height/792
 for name,rect,marks in [('공시_상위열',(316,99,582,239),[(319,114,578,128),(319,222,578,236)]),('공시_첫행',(317,99,582,151),[(321,114,578,129)]),('공시_합계',(317,164,582,239),[(321,222,578,236)])]:
  x,y,x2,y2=rect;part=im.crop((int(x*sx),int(y*sy),int(x2*sx),int(y2*sy)));pen=ImageDraw.Draw(part)
  for l,u,rr,b in marks:pen.rounded_rectangle((round((l-x)*sx),round((u-y)*sy),round((rr-x)*sx),round((b-y)*sy)),radius=5,outline='#a82d3c',width=3)
  part.save(P/(name+'.png'))
def h(s):return html.escape(s)
def im(p):return p.resolve().as_uri()
def panel(which,n,txt):return f'<div class="panel {which}"><img class="art" src="{im(P/f"식탁{n}.jpg")}"><div class="talk">{h(txt)}</div></div>'
def page(g,p,variant,kind='ref'):
 q,key,desc,spec=outline[g-1][p];a=scene[g-1][p];b=(a+[2,3,5,1,3,1][a])%6
 if b==a:b=(a+1)%6
 ans=['접시부터 펼쳐 볼게.','여기서 하나만 빼자!','밑면에 뭐가 적혔지?','세 접시가 같이 간다!','빨간 연필로 찾아 보자.','날짜도 같이 적자.'][b]
 case='가상 실험 · 원화 · 사례마다 같은 출발점에서 비교';source='TRUSTA 투자연구소 · 가상 장부와 계산'
 if g==3 and p in [4,5,6]:source='미국 SEC · ETF 투자자 안내 / TRUSTA 가상 장부'
 if g==4 and p==3:source='FINRA · 자산배분과 분산투자 안내'
 if g==6 or (g==8 and p in [1,2,3]):case='공시 관측 2026.09.30 · 원화 예시는 가상';source='Vanguard · S&P 500 ETF 팩트시트'
 if kind=='doc':
  idx='공시_합계' if p==5 else '공시_첫행' if p in [1,3,6] else '공시_상위열';proof=f'<h2>운용사의 실제 보유종목 표</h2><small>VOO · 2026.09.30 · 전체 순자산 대비 %</small><img src="{im(P/(idx+".png"))}">';a,b=4,2;ans='같은 줄에서 읽어 봐!'
 elif kind=='story':proof=f'<h2>{h(key)}</h2><div>{h(desc)}</div>';a,b=a,(1 if a!=1 else 0)
 elif kind=='poster':
  q='ETF 10만 원, 한 회사가 20% 내리면 얼마를 잃을까?';key='십만 원의 절반만 A에 있다';ans='칩 하나, 만 원이네!';a,b=0,1;desc='A만 20% 하락하면 50,000원 × 20% = 10,000원 손실. B와 C가 그대로인 하루의 ETF 가치는 90,000원이다.';spec='opening';proof=f'<h2>A · B · C에 나뉜 10만 원</h2><small>가상 원화 원금 · 전날 장 마감 · 막대 높이 = 각 회사의 금액</small><img class="model" src="{im(P/"glass/opening.png")}"><div class="legend">'+''.join('<b>'+x+'</b>' for x in glabels[spec])+'</div>'
 elif g==2 and p==0 and variant:
  proof=f'<h2>세로 자료에서 다시 찾는 첫날 장부</h2><div class="vert"><img src="{im(R/"그림/EP001.png")}"><b>50% · 30% · 20%<br>각각 다른 회사</b></div>'
 elif spec in glabels:proof=f'<h2>{h(key)}</h2><small>{h(case)}</small><img class="model" src="{im(P/"glass"/(spec+".png"))}"><div class="legend">'+''.join('<b>'+h(x)+'</b>' for x in glabels[spec])+'</div>'
 else:
  l,x,m,y=spec.split('/');proof=f'<h2>{h(key)}</h2><div class="paper"><div class="ticket"><label>{h(l)}</label><b>{h(x)}</b></div><div class="ticket"><label>{h(m)}</label><b>{h(y)}</b></div></div>'
 if (kind=='poster' or (kind=='ref' and spec in glabels)) and spec!='reported' and not (g==2 and p==0 and variant and kind=='ref'):
  revised=P/'막대교정'/(spec+'_표기.png')
  if revised.is_file():
   oldpath=im(P/'glass'/(spec+'.png'));proof=proof.replace(oldpath,im(revised));proof=proof.partition('<div class="legend">')[0]
 form=(g+p+variant*2)%5
 if spec in glabels:form=(g+p+variant)%3
 if kind=='poster':form=0
 return f'<!doctype html><html lang="ko"><meta charset="utf-8"><style>{css}</style><body class="{kind}"><div class="mast"><b>TRUSTA 투자연구소　/　천억이의 금융 만화</b><span>{h(titles[g-1])}</span></div><h1><mark>{h(q)}</mark></h1><div class="spread s{form}">'+panel('a',a,q if kind!='poster' else '열 개 중 두 개를 빼면 돼?')+panel('b',b,ans)+f'<div class="panel proof">{proof}</div></div><div class="footnote"><strong>{h(key)}</strong>　{h(desc)}</div><div class="source">출처　{h(source)}</div><div class="cap"></div></body></html>'
def capture(file,html):
 with tempfile.TemporaryDirectory(prefix='trusta001-html-') as td:
  td=Path(td);src=td/'frame.html';src.write_text(html);out=td/'shot.png'
  run=subprocess.run(['google-chrome','--headless','--no-sandbox','--hide-scrollbars','--disable-dev-shm-usage','--disable-gpu','--allow-file-access-from-files','--user-data-dir='+str(td/'profile'),'--window-size=1280,720','--force-device-scale-factor=1.5','--virtual-time-budget=900','--screenshot='+str(out),src.as_uri()],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  if run.returncode or not out.is_file():raise RuntimeError('가로 화면 캡처 실패 '+str(file))
  picture=Image.open(out).convert('RGB');assert picture.size==(1920,1080)
  if file.suffix=='.jpg':picture.save(file,quality=92)
  else:picture.save(file)
if __name__=='__main__':
 crop_source();capture(R/'시각자료/EP001_세접시_원화노출.png',page(1,0,0,'poster'));capture(P/'자료화면_검토.png',page(6,3,0,'doc').replace('class="doc"','class="doc poster"').replace('class="talk">이 한 줄을 십만 원에 옮기면?', 'class="talk">엔비디아가 어느 줄이지?'))
