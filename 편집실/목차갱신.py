"""담당 원고 기록과 낭독 해시를 읽어 진행표·목차·로컬 전자책 검토본을 재구성한다."""
import csv
import fcntl
import hashlib
import html
import json
import os
import re
import tempfile
import zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import quote,unquote
from xml.etree import ElementTree as ET
from markdown_it import MarkdownIt
from 재생실갱신 import audio_rows, main as refresh_playback
R=Path(__file__).resolve().parents[1]
ED=R/'편집실'
def atomic(p,s):
 fd,n=tempfile.mkstemp(dir=p.parent,prefix='.work-')
 try:
  with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(s)
  os.replace(n,p)
 finally:
  Path(n).unlink(missing_ok=True)
def H(s):return html.escape(str(s),quote=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text())
def link(k,r):return '['+r['제목']+']('+k+'.md)'
md=MarkdownIt('commonmark',{'html':False,'xhtmlOut':True}).enable('table')
def main():
 with (R/'집필인계/1000편_분담.csv').open(encoding='utf-8-sig') as f: reg={d['ID']:d for d in csv.DictReader(f)}
 master=Path('/home/yh/Downloads/TRUSTA_100_제작마스터.csv')
 with master.open(encoding='utf-8-sig') as f: orig={d['ID']:d for d in csv.DictReader(f)}
 info={p.stem:j(p) for p in (ED/'원고기록').glob('*.json')}
 assert set(info)<=set(reg)
 initial=list(orig)+[f'FAQ{i:02d}' for i in range(1,6)]
 order=sorted(initial,key=lambda k:(int(orig.get(k,{}).get('추천발행순서') or 999),k))+sorted(set(info)-set(initial))
 available=[k for k in order if k in info and (R/(k+'.md')).exists()]
 verified={}
 for k in available:
  f=ED/(k+'_낭독검산.json');v=R/'낭독본문'/(k+'.md')
  if f.exists() and v.exists():
   d=j(f)
   if d.get('판정')=='PASS' and d.get('재생초',0)>=1020 and d.get('sha256')==sha(v):verified[k]=d['재생초']
 fact=[k for k in available if '보류' in info[k]['팩트체크']]
 counts=Counter(m['종류'] for k in available for m in info[k]['이미지'])
 sec=' · '.join(f'{t} {n}장' for t,n in counts.items())
 sounds={k:row for k,row in audio_rows().items() if k in available}
 strict={k:row[5] for k,row in sounds.items() if min(row[4:6])>1020}
 stats=f'목표 {len(reg):,}편 · 본문 {len(available)}편 · 지정 Qwen 전체 음성 {len(sounds)}편 · 1.2배속 낭독만 17분 초과 {len(strict)}편 · 재생시간 검산 통과(대체 음성 포함) {len(verified)}편 · 이미지 연결 {sum(bool(info[k]["이미지"]) for k in available)}편 · 근거 일부 보류 {len(fact)}편'
 toc=['# TRUSTA AI 투자 실험실','',stats,'','[진행표](진행표.md) · [담당 분담 및 원문 기록](집필인계/분담기록.md) · [다른 세션 시작문](집필인계/다른세션_시작프롬프트.md)','','## 먼저 읽는 다섯 편','']
 for k in ['EP021','EP061','EP001','EP041','EP051']:
  if k in available:toc.append('- '+link(k,info[k]))
 groups={}
 for k in sorted(available):groups.setdefault(info[k]['분야'],[]).append(k)
 for g,ks in groups.items():
  toc+=['','## '+g,'']+['- '+link(k,info[k]) for k in ks]
 toc+=['','[첫 장문 낭독본](낭독본문/EP021.md) · [1.2배속 장면별 화면 큐시트](편집실/EP021_화면큐시트.md)','']
 atomic(R/'목차.md','\n'.join(toc))
 prog=['# 집필 진행표','',stats,'',sec,'','**다음 작업**　담당별로 원고와 낭독 검산 상태를 따로 확인한다. 근거 일부 보류 편은 아래 사유부터 재확인한다. 최초 105편을 제외한 확장 ID 배정은 [1,000편 분담표](집필인계/1000편_분담.csv)에 있다.','','|ID·담당|제목·원고|주요 질문|원문 링크|기준일 / 확인일|이미지 연결|팩트체크|17분 검수|','|---|---|---|---|---|---|---|---|']
 faq={'FAQ02':'ISA 원금 인출과 재납입 여력','FAQ04':'일일 목표와 누적 수익','FAQ05':'순매수와 보관잔액'}
 for k in order:
  own=reg[k]['담당 프롬프트']
  if k not in available:
   d=orig.get(k,{});title=d.get('제목',faq.get(k,k));q=d.get('첫훅',title);urls=d.get('원천URL','').split()
   refs=' · '.join('[자료 후보]('+u+')' for u in urls)
   prog.append(f'|{k} · {own}|{title}|{q}|{refs or "기존 EP 원문 확인 예정"}|담당 세션에서 확인|연결 전|초고 대기|대기|');continue
  r=info[k];refs=' · '.join('['+s['제목']+']('+s['URL']+')' for s in r['출처']);images=' · '.join('['+m['종류']+']('+m['파일']+')' for m in r['이미지']) or (k+' 연결 대기' if k.startswith('EP') else '독자질문편')
  length=f'{int(verified[k]//60)}분 {round(verified[k]%60)}초 PASS' if k in verified else '장문화·실측 대기'
  if k not in verified and r.get('음성상태','').endswith('합성 중'):
   length='8단계 장문 완성 · 지정 음성 합성 중' if '8단계' in r.get('장문진행','') else '지정 음성 합성 중'
  if k not in verified and '8단계' in r.get('장문진행','') and '합성 대기' in r.get('음성상태',''):
   length='8단계 장문 완성 · 지정 음성 합성 대기'
  if k in sounds:
   spoken=round(sounds[k][5])
   status='통과' if k in strict else '미달'
   length=f'지정 Qwen · 행간 제외 {spoken//60}분 {spoken%60}초 · {status}'
   if '보강' in r.get('음성상태','') and not sounds[k][0]:
    length+=' · 보강 전'
  prog.append('|'+ '|'.join([k+' · '+own,link(k,r),r['주요질문'],refs,r['기준']+' / '+r['확인일'],images,r['팩트체크'],length])+'|')
 atomic(R/'진행표.md','\n'.join(prog)+'\n')
 summary={'고유배정':len(reg),'담당배정':dict(Counter(v['담당 프롬프트'] for v in reg.values())),'고유본문':len(available),'원고별담당':dict(Counter(reg[k]['담당 프롬프트'] for k in available)),'초기105_원고대기':[k for k in initial if k not in available],'재생시간통과':verified,'지정Qwen전체음성':len(sounds),'지정Qwen낭독17분초과':strict,'이미지연결원고수':sum(bool(info[k]['이미지']) for k in available),'이미지':dict(counts),'근거일부보류':{k:info[k]['팩트체크'] for k in fact}}
 atomic(ED/'현황.json',json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 # A portable EPUB 3 contains the same chapters and images as the local Markdown.
 manifest=[]; spine=[];nav=[];imgpaths={};sections=[]
 css='body{font-family:serif;line-height:1.75;color:#182b3b;margin:5%} h1,h2{line-height:1.35} img{display:block;max-width:100%;max-height:78vh;height:auto;margin:1em auto} table{border-collapse:collapse;font-size:.85em}td,th{border-bottom:1px solid #aeb5be;padding:.32em;text-align:left}a{color:#144e79} p{orphans:2;widows:2}'
 def xhtml(title,body):return '<?xml version="1.0" encoding="utf-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="ko" xml:lang="ko"><head><title>'+H(title)+'</title><link rel="stylesheet" href="style.css"/></head><body>'+body+'</body></html>'
 for k in available:
  r=info[k];body=md.render((R/r['원고']).read_text())
  def image(m):
   p=unquote(html.unescape(m[1]));actual=R/p;assert actual.is_file(),actual
   if p not in imgpaths:imgpaths[p]='images/img'+str(len(imgpaths)+1)+actual.suffix.lower()
   return 'src="'+imgpaths[p]+'"'
  body=re.sub(r'src="([^"]+)"',image,body)
  def rep(m):
   z=unquote(html.unescape(m[1]));return 'href="'+('nav.xhtml' if z=='목차.md' else z[:-3]+'.xhtml')+'"' if z.endswith('.md') and not z.startswith('http') else m[0]
  body=re.sub(r'href="([^"]+)"',rep,body)
  title=r['제목'];section=xhtml(title,body);ET.fromstring(section);sections.append((k,section))
  manifest.append(f'<item id="{k}" href="{k}.xhtml" media-type="application/xhtml+xml"/>');spine.append(f'<itemref idref="{k}"/>')
 for g,ks in groups.items():
  nav.append('<li>'+H(g)+'<ol>'+''.join('<li><a href="'+k+'.xhtml">'+H(info[k]['제목'])+'</a></li>' for k in ks)+'</ol></li>')
 navdoc=xhtml('전자책 목차','<nav epub:type="toc" id="toc"><h1>TRUSTA AI 투자 실험실</h1><p>'+H(stats)+'</p><ol>'+''.join(nav)+'</ol></nav>')
 for i,n in enumerate(imgpaths.values()):manifest.append(f'<item id="img{i}" href="{n}" media-type="image/{"png" if n.endswith(".png") else "jpeg"}"/>')
 opf='<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book">urn:uuid:62c09c2d-b2fb-4ea7-89fb-44e385a69f54</dc:identifier><dc:title>TRUSTA AI 투자 실험실 · 편집 검토본</dc:title><dc:creator>TRUSTA 투자연구소</dc:creator><dc:language>ko</dc:language><meta property="dcterms:modified">2026-11-26T15:00:00Z</meta></metadata><manifest><item id="nav" properties="nav" href="nav.xhtml" media-type="application/xhtml+xml"/><item id="css" href="style.css" media-type="text/css"/>'+''.join(manifest)+'</manifest><spine><itemref idref="nav"/>'+''.join(spine)+'</spine></package>'
 final=R/'전자책_검토본.epub'
 with tempfile.NamedTemporaryFile(dir=R,delete=False) as tmp:tn=tmp.name
 with zipfile.ZipFile(tn,'w',compression=zipfile.ZIP_DEFLATED) as z:
  z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
  z.writestr('META-INF/container.xml','<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="OEBPS/book.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
  z.writestr('OEBPS/book.opf',opf);z.writestr('OEBPS/style.css',css);z.writestr('OEBPS/nav.xhtml',navdoc)
  for k,s in sections:z.writestr('OEBPS/'+k+'.xhtml',s)
  for p,n in imgpaths.items():z.write(R/p,'OEBPS/'+n)
 os.replace(tn,final)
 # Browser preview uses local anchors; Markdown files can still be opened separately in GNOME.
 head='<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>TRUSTA 투자 실험실 · 원고 검토</title><style>body{margin:2rem auto;max-width:800px;padding:0 1rem;font:17px/1.8 sans-serif;color:#182b3b}a{color:#15577a}details{border-bottom:1px solid #cad7dd;padding:.4rem}summary{cursor:pointer}h1,h2{line-height:1.35}img{display:block;max-width:100%;max-height:74vh;margin:auto}table{display:block;overflow:auto;border-collapse:collapse;font-size:.9em}td,th{padding:.28rem;border-bottom:1px solid #b2c3ca}small{color:#42576a}</style>'
 cards=[]
 for g,ks in groups.items():
  cards.append('<h2>'+H(g)+'</h2>')
  for k in ks:
   r=info[k];body=md.render((R/r['원고']).read_text());body=re.sub(r'href="((?:EP|FAQ)\d+)\.md"','href="#\\1"',body).replace('href="%EB%AA%A9%EC%B0%A8.md"','href="#contents"')
   cards.append('<details id="'+k+'"><summary>'+H(r['제목'])+'</summary>'+body+'</details>')
 js='function show(){let e=document.getElementById(location.hash.slice(1));if(e&&e.tagName==="DETAILS"){e.open=true;e.scrollIntoView()}}window.addEventListener("hashchange",show);show()'
 atomic(R/'원고_미리보기.html','<!doctype html><html lang="ko"><head>'+head+'</head><body><h1 id="contents">TRUSTA AI 투자 실험실</h1><p>'+H(stats)+'</p><p><a href="#EP021">계좌 비교 장문 읽기</a> · <a href="전자책_검토본.epub">전자책 검토본</a> · <a href="완성음성_재생실.html">완성 음성</a></p>'+''.join(cards)+'<script>'+js+'</script></body></html>')
 print(stats)
if __name__=='__main__':
 with (ED/'.목차.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);main()
  refresh_playback()

