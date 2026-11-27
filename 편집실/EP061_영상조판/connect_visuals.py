from pathlib import Path
import hashlib, json, os, shutil, tempfile, tomllib
from datetime import datetime
from urllib.parse import quote
t=Path(__file__).resolve().parent;r=Path.cwd();pr=r/'편집실/EP061_영상조판';source=r/'편집실/EP061_원문캡처'
def put(p,s):
 fd,n=tempfile.mkstemp(dir=p.parent)
 with os.fdopen(fd,'w') as out:out.write(s)
 os.replace(n,p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
meta_file=r/'편집실/원고기록/EP061.json';meta=json.loads(meta_file.read_text())
pdf='https://www.direxion.com/uploads/SOXL-SOXS-Fact-Sheet.pdf'
seibro=meta['출처'][0]['URL'];exact={'제목':'Direxion 반도체 ETF 팩트시트','URL':pdf}
if exact not in meta['출처']:meta['출처'].append(exact)
docs=[('EP061_세이브로_조회화면','16:9 세이브로 튜토리얼','천억이가 지시봉으로 가리키는 세이브로의 실제 조회 화면에서 순매수결제·미국이 선택되어 있고 조회기준일은 10월 1일~31일이다.','미국과 순매수결제를 그대로 둔 채 조회기준일만 바꾸면 같은 조건으로 월간과 주간을 비교할 수 있다.','## 열 개를 찾으려면 왜 열일곱 줄이 필요할까'),('EP061_월간순매수_생활그래프','16:9 생활 그래프 만화','천억이와 수건 캐릭터가 지시봉과 두 달력으로 월간과 마지막 주를 비교한다. 입체 막대 앞면에 SOXL 67.51%, 나머지 9개 32.49%가 표시돼 있다.','2026년 10월 1~31일, ETF 열 개의 순매수액에서 SOXL이 차지한 몫이다. 26~30일로 줄이면 ETF 중에서는 TQQQ가 첫째다.','## 달력을 닷새로 접었더니 첫째 줄이 사라졌다'),('EP061_운용사_투자목표','16:9 팩트시트 튜토리얼','두 인물이 Direxion 공식 팩트시트의 SOXL 열을 읽는다. 빨간 원과 화살표가 티커와 Daily Target 300%를 가리킨다.','같은 열에서 Fund Symbol과 Daily Target을 따라 읽는다. SOXL은 비용 전 지수의 하루 수익률 3배를 목표로 한다.','## 거래가 끝난 뒤 계좌에 남은 것')]
article=r/'EP061.md';s=article.read_text()
for slug,kind,alt,cap,anchor in docs:
 path='시각자료/'+slug+'.png';assert (r/path).is_file()
 if path not in s:s=s.replace(anchor,'!['+alt+']('+path+')\n\n'+cap+'\n\n'+anchor)
 meta['이미지']=[i for i in meta['이미지'] if i['파일']!=path]+[{'종류':kind,'원본':slug+'.png','파일':path,'대체텍스트':alt,'캡션':cap,'위치':anchor[3:]+' 소제목 직전'}]
if pdf not in s:s=s.replace('**원문**　','**원문**　[Direxion 반도체 ETF 팩트시트]('+pdf+') · ')
put(article,s);meta['원고해시']=sha(article);meta['가로화면정책']='생활-시각화-판단 80% / 사건 만화 12% / 원문 튜토리얼 8%. 모든 컷에 캐릭터, 차트는 정면 수치와 단위를 보존한 3D 표현.';put(meta_file,json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
proven={'확인일':datetime.now().date().isoformat(),'원문':[{'자료':'SEIBro 외화증권 종목별내역','URL':seibro,'원본':'ksd-original.png','SHA256':sha(source/'ksd-original.png'),'관측':'미국, 순매수결제, 2026-10-01~10-31 선택 후 조회 전 조건 화면. 금액은 별도로 저장한 조회 결과 사용.','강조':'라디오 버튼과 날짜 범위의 실제 좌표에 원·화살표를 올렸다.'},{'자료':'Direxion Semiconductor ETFs Fact Sheet, p.1','URL':pdf,'원본':'issuer.pdf','SHA256':sha(source/'issuer.pdf'),'강조':'PDF의 실제 Fund Symbol SOXL, Daily Target 300%를 확대했다.'}],'원자료검산':'../EP061_결제검산.json'}
put(source/'출처기록.json',json.dumps(proven,ensure_ascii=False,indent=2)+'\n')
for file in ['frame.html','finish_video.py','shots.py','gallery.py','slides.txt','public_visuals.py','buildmix.py','public-main.png','public-ksd.png','public-issuer.png','ksd-original.png','issuer.png','qseq.json','connect_visuals.py']:
 if (t/file).exists():shutil.copy2(t/file,pr/file)
for file in ['comic-0.jpg','comic-1.jpg','comic-2.jpg','comic-3.jpg','comic-4.jpg','comic-5.jpg','wide.png','pose0.png','pose1.png','pose2.png','sig.png',*[f's{i}.md' for i in range(1,9)]]:
 if (t/file).exists() and not (pr/file).exists():shutil.copy2(t/file,pr/file)
a=tomllib.loads((Path.home()/'.codex/automations/trusta-1-000/automation.toml').read_text())
put(r/'집필인계/이번세션_예약프롬프트.md','# 천억뷰 집필 예약\n\n'+a['prompt']+'\n')
