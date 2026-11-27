from pathlib import Path
import html
P=Path(__file__).resolve().parent;R=P.parents[1];C=P/'컷';C.mkdir(exist_ok=True)
titles=[(P/f'장{g}.md').read_text().splitlines()[0][3:] for g in range(1,9)]
outline=[[x.split('|',3) for x in block.splitlines()] for block in (P/'컷대사.txt').read_text().strip().split('\n\n')]
assert [len(v) for v in outline]==[7,7,8,7,8,8,8,7]
def safe(s):return html.escape(s,quote=True)
def uri(p):return p.resolve().as_uri()
def img(p,style):return '<img class="'+style+'" src="'+uri(p)+'" alt="">'
lead=[[0,1,0,4,2,3,1],[1,3,4,1,2,5,4],[3,3,0,4,2,3,4,5],[3,4,0,1,5,4,3],[0,3,2,1,3,1,4,4],[4,4,1,4,3,2,4,5],[5,1,3,1,4,3,1,5],[0,1,2,4,1,3,5]]
charttitle={'closing':'같은 원금으로 시작한 1년 장부','pockets':'두 서랍을 합치면','boundary':'주가에 따라 달라지는 최종 금액','stub':'분배락 전후, 한 주의 가치','bothdays':'주당 100원 지급 뒤의 총가치','rights':'보유 시기와 수량에 따른 수령액','reinvest':'기말 주가 8,500원일 때','rise':'기말 주가 10,500원일 때','spent':'생활비 60만 원을 쓰면','currency':'100달러의 원화 환산액','compare':'지급 방식이 다른 두 장부','ending':'같은 현금, 다른 결말'}
docname={'docKey':'기본 정보 · 최근 12개월 분배율','docPerf':'성과 표 · NAV 행과 1Y 열','docDef':'정의 · 분모를 설명하는 구절'}
css="""@font-face{font-family:'Jalnan Gothic TTF';font-style:normal;font-weight:100 900;src:local('Jalnan Gothic TTF'),url('file:///home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf') format('truetype')}*{box-sizing:border-box;font-synthesis:none}html,body{margin:0;width:1280px;height:720px;overflow:hidden}body{padding:21px 32px 0;color:#322d2b;background:radial-gradient(ellipse at 19% 5%,#fffaf2 10%,#f5e7d8 100%);font:700 19px/1.28 'Jalnan Gothic TTF',sans-serif}.mast,.folio{display:flex;align-items:center;justify-content:space-between}.mast{color:#753b42;padding-bottom:6px;border-bottom:2px solid #9c7968;letter-spacing:.5px;font-size:14px}.folio{margin:7px 0 10px;gap:15px}h1{margin:0;font:900 38px/1.16 'Jalnan Gothic TTF',sans-serif;letter-spacing:-2px}.tab{white-space:nowrap;background:#fbedb2;border:1px dashed #977b56;border-radius:3px;padding:4px 9px;color:#5e4a35;font-size:16px}.spread{height:398px;display:grid;gap:7px;grid-template-columns:.91fr 1.25fr;grid-template-rows:1fr 1fr;grid-template-areas:'a proof' 'b proof'}.layout1{grid-template-columns:1.2fr .90fr;grid-template-areas:'proof a' 'proof b'}.layout2{grid-template-columns:.81fr 1.13fr .66fr;grid-template-rows:1fr;grid-template-areas:'a proof b'}.layout3{grid-template-columns:1.10fr .86fr;grid-template-rows:.94fr 1.06fr;grid-template-areas:'a b' 'a proof'}.layout4{grid-template-columns:1.2fr .8fr 1fr;grid-template-rows:1fr .8fr;grid-template-areas:'a a proof' 'b b proof'}.layout5{grid-template-columns:.9fr 1.15fr;grid-template-rows:.83fr 1fr;grid-template-areas:'b a' 'proof a'}.frame,.proof{overflow:hidden;border:2.5px solid #43322e;min-width:0;min-height:0;position:relative;border-radius:7px}.frame.a{grid-area:a}.frame.b{grid-area:b}.art{width:100%;height:100%;object-fit:cover;object-position:var(--x,50%) var(--y,48%);display:block}.bubble{position:absolute;left:8px;bottom:7px;max-width:96%;padding:3px 9px 5px;background:#fffdf6;border:2px solid #392924;border-radius:17px 19px 12px 5px;box-shadow:1px 2px 0 #321e213b;font:900 20px/1.2 'Jalnan Gothic TTF',sans-serif;color:#302b29}.b .bubble{left:auto;right:7px;top:7px;bottom:auto;border-radius:18px 16px 5px 18px}.proof{grid-area:proof;background:#f8f4eb;display:flex;flex-direction:column;padding:8px 12px;justify-content:center;align-items:stretch}.proof h2{font:900 22px/1.15 'Jalnan Gothic TTF',sans-serif;margin:0;color:#742e39}.proof small{font-size:14px;color:#68594d;display:block;margin:3px 0}.chart{flex:1;min-height:0;min-width:0;object-fit:contain;width:100%;border-radius:4px;background:#eceeeb}.docimg{height:auto;max-height:100%;width:100%;object-fit:contain;min-height:0;flex:1}.slips{flex:1;min-height:0;display:flex;gap:10px;align-items:center;justify-content:center;padding:6px 2px;background:linear-gradient(140deg,#fff7dd,#f5e7dc 75%,#d9e6e1);border-radius:3px}.slip{width:47%;padding:10px 4px 8px;border-top:3px solid #b07765;border-bottom:1.5px dashed #a98c78;background:#fef5df;text-align:center;box-shadow:2px 3px 4px #5a452c24}.slip:last-child{background:#e4eff0;border-top-color:#5e8390}.slip label{font-size:17px;background:#faedaf;color:#513e32}.slip b{display:block;font-size:22px;font-weight:900;margin-top:4px;line-height:1.16}.footnote{margin:9px 1px 0;padding:0 0 6px;border-bottom:1px dashed #988577;font-size:18px;color:#342e29}.footnote b{color:#912c3d}.source{font-size:13px;color:#68594e;margin-top:5px}.cap{position:absolute;left:0;right:0;bottom:0;height:119px;background:#2d2830}.poster .cap{display:none}.poster .spread{height:491px}.poster .footnote{font-size:20px}.poster h1{font-size:40px}.poster .source{font-size:15px}.story .proof{background:#f7eac8}.story .proof p{font:800 21px/1.34 'Jalnan Gothic TTF';margin:7px 0}.orig{flex:1;min-height:0;display:flex;gap:16px;align-items:center;justify-content:center}.orig img{height:100%;min-height:0;object-fit:contain}.orig b{font-size:24px;color:#753343}.twoDoc{display:flex;flex:1;min-height:0;flex-direction:column;justify-content:space-evenly}.twoDoc div{padding:1px 5px;min-height:0;flex:1;display:flex;flex-direction:column}.twoDoc span{color:#672e39;font-size:17px}.twoDoc img{flex:1;min-height:0;object-fit:contain;width:100%}"""
def panel(cls,i,text,x,y):
 return f'<div class="frame {cls}" style="--x:{x}%;--y:{y}%">'+img(P/f'매표소{i}.jpg','art')+'<div class="bubble">'+safe(text)+'</div></div>'
def page(g,p,variant,kind='ref'):
 q,answer,desc,spec=outline[g-1][p];a=lead[g-1][p];b=([1,2,4,1,5,0] if variant==0 else [3,4,3,2,1,4])[a]
 label='가상 원화 장부';source='TRUSTA 투자연구소 · 열두 봉투 가상 계산'
 if g==6:label='미국 QYLD 공시';source='Global X · QYLD 팩트시트 및 상품 설명'
 if g==4 and p==1:label='미국 지급 이력';source='Global X · QYLD 상품 설명 및 분배 일정'
 if g==3 and p in (2,3,6):source='미국 SEC · 펀드 분배금 투자자 안내'
 if g==4 and p==0:source='미국 SEC · 분배락일 투자자 안내'
 if g==6 and p==5:label='공시 산식 · 가상 예시'
 if g==7 and p in (5,6):label='가상 원화 환산'
 if g==8 and p==3:label='편집부 질문'
 head=q;character=q
 f=(g+2*p+variant*3)%6
 if kind=='poster':
  head='열두 번 돈이 들어왔는데, 왜 30만 원이 모자랄까?';a,b=0,2;character='도장에 ‘이익’이라고 쓸까?';answer='아래 서랍도 열어 봐!';spec='pockets';f=0
  desc='연초 1,000만 원 → 기말 970만 원. 1년에 받은 현금은 원금의 12%, 같은 기간 투자 손익은 −3%.';label='가상 · 원화 · 1년'
 if kind=='docposter':
  head='같은 종이의 12.11%와 22.94%, 어느 줄을 읽을까?';character='지급액은 어느 쪽이야?';answer='성과는 NAV와 1Y가 만나는 칸!';a,b=4,1;spec='pair';f=0
  label='공시 관측 2026.09.30';desc='오른쪽 기본 정보는 최근 12개월 분배율, 왼쪽 성과 표는 NAV 기준 1년 성과다. 두 값을 더하면 안 된다.'
 if kind=='story':
  f=(3 if (p+g+variant)%2 else 5);proof='<h2>'+safe(answer)+'</h2><p>'+safe(desc)+'</p>'
 elif spec=='pair':
  proof='<h2>미국 QYLD · 실제 팩트시트 1쪽</h2><div class="twoDoc"><div><span>최근 12개월 분배율</span>'+img(P/'docKey.png','')+'</div><div><span>NAV 1년 성과</span>'+img(P/'docPerf.png','')+'</div></div>'
 elif spec in docname and kind=='ref':
  item={'docKey':('최근 12개월 분배율','12.11%','지급 주기','월간'),'docPerf':('기준 시점','2026.09.30','NAV · 1년 성과','22.94%'),'docDef':('분자','12개월 분배 합계','분모','최근 NAV ＋ 해당 기간 자본이득 분배')}[spec]
  proof='<h2>'+docname[spec]+'</h2><small>미국 QYLD · 2026.09.30 · 공시 독해</small><div class="slips">'+''.join('<div class="slip"><label>'+safe(x)+'</label><b>'+safe(y)+'</b></div>' for x,y in [item[:2],item[2:]])+'</div>';f=0 if variant==0 else 1
 elif spec in docname:
  proof='<h2>'+docname[spec]+'</h2><small>Global X QYLD · 2026.09.30</small>'+img(P/(spec+'.png'),'docimg');f=(1 if variant else 0)
 elif kind=='ref' and g==2 and p==6 and variant:
  proof='<h2>세로 장부도 같은 결산</h2><div class="orig">'+img(R/'그림/EP041.png','')+'<b>850만 원<br>＋120만 원<br>＝970만 원</b></div>';f=1
 elif spec in charttitle:
  unit='가상 실험 · 같은 단위, 공통 0선 · 막대 높이를 비교'
  if spec=='pockets':unit='원화 · 만 원 단위 · 세 번째 막대는 두 서랍의 합계'
  proof='<h2>'+charttitle[spec]+'</h2><small>'+unit+'</small>'+img(P/'glass'/(spec+'_표기.png'),'chart')
  if kind!='poster':f=[0,1,2][(g+p+variant)%3]
 else:
  l,k,m,v=spec.split('/')
  proof='<h2>창구에서 대조한 두 칸</h2><div class="slips">'+''.join('<div class="slip"><label>'+safe(x)+'</label><b>'+safe(y)+'</b></div>' for x,y in [(l,k),(m,v)])+'</div>'
 if kind=='poster':
  return f'<!doctype html><html lang="ko"><meta charset="utf-8"><style>{css}.theatre{{height:485px;display:grid;gap:7px;grid-template-columns:24fr 56fr 20fr;grid-template-rows:45fr 55fr;grid-template-areas:"a proof c" "a proof b"}}.theatre .c{{grid-area:c}}.theatre .bubble{{font-size:19px}}.theatre .a .art{{object-position:67% center}}.theatre .b .art{{object-position:20% center}}.theatre .c .art{{object-position:62% center}}.theatre .a .bubble{{left:4px;bottom:10px}}.theatre .b .bubble{{top:auto;bottom:8px;right:4px}}.theatre .proof{{padding:8px 5px}}.theatre .chart{{object-fit:contain;background:#e7e8e5}}</style><body class="poster"><div class="mast"><b>TRUSTA 투자연구소　·　천억이의 금융 만화</b><b>겨울 인형극장 매표소</b></div><div class="folio"><h1>{safe(head)}</h1><span class="tab">{safe(label)}</span></div><div class="theatre">'+panel('a',0,'열두 번이나 받았는데?',67,50)+f'<div class="proof">{proof}</div>'+panel('c',1,'수첩엔 얼마가 남았지?',62,45)+panel('b',2,'30만 원이 모자라!',20,48)+'</div><div class="footnote"><b>상자 두 개를 같은 날 결산하면</b>　ETF 850만 원 ＋ 현금 120만 원 ＝ 970만 원. 원금 1,000만 원보다 3% 적다.</div><div class="source">출처　TRUSTA 투자연구소 · 열두 봉투 가상 계산</div></body></html>'
 cls='poster' if kind in ('poster','docposter') else kind
 ac=[43,47,27,35,66,43];bc=[60,58,26,68,47,62];x,y=ac[a],40 if a in (0,1,2) else 50
 return f'<!doctype html><html lang="ko"><meta charset="utf-8"><style>{css}</style><body class="{cls}"><div class="mast"><b>TRUSTA 투자연구소　·　천억이의 금융 만화</b><b>{safe(titles[g-1])}</b></div><div class="folio"><h1>{safe(head)}</h1><span class="tab">{safe(label)}</span></div><div class="spread layout{f}">'+panel('a',a,character,x,y)+panel('b',b,answer,bc[b],45)+f'<div class="proof">{proof}</div></div><div class="footnote"><b>{safe(answer)}</b>　{safe(desc)}</div><div class="source">출처　{safe(source)}</div><div class="cap"></div></body></html>'
