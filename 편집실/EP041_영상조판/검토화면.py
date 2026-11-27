from pathlib import Path
import os,sys,re,json,hashlib,tempfile,shutil
from urllib.parse import unquote
from markdown_it import MarkdownIt
from PIL import Image
import html
P=Path(__file__).resolve().parent;R=P.parents[1];D=R/'영상/EP041';D.mkdir(exist_ok=True)
def save(p,s):
 fd,n=tempfile.mkstemp(dir=p.parent)
 with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(s)
 os.replace(n,p)
def jd(obj):return json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
def stamp(sec):
 n=round(sec);return f'{n//60}분 {n%60:02d}초'
def publish(start=False):
 a=R/'EP041.md';mf=R/'편집실/원고기록/EP041.json';m=json.loads(mf.read_text());body=a.read_text()
 specs=[('16:9 정보 만화','열두봉투_장부.png','시각자료/EP041_두서랍_월분배금.png','## 파란 수첩에서 사라진 돈','매표소에서 천억이와 수건 친구가 봉투와 ETF 수첩을 연다. 세 유리 기둥은 ETF 850만 원, 현금 120만 원, 합계 970만 원을 나타낸다.','가상 1년, 원화, 세금·비용·이자 0, 미재투자. 열두 번 받은 현금을 남은 ETF에 보태면 30만 원 손실이다.'),('16:9 공시 읽기','QYLD_분배율과성과.png','시각자료/EP041_QYLD_두항목.png','## 이미 써 버린 육십만 원은 어디에 적을까','두 인물이 Global X 팩트시트 원문에서 최근 열두 달 분배율과 1년 순자산가치 성과를 찾는다. 두 실제 공시 화면에 확인할 행과 열을 표시했다.','2026년 9월 30일 미국 QYLD. 최근 12개월 분배율 12.11%와 1년 NAV 성과 22.94%는 다른 질문에 답한다.')]
 for kind,file,rel,anchor,alt,cap in specs:
  src=D/file;dest=R/rel;assert Image.open(src).size==(1920,1080)
  if not dest.exists() or not os.path.samefile(src,dest):
   tmp=dest.with_suffix('.new');tmp.unlink(missing_ok=True);os.link(src,tmp);os.replace(tmp,dest)
  if rel not in body:body=body.replace(anchor,'!['+alt+']('+rel+')\n\n*'+cap+'*\n\n'+anchor)
  m['이미지']=[z for z in m['이미지'] if z['파일']!=rel]+[{'종류':kind,'원본':file,'파일':rel,'위치':anchor[3:]+' 직전','대체텍스트':alt,'캡션':cap}]
 save(a,body);m['원고해시']=hashlib.sha256(a.read_bytes()).hexdigest()
 vf=R/'편집실/EP041_낭독검산.json';movie=D/'열두봉투_월분배금과총수익.mp4'
 if vf.is_file() and movie.is_file():
  v=json.loads(vf.read_text());m['음성상태']='지정 Qwen v2 전체 합성 · 영상 완성';m['영상']=str(movie.relative_to(R));m['장문진행']='8단계 장문 완성 · 실제 음성 '+v['판정']
  video=f'<h2>지정 목소리로 듣기</h2><video controls preload="metadata" src="{movie.name}"></video><p>기본 {stamp(v["일배속초"])} · 1.2배속 {stamp(v["영상1.2배속초"])}</p><nav><a href="{movie.name}" download>영상 저장</a><a href="열두봉투_한국어자막.srt" download>한국어 자막</a></nav>'
 elif start or '합성 중' in m['음성상태']:
  m['음성상태']='지정 Qwen 자연스러운 v2 voiceB 합성 중'
  video='<p>지정 목소리로 전체 음성을 합성하고 있습니다.</p>'
 else:
  m['음성상태']='지정 음성 합성 대기 · EP001 후속'
  video='<p>전체 음성은 앞선 편의 합성이 끝나면 시작합니다.</p>'
 save(mf,jd(m))
 rendered=MarkdownIt('commonmark',{'html':False}).enable('table').render(body)
 rendered=re.sub(r'(href|src)="([^"]+)"',lambda mt:mt[1]+'="'+('' if mt[2].startswith(('http','#')) else '../../')+mt[2]+'"',rendered)
 page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>월분배금과 총수익 · TRUSTA</title><style>*{box-sizing:border-box}body{margin:0;background:#faf4e9;color:#352d29;font:18px/1.8 "Jalnan Gothic TTF",sans-serif}main{max-width:1120px;margin:auto;padding:25px clamp(14px,3vw,44px) 60px}header{border-bottom:2px solid #9f796e;padding-bottom:8px;font-weight:800;color:#85434a}h1,h2{line-height:1.25;letter-spacing:-.045em}a{color:#804344}nav{display:flex;gap:16px;flex-wrap:wrap;margin:10px 0 20px}img,video{max-width:100%;height:auto}article{max-width:49em;margin:auto}article img{max-height:80vh;display:block;margin:auto}th,td{text-align:left;border-bottom:1px solid #cbb8a8;padding:.35em}table{border-collapse:collapse;max-width:100%;font-size:.94em}details{margin-top:28px;border-top:1px solid #a88e80}summary{padding:10px 0;cursor:pointer;font-weight:800}</style><main><header>TRUSTA 투자연구소　·　천억이의 금융 만화</header><h1>'''+html.escape(m['제목'])+'</h1><a href="열두봉투_장부.png"><img src="열두봉투_장부.png" alt="'+specs[0][4]+'"></a>'+video+'<nav><a href="QYLD_분배율과성과.png">공시에서 두 줄 찾아보기</a><a href="../../낭독본문/EP041_Qwen_v2.jsonl" download>낭독 대본</a><a href="../../전자책_검토본.epub" download>전자책</a></nav><details open><summary>원고와 원문 읽기</summary><article>'+rendered+'</article></details></main></html>'
 save(D/'index.html',page)
if __name__=='__main__':publish('--합성중' in sys.argv)
