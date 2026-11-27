from pathlib import Path
import csv, datetime, hashlib, json, os, re, tempfile
from decimal import Decimal as D
from PIL import Image
pr=Path(__file__).resolve().parent
root=pr.parents[1]
def save(p,data):
 fd,n=tempfile.mkstemp(dir=p.parent)
 with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(data)
 os.replace(n,p)
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
with (root/'집필인계/1000편_분담.csv').open(encoding='utf-8-sig') as f:
 assert next(z for z in csv.DictReader(f) if z['ID']=='EP001')['담당 프롬프트']=='천억뷰'
raw='\n\n'.join((pr/f'원고_{s}.md').read_text().strip() for s in ['앞','중간','뒤'])
groups=re.split(r'(?m)^## ',raw)[1:];assert len(groups)==8
meta_file=root/'편집실/원고기록/EP001.json';meta=json.loads(meta_file.read_text());title=meta['제목']
article=['# '+title];narr=['# '+title];seq=[];lines=[]
def pieces(para):
 pieces=re.findall(r'[^.!?]+(?:[.!?]+[”’」]?|$)',para)
 pending=''
 for p in pieces:
  p=p.strip();s=(pending+' '+p).strip()
  if pending and len(s)>135:
   yield pending;pending=p
  else:pending=s
 if pending:yield pending
for stage,gr in enumerate(groups,1):
 head,*paras=gr.strip().split('\n\n');article+=['## '+head];narr+=['## '+head]
 for i,p in enumerate(paras):
  spoken=p.replace('ETF','이티에프');narr.append(spoken);article.append(p)
  for chunk in pieces(spoken):
   idx='L%04d'%(len(lines)+1);lines.append({'line_id':idx,'text':chunk});seq.append({'line_id':idx,'stage':stage,'para':i,'title':head,'text':chunk})
 if stage==1:
  article+=['![세 회사의 출발 비중 50%, 30%, 20%와 회사별 하락 충격을 보여 주는 세로 카드.](그림/EP001.png)','*가상 원금 10만 원. 같은 하루에 한 회사만 20% 내리는 세 가지 경우를 비교한다.*']
 if stage==2:
  article+=['| 첫날 움직인 회사 | 출발 노출 | 주가 −20%에 따른 손실 | ETF 기말 가치 |\n|---|---:|---:|---:|\n| A | 50,000원 | 10,000원 | 90,000원 |\n| B | 30,000원 | 6,000원 | 94,000원 |\n| C | 20,000원 | 4,000원 | 96,000원 |']
 if stage==3:article+=['미 SEC가 설명하는 장중 시장 가격과 순자산가치의 차이를 확인할 수 있다. [SEC 투자자 안내](https://www.investor.gov/introduction-investing/investing-basics/investment-products/mutual-funds-and-exchange-traded-2)']
 if stage==4:article+=['[FINRA 분산투자 안내](https://www.finra.org/investors/investing/investing-basics/asset-allocation-diversification)']
 if stage==6:article+=['**공시와 계산**　2026년 9월 30일 VOO의 엔비디아 비중은 8.4%, 상위 10개 합계는 40.6%다. 원화 100,000원 × 0.084 = 약 8,400원. 단위를 맞춘 설명용 환산이며 기준일 이후의 수익률은 가정하지 않았다. [Vanguard VOO 팩트시트 2쪽](https://institutional.vanguard.com/iippdf/pdfs/FS0968R.pdf)']
ref={'제목':'Vanguard VOO 팩트시트','URL':'https://institutional.vanguard.com/iippdf/pdfs/FS0968R.pdf'}
meta['출처']=[s for s in meta['출처'] if s['URL']!=ref['URL']]+[ref]
article+=['**원문**　'+' · '.join('['+x['제목']+']('+x['URL']+')' for x in meta['출처']),'**이어 읽기**　[한 상품의 두 분류](EP002.md) · [두 ETF에서 같은 회사가 겹칠 때](FAQ01.md) · [전자책 목차](목차.md)']
save(root/'EP001.md','\n\n'.join(article)+'\n');save(root/'낭독본문/EP001.md','\n\n'.join(narr)+'\n')
jsonl=root/'낭독본문/EP001_Qwen_v2.jsonl';contents=''.join(json.dumps(l,ensure_ascii=False)+'\n' for l in lines)
if jsonl.exists() and jsonl.read_text()!=contents and (root/'음성/EP001_Qwen_v2/raw').is_dir():raise RuntimeError('이미 시작된 음성과 다른 JSONL')
save(jsonl,contents);save(pr/'장면과낭독행.json',dump(seq))
assert len({r['line_id'] for r in seq})==len(seq) and max(len(x['text']) for x in seq)<230
src=pr/'VOO_팩트시트_원문.pdf';assert src.read_bytes()[:5]==b'%PDF-'
pct=list(map(D,['8.4','7.4','5.8','5.5','3.7','2.5','2.4','1.8','1.5','1.5']));assert sum(pct)==D('40.5')
assert [100000-w*D('.2') for w in [50000,30000,20000]]==[90000,94000,96000]
assert D(90000)-D(45000)*D('.1')==85500 and D(90000)-D(40000)*D('.1')==86000
assert D(100000)*pct[0]/100==8400 and D(100000)*D('.406')==40600
save(pr/'팩트체크.json',dump({'실측원문':ref,'원문sha256':sha(src),'관측일':'2026-09-30','확인일':datetime.date.today().isoformat(),'공표비중_퍼센트':{'NVIDIA':8.4,'상위10':40.6},'표시행합':str(sum(pct)),'가상조건':'원화 10만원·A50 B30 C20·세금·보수·거래비용·분배·환율변화 0. 별도 예시는 본문 조건별로 초기화','첫날각각20퍼센트하락_계좌원':[90000,94000,96000],'이틀째A10퍼센트하락_방치와재조정':[86000,85500]}))
meta.update({'답':'십만 원의 절반인 오만 원을 A에 담고 A만 하루 20% 내리면 일만 원 손실이다. 전일 금액·다른 자산·매매 조건을 바꾸면 답이 달라진다.','원고해시':sha(root/'EP001.md'),'기준':'가상 원금 100,000원 및 사례별 기간. VOO 편입 비중 실측 2026-09-30','확인일':datetime.date.today().isoformat(),'팩트체크':'SEC 구조·FINRA 분산 원문, Vanguard 공시 2쪽과 원화 환산·재조정 산식 대조','장문진행':'8단계 장문 원고·지정 음성용 JSONL 완성','낭독JSONL':str(jsonl.relative_to(root)),'음성상태':'Qwen 자연스러운 v2 합성 대기','다음장면':'지정 음성의 실제 길이와 자막·화면 확인 후 영상 기록 갱신'})
meta['이미지'][0].update({'위치':'첫 장 끝','대체텍스트':'가상 ETF의 세 회사 50%, 30%, 20% 편입 금액과 하루 하락 충격을 비교하는 세로 자료','캡션':'가상 원금 10만 원. 한 종목만 하루 20% 내리는 조건별 비교.'})
assert Image.open(root/'그림/EP001.png').size==(1080,1920)
save(meta_file,dump(meta));print(len(lines),sum(len(a['text']) for a in lines))
