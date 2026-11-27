from pathlib import Path
from PIL import Image,ImageStat,ImageChops,ImageDraw
import csv, io,json,hashlib,subprocess,re,tempfile,math,concurrent.futures,zipfile,wave,datetime,sqlite3,tomllib
t=Path(__file__).resolve().parent;r=Path.cwd();ed=r/'편집실';d=r/'영상/EP061';p=d/'천억이_미국ETF_순매수.mp4';video=json.loads(subprocess.check_output(['ffprobe','-v','error','-of','json','-show_streams','-show_format','-show_chapters',str(p)]))
mix=json.loads((ed/'EP061_화면배분.json').read_text());h=json.loads((ed/'EP061_낭독검산.json').read_text());m=json.loads((ed/'원고기록/EP061.json').read_text());usd=json.loads((ed/'EP061_결제검산.json').read_text())
def sha(p):return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
assert sha(r/'EP061.md')==m['원고해시'];assert sha(r/'낭독본문/EP061.md')==h['sha256']
assert len(video['chapters'])==8 and h['화면컷수']==len(mix['cuts']) and h['판정']=='PASS' and h['재생초']>1020
v,a=video['streams'][:2];assert (v['width'],v['height'],v['codec_name'],a['codec_name'])==(1920,1080,'h264','aac');assert abs(float(v['duration'])-mix['total_seconds'])<.05
price=usd['월간']['전체50'];week=usd['주간']['전체50'];assert len(price)==50 and len(week)==50
ranks=usd['월간']['ETF상위10'];amt=lambda row:int(row['SUM_FRSEC_NET_BUY_AMT'])
top=sum(amt(price[i-1]) for i in ranks.values());soxl=amt(price[ranks['SOXL']-1]);assert round(soxl/top*100,2)==67.51 and round((top-soxl)/top*100,2)==32.49 and round(soxl/sum(map(amt,price))*100,2)==44.07
assert price[0]['ISIN'] not in [x['ISIN'] for x in week] and amt(week[3])==104961242
assert all((r/i['파일']).is_file() for i in m['이미지'])
actual=(d/'index.html').read_text();assert all(j in actual for j in [p.name,'운용사_하루목표.png','세이브로_조회조건.png','천억이_순매수_생활그래프.png'])
with zipfile.ZipFile(r/'전자책_검토본.epub') as book:
 ch=[n for n in book.namelist() if n.lower().endswith('ep061.xhtml')];assert ch,ch
 chapter=book.read(ch[0]).decode();assert chapter.count('<img')>=len(m['이미지'])
cuts=mix['cuts']
def capture(it):
 idx,c=it;time=(c['start']+c['end'])/2
 args=['ffmpeg','-v','error','-threads','1','-ss',f'{time:.5f}','-i',str(p),'-frames:v','1','-vf','scale=384:216','-f','image2pipe','-vcodec','png','-threads','1','-']
 got=Image.open(io.BytesIO(subprocess.check_output(args))).convert('RGB')
 expected=Image.open(t/(c['key']+'.jpg')).convert('RGB').resize((384,216),Image.Resampling.LANCZOS)
 region=(0,0,384,175);diff=ImageStat.Stat(ImageChops.difference(got.crop(region),expected.crop(region))).mean;error=sum(diff)/3
 return idx,c['key'],round(time,3),round(error,3),got
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 checks=list(pool.map(capture,enumerate(cuts)))
bad=[(i,k,tt,err) for i,k,tt,err,im in checks if err>=8];assert not bad,bad
select=[]
for match in ['f1-0-0-story','document-issuer','f2-3-0-ref','document-ksd','f4-1-0-ref','f6-2-0-ref','f7-1-0-ref','f8-5-0-story']:
 found=next((el for el in checks if el[1]==match),None)
 if found:select.append(found)
sheet=Image.new('RGB',(384*2,216*math.ceil(len(select)/2)),(36,43,42))
for j,el in enumerate(select):sheet.paste(el[-1],(j%2*384,j//2*216))
sheet.save(ed/'EP061_인코딩화면검수.jpg',quality=92)
rec={'파일':p.name,'sha256':sha(p),'규격':[v['width'],v['height']],'fps':v['avg_frame_rate'],'챕터':len(video['chapters']),'음성구간':sum(1 for l in (r/'낭독본문/EP061_Qwen_v2.jsonl').read_text().splitlines() if l.strip()),'검수컷':len(checks),'검수':'각 컷 중간의 실제 MP4 상단을 조판 JPEG와 비교 · 0~255 스케일에서 평균 채널차이','최대평균차이':max(el[3] for el in checks),'도해가있는전자책이미지':chapter.count('<img'),'누적편집시간초':mix['seconds'],'실제영상초':float(v['duration']),'검수컷별':[[a,b,c,d] for a,b,c,d,_ in checks],'판정':'PASS'}
(ed/'EP061_가로영상검수.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
print({k:v for k,v in rec.items() if k!='검수컷별'})
