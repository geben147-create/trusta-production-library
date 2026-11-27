from pathlib import Path
import bisect, csv, hashlib,json,math,os,random,re,shutil,subprocess,sys,tempfile,wave
from collections import Counter
from PIL import Image,ImageChops,ImageStat
from 페이지 import P,R,C,titles
from 검토화면 import D,publish,save,jd
from 컷렌더 import render
preview='--도입' in sys.argv
src=(P/'도입합성') if preview else (R/'음성/EP041_Qwen_v2');build=P/('도입편집' if preview else '전체편집');build.mkdir(exist_ok=True)
seq=json.loads((P/'장면과낭독행.json').read_text());report=list(csv.DictReader((src/'report.csv').open()));rows=seq[:len(report)] if preview else seq
assert len(rows)==len(report)
def wav(x):
 with wave.open(str(x)) as f:return f.getnframes(),f.getframerate()
def sha(x):
 with x.open('rb') as fp:return hashlib.file_digest(fp,'sha256').hexdigest()
def ts(s):
 n=round(s*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
def short(s):
 n=round(s);return f'{n//60:02d}:{n%60:02d}'
def subs(s):
 out=[];cur=''
 for word in s.split():
  if cur and len(cur)+1+len(word)>31:out.append(cur);cur=''
  cur=(cur+' '+word).strip()
 if cur:out.append(cur)
 return ['\n'.join(out[i:i+2]) for i in range(0,len(out),2)]
rng=random.Random(7);N,sr=wav(src/'full.wav');cursor=0;speech=0;subtitle=[];base=[];anchors={};last=None;prev=0
for row,rec in zip(rows,report):
 line=row['line_id'];assert line==rec['line_id'];n,rate=wav(src/(line+'.wav'));assert rate==sr and abs(float(rec['seconds'])-n/sr)<.006
 g,p=row['stage'],row['para'];start=cursor/sr;anchors.setdefault((g,p),start)
 chunks=subs(row['text']);weights=[len(c.replace('\n','')) for c in chunks];acc=0;wg=sum(weights)
 for j,(c,w) in enumerate(zip(chunks,weights)):
  a=start+n*acc/wg/sr;acc+=w;b=start+n*acc/wg/sr
  subtitle.append(str(len(subtitle)+1)+'\n'+ts(a)+' --> '+ts(b)+'\n'+c)
  if (g,p)!=last:last=(g,p);v=0;prev=a;base.append((a,(g,p,v)))
  elif a-prev>=11:prev=a;v=1-v;base.append((a,(g,p,v)))
 gap=rng.uniform(.35,.65)
 if row['text'].rstrip().endswith(('?','？')):gap=.7
 assert abs(float(rec['gap_after'])-gap)<.006
 cursor+=n+int(gap*sr);speech+=n
assert cursor==N
total=N/sr;regions=[]
def allocate(points,fraction,kind):
 width=total*fraction/len(points)
 for when in points:
  gaps=[];end=0
  for a,b,_ in sorted(regions):
   if a-end>=width:gaps.append((end,a-width))
   end=b
  if total-end+1e-7>=width:gaps.append((end,total-width))
  begin=min((min(max(when,lo),hi) for lo,hi in gaps),key=lambda x:abs(x-when));regions.append((begin,begin+width,kind))
if preview:allocate([0],.12,'story')
else:
 allocate([anchors[k] for k in [(6,i) for i in range(5)]],.08,'doc')
 allocate([anchors[k] for k in [(1,0),(2,0),(3,0),(4,0),(5,0),(6,7),(7,0),(8,6)]],.12,'story')
edges=sorted({0,total,*[a for a,k in base],*[k for a,b,kind in regions for k in (a,b)]});starts=[a for a,obj in base]
runs=[];totals=Counter();inputs=set()
for a,b in zip(edges,edges[1:]):
 if b-a<.0001:continue
 mid=(a+b)/2;g,p,v=base[bisect.bisect_right(starts,mid)-1][1];mode=next((kind for l,r,kind in regions if l<=mid<r),'ref')
 if mode=='doc':
  doc_positions=[(6,i) for i in range(5)]
  g,p=min(doc_positions,key=lambda gp:abs(anchors[gp]-mid));v=0
 key=(g,p,v,mode);inputs.add(key);totals[mode]+=b-a
 if runs and runs[-1][2]==key:runs[-1][1]=b
 else:runs.append([a,b,key])
if not preview:
 for k,val in [('ref',.8),('story',.12),('doc',.08)]:assert abs(totals[k]/total-val)<.0001
render(inputs)
def path(key):
 g,p,v,mode=key;return C/f's{g:02d}-{p:02d}-{v}-{mode}.jpg'
seqfile=['ffconcat version 1.0']
for a,b,key in runs:
 escaped=str(path(key)).replace("'","'\\''");seqfile.extend(["file '"+escaped+"'","option framerate 24",f'duration {b-a:.8f}'])
seqfile+=["file '"+str(path(runs[-1][2]))+"'","option framerate 24"]
(build/'concat.txt').write_text('\n'.join(seqfile)+'\n');(build/'자막.srt').write_text('\n\n'.join(subtitle)+'\n');chap=[';FFMETADATA1','title=월분배금과 매표소의 두 서랍','artist=TRUSTA 투자연구소']
stages=sorted({x['stage'] for x in rows});chapters=[]
for i,g in enumerate(stages):
 a=anchors[(g,0)];b=anchors[(stages[i+1],0)] if i+1<len(stages) else total;chapters.append((g,a,b));chap+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(a*1000)}',f'END={round(b*1000)}','title='+titles[g-1]]
(build/'chapters.txt').write_text('\n'.join(chap)+'\n')
name='도입_열두봉투.mp4' if preview else '열두봉투_월분배금과총수익.mp4';dest=D/name;temp=build/'편집중.mp4'
cmd=['ffmpeg','-nostdin','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i','concat.txt','-i',str(src/'full.wav'),'-f','ffmetadata','-i','chapters.txt','-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-vf',"fps=24,subtitles=자막.srt:force_style='FontName=Jalnan Gothic TTF,FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H0021323A,Outline=0.7,Shadow=0,MarginV=9,Alignment=2',format=yuv420p"]
out=['-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-t',f'{total:.8f}',str(temp)]
if subprocess.run(cmd+['-c:v','h264_nvenc','-gpu','0','-preset','p4','-cq','23','-b:v','0']+out,cwd=build).returncode:subprocess.run(cmd+['-c:v','libx264','-preset','veryfast','-crf','22','-threads','6']+out,cwd=build,check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_chapters','-of','json',str(temp)]))
vs=next(x for x in probe['streams'] if x['codec_type']=='video');au=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (vs['width'],vs['height'],vs['codec_name'],au['codec_name'])==(1920,1080,'h264','aac') and len(probe['chapters'])==len(stages)
assert abs(float(au['duration'])-total)<.08 and abs(float(vs['duration'])-total)<.1
# Each chapter and each type of scene must survive MP4 encoding at its intended time.
targets={next(i for i,t in enumerate(runs) if t[2][0]==g) for g in stages}
targets.update(next(i for i,t in enumerate(runs) if t[2][3]==kind) for kind in totals)
for i in sorted(targets):
 a,b,key=runs[i];clock=(a+b)/2;bytes_=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-ss',str(clock),'-i',str(temp),'-frames:v','1','-vf','scale=384:216','-f','rawvideo','-pix_fmt','rgb24','-'])
 got=Image.frombytes('RGB',(384,216),bytes_);ref=Image.open(path(key)).convert('RGB').resize((384,216),Image.Resampling.LANCZOS);err=sum(ImageStat.Stat(ImageChops.difference(got,ref).crop((0,0,384,175))).mean)/3;assert err<9,(i,err)
os.replace(temp,dest)
if preview:
 save(P/'도입검수.json',jd({'파일':name,'실측초':total,'Qwen행수':len(rows),'검수':'PASS'}));publish();print('도입 PASS',total,flush=True);sys.exit()
shutil.copy2(build/'자막.srt',D/'열두봉투_한국어자막.srt')
verification={'원고':'EP041.md','sha256':sha(R/'낭독본문/EP041.md'),'JSONLsha256':sha(R/'낭독본문/EP041_Qwen_v2.jsonl'),'전체WAVsha256':sha(src/'full.wav'),'한국어음성':'Qwen3-TTS-Base 자연스러운 v2 / voiceB','샘플레이트':sr,'표본수':N,'행간제외표본수':speech,'일배속초':round(total,3),'배속':1.2,'재생초':round(speech/sr/1.2,3),'영상1.2배속초':round(total/1.2,3),'요건초':1020,'판정':'PASS' if speech/sr>1224 else '미달','동영상':{'파일':str(dest.relative_to(R)),'출력규격':'1920×1080 H.264/AAC','sha256':sha(dest),'검수한영상표본수':len(targets)},'화면비중':{k:round(v/total*100,3) for k,v in totals.items()}}
save(R/'편집실/EP041_낭독검산.json',jd(verification));save(P/'컷시간.json',jd(runs))
cue=['# 매표소의 두 서랍 · 화면 큐시트','','기준은 실제 지정 음성의 WAV 표본과 줄별 간격이다. 한 낭독 행 안에서 자막은 문장 길이에 비례하여 나눴다.','','|기본 속도|1.2배속|장면|','|---|---|---|']
for g,a,b in chapters:cue.append(f'|{short(a)}–{short(b)}|{short(a/1.2)}–{short(b/1.2)}|{titles[g-1]}|')
save(R/'편집실/EP041_화면큐시트.md','\n'.join(cue)+'\n');publish();subprocess.run([sys.executable,str(R/'편집실/목차갱신.py')],check=True);print('전체 영상',verification['판정'],verification['재생초'],dest,flush=True)
