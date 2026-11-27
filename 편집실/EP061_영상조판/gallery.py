from pathlib import Path
import html,json,re
from urllib.parse import unquote
from markdown_it import MarkdownIt
r=Path.cwd();d=r/'영상/EP061'
article=MarkdownIt('commonmark',{'html':False}).enable('table').render((r/'EP061.md').read_text())
def fix(m):
 attr,src=m.groups();return attr+'="'+('' if src.startswith(('http','#')) else '../../')+src+'"'
article=re.sub(r'(src|href)="([^"]+)"',fix,article)
complete=(d/'천억이_미국ETF_순매수.mp4').exists() and (r/'편집실/EP061_낭독검산.json').exists()
main='천억이_미국ETF_순매수.mp4' if complete else '도입_목소리미리듣기.mp4'
label='전체 영상' if complete else '먼저 듣는 도입'
record=''
if complete:
 h=json.loads((r/'편집실/EP061_낭독검산.json').read_text())
 def fmt(s):
  n=round(s);return f'{n//60}분 {n%60:02d}초'
 record='<p>기본 속도 '+fmt(h['일배속초'])+' · 1.2배속 '+fmt(h['영상1.2배속초'])+' · '+str(h['판정'])+'</p>'
else:record='<p>전체 내레이션 합성 중 · Qwen3-TTS-Base 자연스러운 v2 · voiceB</p>'
extra='<a href="천억이_한국어자막.srt" download>한국어 자막</a> <a href="../../음성/EP061_Qwen_v2/full.wav">전체 음성</a>' if complete else ''
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>천억이의 한 장 금융 만화 · 미국 ETF</title><style>*{box-sizing:border-box}body{margin:0;background:#f7f4ed;color:#22353a;font:18px/1.65 "NanumSquare",sans-serif}main{max-width:1110px;margin:0 auto;padding:24px clamp(16px,4vw,56px) 75px}header{border-bottom:2px solid #37504e;font-weight:800;display:flex;justify-content:space-between;color:#385753}h1,h2{line-height:1.25;letter-spacing:-.05em}h1{font-size:clamp(29px,5vw,52px)}figure{margin:0}img,video{max-width:100%;height:auto}figure img,video{display:block;width:100%;border:1px solid #b3ab96}video{background:#182e36;aspect-ratio:16/9}.links{display:flex;gap:.4em 1.3em;flex-wrap:wrap}a{color:#205853;text-underline-offset:4px}details{margin-top:20px;border-top:1px solid #a4a392;padding:18px 0}summary{font-weight:800;cursor:pointer}article{max-width:49em;margin:2em auto}article img{max-height:85vh;display:block;margin:1em auto}table{border-collapse:collapse}td,th{border-bottom:1px solid #ccc4ac;padding:.35em .6em}.vis{margin:1.5em 0}</style><main><header><span>TRUSTA 투자연구소</span><span>천억이의 금융 만화</span></header><h1>한 상품인데 이름이 왜 둘이야?</h1><figure><a href="천억이_한상품_두이름.png"><img src="천억이_한상품_두이름.png" alt="발행사의 긴 이름과 주문 기호를 비교하는 천억이의 말풍선 만화"></a></figure><h2>'''+label+'''</h2><video controls preload="metadata" playsinline src="'''+main+'''"></video>'''+record+'<div class="links"><a href="'+main+'" download>영상 저장</a><a href="천억이_한상품_두이름.png" download>가로 만화 저장</a><a href="../../낭독본문/EP061_Qwen_v2.jsonl" download>음성 대본 JSONL</a>'+extra+'</div><details><summary>전체 원고와 근거 자료 읽기</summary><article>'+article+'</article></details></main></html>'
page=page.replace('<h1>한 상품인데 이름이 왜 둘이야?</h1>','<h1>월간 1위가 마지막 주엔 사라졌다고?</h1>').replace('href="천억이_한상품_두이름.png"><img src="천억이_한상품_두이름.png" alt="발행사의 긴 이름과 주문 기호를 비교하는 천억이의 말풍선 만화"','href="천억이_순매수_생활그래프.png"><img src="천억이_순매수_생활그래프.png" alt="천억이와 수건 친구가 유리 원판을 붙잡고 달력을 넘긴다. 앰버빛 SOXL 조각은 월간 순매수액의 67.51%다."').replace('href="천억이_한상품_두이름.png" download>가로 만화 저장','href="천억이_순매수_생활그래프.png" download>생활 그래프 만화 저장')
shelf='<h2>화면에서 직접 따라 읽기</h2><section class="links">'
for filename,title,desc in [('세이브로_조회조건.png','세이브로 조회 조건','미국·순매수결제를 고르고 조회 기간을 바꾸는 실제 화면'),('운용사_하루목표.png','운용사 팩트시트','지시봉과 빨간 원으로 찾아가는 SOXL 하루 목표 300%'),('천억이_한상품_두이름.png','한 상품에 이름표 두 장','천억이와 수건 캐릭터가 티커와 정식명을 맞춰보는 사건 만화')]:
 shelf+='<figure style="flex:1 1 280px"><a href="'+filename+'"><img src="'+filename+'" alt="'+desc+'">'+title+'</a></figure>'
page=page.replace('<details><summary>',shelf+'</section><details><summary>')
if complete:
 mix=json.loads((r/'편집실/EP061_화면배분.json').read_text())
 cue=next((v['start'] for v in mix['cuts'] if v['key'].startswith('f4-') and v['type']=='ref'),0)
 page=page.replace('<video controls','<video id="player" controls').replace('<div class="links"><a href="'+main+'" download>', '<div class="links"><a href="'+main+'#t='+str(round(cue,2))+'" onclick="let v=document.querySelector(&quot;video&quot;);v.currentTime='+str(round(cue,2))+';v.play();v.scrollIntoView();return false">유리 원판 장면부터 재생</a><a href="'+main+'" download>')
page=page.replace('음성 대본 JSONL</a>', '음성 대본 JSONL</a><a href="../../전자책_검토본.epub" download>전자책 검토본</a>')
(d/'index.html').write_text(page)
