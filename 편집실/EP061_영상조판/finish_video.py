from pathlib import Path
import csv,random,json,sys,subprocess,shutil,wave,hashlib,os,datetime,re,zipfile,tempfile
t=Path(__file__).resolve().parent;r=Path.cwd();result=r/'영상/EP061';result.mkdir(parents=True,exist_ok=True)
preview=len(sys.argv)>1 and sys.argv[1]=='preview'
source=t/'preview-q' if preview else r/'음성/EP061_Qwen_v2'
inp=t/'preview-input.jsonl' if preview else r/'낭독본문/EP061_Qwen_v2.jsonl'
entries=[json.loads(z) for z in inp.read_text().splitlines() if z.strip()]
seq=json.loads((t/'qseq.json').read_text())[:len(entries)];timeline=[]
def info(p):
 with wave.open(str(p),'rb') as f:return f.getnframes(),f.getframerate()
N,rate=info(source/'full.wav');ticks=0;rng=random.Random(7);speech=0
rows=list(csv.DictReader((source/'report.csv').open()))
assert len(rows)==len(entries)
for event,entry,row in zip(seq,entries,rows):
 assert event['line_id']==row['line_id']==entry['line_id']
 frames,sr=info(source/(entry['line_id']+'.wav'));assert sr==rate;speech+=frames
 gap=rng.uniform(.35,.65)
 if entry['text'].rstrip().endswith(('?','？')):gap=.7
 s=event['sentences'];weights=[len(x) for x in s];frac=0
 for j,(z,weight) in enumerate(zip(s,weights)):
  a=(ticks+frames*frac/sum(weights))/sr;frac+=weight;b=(ticks+frames*frac/sum(weights))/sr
  timeline.append(dict(stage=event['stage'],para=event['para'],text=z,start=a,end=b))
 ticks+=frames+int(gap*sr)
assert ticks==N,(ticks,N)
(t/'events.json').write_text(json.dumps(timeline,ensure_ascii=False))
(t/'program-seconds.txt').write_text(str(N/rate))
subprocess.run([sys.executable,str(t/'shots.py')],check=True)
secs=N/rate
def ms(v):return round(v*1000)
rom=[';FFMETADATA1','title=한 상품인데 이름이 왜 둘일까? · 천억이의 금융 만화','artist=TRUSTA 투자연구소']
cues=[]
for i in range(1,9):
 ev=[x for x in timeline if x['stage']==i]
 if not ev:continue
 end=next((x['start'] for x in timeline if x['stage']>i),secs);start=ev[0]['start']
 ch=(t/f's{i}.md').read_text().splitlines()[0][3:]
 cues.append([i,ch,start,end])
 rom+=['[CHAPTER]','TIMEBASE=1/1000',f'START={ms(start)}',f'END={ms(end)}','title='+ch]
(t/'chapters.txt').write_text('\n'.join(rom)+'\n')
target=result/('도입_목소리미리듣기.mp4' if preview else '천억이_미국ETF_순매수.mp4')
build=t/('preview-ready.mp4' if preview else 'qwen-ready.mp4')
common=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-f','concat','-safe','0','-i','concat.txt','-i',str(source/'full.wav'),'-f','ffmetadata','-i','chapters.txt','-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-vf',"fps=24,subtitles=video.srt:force_style='FontName=NanumSquare,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H0021323A,Bold=0,Outline=0.6,Shadow=0,MarginV=9,Alignment=2',format=yuv420p"]
out=['-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-t',f'{secs:.8f}',str(build)]
cmd=common+['-c:v','h264_nvenc','-gpu','0','-preset','p4','-rc','vbr','-cq','24','-b:v','0']+out
if subprocess.run(cmd,cwd=t).returncode:
 subprocess.run(common+['-c:v','libx264','-preset','veryfast','-crf','22','-threads','6']+out,cwd=t,check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(build)]))
vs=next(x for x in probe['streams'] if x['codec_type']=='video');au=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (vs['width'],vs['height'],vs['codec_name'],au['codec_name'])==(1920,1080,'h264','aac')
assert abs(float(au['duration'])-secs)<.12 and abs(float(vs['duration'])-secs)<.1 and len(probe['chapters'])==len(cues)
subprocess.run(['ffmpeg','-nostats','-v','error','-xerror','-i',str(build),'-map','0:a','-f','null','-'],check=True)
tempdest=target.with_suffix('.working');shutil.copy2(build,tempdest);os.replace(tempdest,target)
if preview:
 print('PREVIEW',secs,target,flush=True);sys.exit(0)
shutil.copy2(t/'video.srt',result/'천억이_한국어자막.srt')
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
 fd,n=tempfile.mkstemp(dir=p.parent)
 with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(obj)
 os.replace(n,p)
def jd(z):return json.dumps(z,ensure_ascii=False,indent=2)+'\n'
ed=r/'편집실';spoken_seconds=speech/rate; passed=spoken_seconds/1.2>1020
verify={'원고':'EP061.md','sha256':digest(r/'낭독본문/EP061.md'),'한국어음성':'Qwen3-TTS-Base 자연스러운 v2 / voiceB','기본속도':'원본','샘플레이트':rate,'JSONLsha256':digest(inp),'전체WAVsha256':digest(source/'full.wav'),'표본수':N,'행간제외표본수':speech,'일배속초':round(secs,3),'배속':1.2,'재생초':round(spoken_seconds/1.2,3),'영상1.2배속초':round(secs/1.2,3),'요건초':1020,'판정':'PASS' if passed else '미달','동영상':{'규격':'1920×1080 H.264/AAC','원본초':float(vs['duration']),'오디오초':float(au['duration']),'마스터링목표LUFS':-12,'파일':str(target.relative_to(r))}}
mix=json.loads((t/'mix.json').read_text());verify['화면시간비중']=mix['percent'];verify['화면컷수']=len(mix['cuts']);save(ed/'EP061_화면배분.json',jd(mix));save(ed/'EP061_낭독검산.json',jd(verify))
meta_p=ed/'원고기록/EP061.json';meta=json.loads(meta_p.read_text())
meta.update({'음성상태':'Qwen v2 voiceB 실제 음성·MP4 완료','영상':str(target.relative_to(r)),'시각원화':'집필인계/천억이_시그니처표정.png'})
save(meta_p,jd(meta))
def stamp(t):
 sec=round(t);return f'{sec//60:02d}:{sec%60:02d}'
directions=['도입에서 수건 캐릭터가 짧은 표를 받고 천억이가 긴 표를 잡는다. 입이 크게 벌어지는 반전과 둘의 말풍선을 잇는다. 차례로 티커, 정식명, SOXX 반례, VOO 두 분류를 나눈다.','발목을 감싼 영수증을 풀며 매수·매도·순매수 세 금액을 유리 기둥에 대응시킨다.','9:16 카드 전체 비율을 유지한다. 전체 17줄에서 ETF 10줄로 초점을 옮긴다.','두 인물이 굴러가는 유리 원판을 붙잡는다. 열 종목의 순매수액을 앰버·투명 조각으로 나누고, 분모를 바꾸는 대목에서 크리스털 기둥으로 비교한다.','한 달과 닷새를 가로로 놓고 빈칸의 정확액 미상을 짙은 빨강으로 보인다.','운용사 원문에서 일일 목표를 가리킨 뒤, 100달러로 출발하는 이틀 경로를 입체 기둥과 연결선으로 읽는다.','순매수와 월말 잔액을 말풍선, 두 열로 된 장부로 읽는다.','첫 컷의 두 인물과 한 서류철에 달린 이름표로 복귀한다. 날짜와 단위를 짚고 끝낸다.']
circ=['일상','필요','진입','탐색','발견','대가','귀환','변화']
cue=['# 천억이의 두 이름 · 가로 영상 큐시트','','지정 Qwen3-TTS-Base 자연스러운 v2 voiceB의 줄별 WAV와 간격을 합산했다. 시간은 1배속 영상 및 플레이어 1.2배속 기준이다. 독자용 화면에는 제작 ID나 회차를 넣지 않았다.','','|기본 재생|1.2배 재생|하몬 단계|장면·화면|','|---|---|---|---|']
for i,ch,a,b in cues:cue.append(f'|{stamp(a)}–{stamp(b)}|{stamp(a/1.2)}–{stamp(b/1.2)}|{circ[i-1]}|{ch} · {directions[i-1]}|')
save(ed/'EP061_화면큐시트.md','\n'.join(cue)+'\n');subprocess.run([sys.executable,str(ed/'목차갱신.py')],check=True)
subprocess.run([sys.executable,str(t/'gallery.py')],check=True)
print('FINAL',verify,flush=True)
