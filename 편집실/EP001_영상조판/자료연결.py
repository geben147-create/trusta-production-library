from pathlib import Path
from urllib.parse import quote,unquote
import sys, json, shutil, os, hashlib, re, html, tempfile
from markdown_it import MarkdownIt
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];D=R/'영상/EP001';D.mkdir(exist_ok=True)
def save(p,s):
 fd,n=tempfile.mkstemp(dir=p.parent)
 with os.fdopen(fd,'w',encoding='utf8') as f:f.write(s)
 os.replace(n,p)
def jd(z):return json.dumps(z,ensure_ascii=False,indent=2)+'\n'
def publish():
 article=R/'EP001.md';mfile=R/'편집실/원고기록/EP001.json';m=json.loads(mfile.read_text());s=article.read_text()
 items=[('16:9 세 접시 정보 만화',R/'시각자료/EP001_세접시_원화노출.png','세접시_편입비중.png','두 인물이 A·B·C에 분산한 십만 원을 살핀다. 유리 기둥은 오만·삼만·이만 원이고 A에서 만 원을 덜면 총액 구만 원이 남는다.','가상 원금 10만 원. A만 하루 20% 내리고 B와 C가 그대로일 때의 손실은 1만 원이다.','## 한 칸을 치우니 비중도 움직였다'),('16:9 운용사 원문 튜토리얼',R/'시각자료/EP001_VOO_보유비중_팩트시트.png','VOO_보유종목_원문.png','천억이와 수건 친구가 실제 VOO 팩트시트의 첫 보유종목 줄과 전체 순자산 대비 비중을 찾는다.','2026년 9월 30일 VOO의 엔비디아 비중은 8.4%. 가상 원금과 실제 관측 비중을 따로 읽는다.','## 어제 사진을 오늘 식탁에 대 봤더니')]
 for typ,src,local,alt,cap,anchor in items:
  if 'VOO' in local:shutil.copy2(P/'자료화면_검토.png',src)
  assert Image.open(src).size==(1920,1080)
  dest=D/local
  if not dest.exists() or not os.path.samefile(dest,src):
   tmp=D/(local+'.new');tmp.unlink(missing_ok=True);os.link(src,tmp);os.replace(tmp,dest)
  rel=str(src.relative_to(R))
  if rel not in s:s=s.replace(anchor,'!['+alt+']('+rel+')\n\n*'+cap+'*\n\n'+anchor)
  m['이미지']=[x for x in m['이미지'] if x['파일']!=rel]+[{'종류':typ,'원본':src.name,'파일':rel,'위치':anchor[3:]+' 직전','대체텍스트':alt,'캡션':cap}]
 save(article,s);m['원고해시']=hashlib.sha256(article.read_bytes()).hexdigest()
 v=R/'편집실/EP001_낭독검산.json';movie=D/'천억이_세접시_편입비중.mp4';ready=v.is_file() and movie.is_file()
 if ready:
  vr=json.loads(v.read_text());m['음성상태']='지정 Qwen 실제 합성 · MP4 완성';m['영상']=str(movie.relative_to(R));m['장문진행']='8단계 장문 완성 · 실제 음성 '+vr['판정']
 else:m['음성상태']='지정 Qwen 자연스러운 v2 voiceB 합성 중'
 preview_report=P/'도입검수.json'
 preview=None
 if preview_report.is_file():
  candidate=json.loads(preview_report.read_text());clip=D/candidate['파일']
  if candidate['검수']=='PASS' and clip.is_file():
   preview=candidate;m['도입미리보기']=str(clip.relative_to(R))
 save(mfile,jd(m))
 article_html=MarkdownIt('commonmark',{'html':False}).enable('table').render(s)
 def fix(mt):
  attr,url=mt.groups();return attr+'="'+('' if url.startswith(('http','#')) else '../../')+url+'"'
 article_html=re.sub(r'(src|href)="([^"]+)"',fix,article_html)
 def stamp(x):
  x=round(x);return f'{x//60}분 {x%60:02d}초'
 video=(f'<h2>가로 영상</h2><video controls preload="metadata" src="{movie.name}"></video><p>기본 {stamp(vr["일배속초"])} · 1.2배속 {stamp(vr["영상1.2배속초"])}</p><nav><a href="{movie.name}" download>영상 저장</a><a href="천억이_세접시_자막.srt" download>한국어 자막</a><a href="../../음성/EP001_Qwen_v2/full.wav">전체 음성</a></nav>') if ready else '<p>지정 Qwen 목소리로 전체 대본을 합성하고 있습니다.</p>'
 if preview and not ready:
  video=f'<h2>도입 먼저 보기</h2><video controls preload="metadata" src="{preview["파일"]}"></video><p>지정 목소리로 낭독한 첫 {preview["실측초"]:.1f}초입니다. 전체 음성을 합성하고 있습니다.</p>'
 page='<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+m['제목']+'</title><style>*{box-sizing:border-box}body{background:#f9f3e7;color:#322e29;font:18px/1.7 "NanumSquare",sans-serif;margin:0}main{max-width:1120px;margin:auto;padding:24px 4vw 60px}header{border-bottom:2px solid #4f4236;font-weight:800;color:#67553e}h1,h2{line-height:1.25;letter-spacing:-.04em}img,video{width:100%;height:auto;border-radius:5px}a{color:#225a57}nav{display:flex;gap:16px;flex-wrap:wrap}details{margin-top:25px;border-top:1px solid #c5b69c;padding:14px 0}summary{cursor:pointer;font-weight:800}article{max-width:48em;margin:auto}article img{max-width:100%;width:auto;max-height:74vh;display:block;margin:auto}td,th{padding:.3em;border-bottom:1px solid #cdbaa6}table{border-collapse:collapse}</style><main><header>TRUSTA 투자연구소　·　천억이의 금융 만화</header><h1>'+m['제목']+'</h1><a href="세접시_편입비중.png"><img src="세접시_편입비중.png" alt="'+items[0][3]+'"></a>'+video+'<nav><a href="VOO_보유종목_원문.png">운용사 공시 읽기</a><a href="../../낭독본문/EP001_Qwen_v2.jsonl" download>낭독 대본</a><a href="../../전자책_검토본.epub" download>전자책</a></nav><details open><summary>원고와 원문 읽기</summary><article>'+article_html+'</article></details></main></html>'
 save(D/'index.html',page)
if __name__=='__main__':publish()
