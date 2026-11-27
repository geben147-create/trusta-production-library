from pathlib import Path
import json,hashlib,os,tempfile,re,csv
from decimal import Decimal
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
def save(path,body):
 fd,n=tempfile.mkstemp(dir=path.parent)
 with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(body)
 os.replace(n,path)
def jd(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pdf='https://assets.ctfassets.net/9gigg57dwmx9/funds-documents-qyld-fact-sheet_qyld-af2371ada8/19b9c4deab1c51478c64bbfaba382acf/Fact-Sheet_QYLD.pdf'
sec='https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/fund-distributions-investor-bulletin'
gx='https://www.globalxetfs.com/funds/qyld'
when='https://www.investor.gov/introduction-investing/investing-basics/glossary/ex-dividend-dates-when-are-you-entitled-stock-and'
report='https://www.sec.gov/Archives/edgar/data/1432353/000093041326000081/c114720_ncsr.htm'
sources=[('SEC 펀드 분배금 투자자 안내',sec),('Global X QYLD 팩트시트',pdf),('Global X QYLD 상품 설명·지급 이력',gx),('SEC 분배락일 안내',when),('SEC EDGAR Global X 주주보고서 · QYLD',report)]
case=[(1000,8500,1200000,9700000),(1000,8700,1200000,9900000),(1000,8800,1200000,10000000),(1000,8900,1200000,10100000)]
assert all(q*p+c==v for q,p,c,v in case) and (case[0][-1]-10000000)*100//10000000==-3
assert 101*8500+10100==868600 and 100*8500+20000==870000
assert 101*10500+10100==1070600 and 100*10500+20000==1070000
assert 1000*100*6+500*100*6==900000 and 8500000+600000==9100000
assert Decimal(120)/1000==Decimal('.12') and Decimal(11*100+50)==1150
with (R/'집필인계/1000편_분담.csv').open(encoding='utf-8-sig') as f:assert any(v['ID']=='EP041' and v['담당 프롬프트']=='천억뷰' for v in csv.DictReader(f))
assert Image.open(R/'그림/EP041.png').size==(1080,1920)
facts={'가상조건':'원화 세전, 비용·이자 0, 원래 사례는 미재투자·외부 입출금 없음, 연초 1천 주 × 1만 원, 월말 주당 100원씩 12회, 기말 분배 반영 후 8,500원','원화장부':case,'재투자_하락_현금과재투자':[870000,868600],'재투자_상승_현금과재투자':[1070000,1070600],'공시기준일':'2026-09-30','미국QYLD_팩트시트_해시':sha(P/'QYLD_팩트시트.pdf'),'원문관측':{'1쪽 최근12개월 분배율':12.11,'1쪽 1년 NAV 성과':22.94,'지급이력 2026-10 배당락일·지급일':['2026-10-19','2026-10-22']},'확인일':'2026-11-27','원문':[u for t,u in sources]}
raw=(P/'QYLD_추출.txt').read_text()
assert '12.11%' in raw and '22.94%' in raw and '9/30/2026' in raw
save(P/'원문과계산.json',jd(facts))
title='월분배금 120만 원을 받았는데, 왜 ETF에서 30만 원을 잃었을까?'
article=['# '+title];narr=['# '+title];seq=[];rows=[];counts=[]
addition={
1:['| 같은 1년의 가상 원화 장부 | 계산 | 금액 |\n|---|---|---:|\n| 연초 원금 | 1,000주 × 10,000원 | 10,000,000원 |\n| 받은 현금 | 1,000주 × 100원 × 12회 | 1,200,000원 |\n| 기말 ETF | 1,000주 × 8,500원 | 8,500,000원 |\n| 기말 총액 | ETF + 보관 현금 | 9,700,000원 |'],
2:['![첫 원금과 기말 ETF 평가액, 현금 분배금을 같은 시점에 비교하는 세로 카드](그림/EP041.png)','*가상 장부에서 현금은 원금의 12%, 단순 보유기간 수익률은 −3%다. 두 서랍이 손익분기를 이루는 기말 가격은 8,800원이다.*'],
3:['[SEC 펀드 분배금 투자자 안내]('+sec+')'],
4:['[Global X QYLD 분배 일정]('+gx+') · [SEC 분배락일 안내]('+when+')'],
5:['| 두 번 지급한 별도 실험 | 2차 지급 뒤 주가 8,500원 | 2차 지급 뒤 주가 10,500원 |\n|---|---:|---:|\n| 1차 지급을 현금으로 보관 | 870,000원 | 1,070,000원 |\n| 1차 지급으로 1주 매수 | 868,600원 | 1,070,600원 |\n| 재투자 경로에서 더 남은 돈 | −1,400원 | +600원 |'],
6:['**같은 기준일, 다른 질문**　2026년 9월 30일 미국 QYLD의 최근 12개월 분배율은 12.11%, 1년 NAV 성과는 22.94%였다. [Global X QYLD 팩트시트 1·2쪽]('+pdf+') · [Global X 상품 설명]('+gx+') · [SEC EDGAR QYLD 재투자 가정]('+report+')']}
def pieces(t):
 acc=''
 for bit in re.split(r'(?<=[.!?])(?=[”’]?\s)',t):
  bit=bit.strip()
  if not bit:continue
  if bit[0] in '”’' and acc:
   acc+=bit[0];bit=bit[1:].lstrip()
  if not bit:continue
  if acc and len(acc+' '+bit)>119:
   yield acc;acc=''
  acc=(acc+' '+bit).strip()
 if acc:yield acc
for g in range(1,9):
 lines=(P/f'장{g}.md').read_text().strip().split('\n\n');heading=lines[0];counts.append(len(lines)-1)
 article.append(heading);narr.append(heading)
 for p,body in enumerate(lines[1:]):
  article.append(body)
  spoken=body.replace('ETF','이티에프').replace('유튜브','유튜브')
  narr.append(spoken)
  for chunk in pieces(spoken):
   k=f'L{len(rows)+1:04d}';rows.append({'line_id':k,'text':chunk});seq.append({'line_id':k,'stage':g,'para':p,'title':heading[3:],'text':chunk})
 article.extend(addition.get(g,[]))
article+=['**원문**　'+' · '.join(f'[{n}]({u})' for n,u in sources),'**이어 읽기**　[분배율에 붙은 날짜와 분모](EP043.md) · [분배락 뒤 지급 전의 장부](FAQ03.md) · [전자책 목차](목차.md)']
assert all(len(row['text'])<190 for row in rows) and len(set(x['line_id'] for x in rows))==len(rows)
dest=R/'낭독본문/EP041_Qwen_v2.jsonl';data=''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows)
if dest.exists() and dest.read_text()!=data and (R/'음성/EP041_Qwen_v2/raw').exists():raise RuntimeError('음성 입력 변경 감지')
save(dest,data);save(P/'장면과낭독행.json',jd(seq));save(R/'EP041.md','\n\n'.join(article)+'\n');save(R/'낭독본문/EP041.md','\n\n'.join(narr)+'\n')
mfile=R/'편집실/원고기록/EP041.json';m=json.loads(mfile.read_text());m.update({'제목':title,'팩트체크':'SEC·Global X 공시와 기말 장부, 손익분기점·재투자 반례 산술 확인','기준':'원화 가상 1년 · QYLD 공시 관측 2026-09-30, 10월 지급 이력','확인일':'2026-11-27','출처':[{'제목':t,'URL':u} for t,u in sources],'장문진행':'8단계 장문 원고·지정 음성용 JSONL 완성','음성상태':'이전 지정 음성 작업 종료 뒤 합성 대기','낭독행수':len(rows),'원고해시':sha(R/'EP041.md'),'낭독해시':sha(R/'낭독본문/EP041.md'),'낭독JSONL해시':sha(dest),'답':'ETF 850만 원과 현금 120만 원이 합계 970만 원. 최초 1천만 원에 비해 30만 원 손실이다. 지출과 재투자는 각각 따로 대조한다.'})
m['이미지'][0].update({'대체텍스트':'최초 원금 1천만 원, 기말 ETF 850만 원과 분배금 120만 원을 대조한 세로 카드.','위치':'두 번째 장 끝, 손익분기 주가 계산 뒤','캡션':'같은 원금 기준의 현금 분배 비율은 12%, 미재투자 단순 보유기간 수익률은 −3%다.'})
save(mfile,jd(m));print(len(rows),sum(map(lambda x:len(x['text']),rows)),counts)
