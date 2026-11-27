from pathlib import Path
import asyncio,base64,json,re,subprocess,time,urllib.request,itertools,math,shutil
import websockets
t=Path(__file__).resolve().parent
r=Path.cwd();shutil.copyfile(r/'시각자료/EP061_월간순매수_세로표.png',t/'original.png')
ev=json.loads((t/'events.json').read_text());titles=['주문창의 두 이름','영수증 속 영어','열일곱 줄의 원표','분모를 바꾼 실험','마지막 주의 반전','일일 배수의 대가','계좌에 남은 돈','다시 보는 사진']
slides=[[[*p.split('|')] for p in s.splitlines()] for s in (t/'slides.txt').read_text().strip().split('\n\n')]
def timestamp(n):
 msec=round(n*1000);return f'{msec//3600000:02d}:{msec//60000%60:02d}:{msec//1000%60:02d},{msec%1000:03d}'
from PIL import ImageFont
font=ImageFont.truetype('/home/yh/.local/share/fonts/kukppong-user-pack/533a202f020e-NanumSquareL.otf',35)
def wrap(s,limit):
 lines=[];line=''
 for word in s.split():
  new=(line+' '+word).strip()
  if line and font.getlength(new)>limit:lines.append(line);line=word
  else:line=new
 if line:lines.append(line)
 return lines
srt=[]; frames=[]; objects={};shots=[]; lastkey=None
for (g,p),grp in itertools.groupby(ev,lambda e:(e['stage'],e['para'])):
 group=list(grp); before=group[0]['start']; elapsed=0;v=0
 for j,e in enumerate(group):
  if j>0 and e['start']-before>=12:
   v=1-v;before=e['start']
  lines=wrap(e['text'],1060)
  chunks=[lines[i:i+2] for i in range(0,len(lines),2)]
  ticks=[sum(len(x) for x in g) for g in chunks];cum=0
  for c,n in zip(chunks,ticks):
   a=e['start']+(e['end']-e['start'])*cum/sum(ticks);cum+=n;b=e['start']+(e['end']-e['start'])*cum/sum(ticks)
   srt.append(str(len(srt)+1)+'\n'+timestamp(a)+' --> '+timestamp(b)+'\n'+'\n'.join(c))
  obj=[g,p,v,*slides[g-1][p],titles[g-1]]
  key=f'f{g}-{p}-{v}'
  if lastkey!=key:
   frames.append((e['start'],key));objects[key]=obj;lastkey=key
(t/'video.srt').write_text('\n\n'.join(srt)+'\n')
import bisect
T=float((t/'program-seconds.txt').read_text())
def at(g,p):
 return next(x['start'] for x in ev if (x['stage'],x['para'])==(g,p))
occupied=[]
def place(anchors,pct,mode):
 length=T*pct/len(anchors)
 for pref,source in anchors:
  gaps=[];last=0.
  for a,b,_,_ in sorted(occupied):
   if a-last+1e-7>=length:gaps.append((last,a-length))
   last=b
  if T-last+1e-7>=length:gaps.append((last,T-length))
  a=min((max(lo,min(hi,pref)) for lo,hi in gaps),key=lambda n: abs(n-pref));occupied.append((a,a+length,mode,source))
if T<100:
 place([(T*.58,'issuer')],.08,'doc');place([(0,'')],.12,'story')
else:
 place([(at(g,p)+off,source) for g,p,off,source in [(1,1,0,'issuer'),(1,6,1,'issuer'),(2,3,1,'ksd'),(3,0,1,'ksd'),(5,1,1,'ksd'),(6,0,3,'issuer'),(8,4,1,'ksd')]],.08,'doc')
 place([(at(g,p),'') for g,p in [(1,0),(1,2),(1,8),(2,0),(3,4),(4,0),(5,0),(6,4),(7,0),(8,5)]],.12,'story')
edges=sorted(set([0.,T]+[s for s,k in frames]+[q for a,b,_,_ in occupied for q in [a,b]]))
base_starts=[a for a,k in frames];newframes=[];newobjs={};runs=[];counts={'ref':0.,'story':0.,'doc':0.}
for a,b in zip(edges,edges[1:]):
 if b-a<1e-8:continue
 m=(a+b)/2;source='';mode='ref'
 for x,y,kind,file in occupied:
  if x<=m<y:mode=kind;source=file;break
 base=frames[bisect.bisect_right(base_starts,m)-1][1];k=base+'-'+mode+source
 if mode=='doc':k='document-'+source
 if not newframes or k!=newframes[-1][1]:newframes.append((a,k))
 newobjs[k]=objects[base]+[mode,source];counts[mode]+=b-a
 if runs and runs[-1]['key']==k:runs[-1]['end']=b
 else:runs.append({'start':a,'end':b,'key':k,'type':mode,'source':source})
objects=newobjs;frames=newframes
for mode,pct in [('ref',.8),('story',.12),('doc',.08)]:assert abs(counts[mode]/T-pct)<1e-6
(t/'mix.json').write_text(json.dumps({'total_seconds':T,'seconds':counts,'percent':{k:round(100*v/T,4) for k,v in counts.items()},'cuts':runs},ensure_ascii=False,indent=2))

for i,(a,key) in enumerate(frames):
 b=frames[i+1][0] if i+1<len(frames) else T
 shots.append(f"file '{key}.jpg'\noption framerate 24\nduration {b-a:.8f}\n")
(t/'concat.txt').write_text('ffconcat version 1.0\n'+''.join(shots)+f"file '{frames[-1][1]}.jpg'\noption framerate 24\n")
print('cuts',len(frames),'layouts',len(objects),'subtitle cues',len(srt),flush=True)
cmd=['google-chrome','--headless','--hide-scrollbars','--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--allow-file-access-from-files','--remote-allow-origins=*','--remote-debugging-port=0','--user-data-dir='+str(t/'frames-chrome'),(t/'frame.html').as_uri()]
proc=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
async def run():
 for _ in range(100):
  try:
   port=(t/'frames-chrome/DevToolsActivePort').read_text().splitlines()[0]
   tabs=json.load(urllib.request.urlopen('http://localhost:'+port+'/json/list'));url=next(x['webSocketDebuggerUrl'] for x in tabs if x['type']=='page');break
  except (OSError,StopIteration):await asyncio.sleep(.15)
 async with websockets.connect(url,max_size=16000000) as ws:
  counter=0
  async def call(method,params={}):
   nonlocal counter
   counter+=1;cid=counter;await ws.send(json.dumps({'id':cid,'method':method,'params':params}))
   while True:
    obj=json.loads(await ws.recv())
    if obj.get('id')==cid:
     if 'error' in obj:raise RuntimeError(obj)
     return obj['result']
  await call('Emulation.setDeviceMetricsOverride',dict(width=1280,height=720,deviceScaleFactor=1.5,mobile=False))
  for _ in range(100):
   res=await call('Runtime.evaluate',{'expression':'typeof show'})
   if res['result'].get('value')=='function':break
   await asyncio.sleep(.1)
  for key,obj in objects.items():
   js='(async()=>{await show('+json.dumps(obj,ensure_ascii=False)+');await Promise.all([...document.images].map(i=>i.decode()));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const board=document.getElementById("board");if(board.classList.contains("atelier")){const cr=board.querySelector(".asource"),ob=board.querySelector(".object");if(cr.getBoundingClientRect().bottom>598||ob.scrollHeight>ob.clientHeight+3)throw Error("atelier clip "+[cr.getBoundingClientRect().bottom,ob.scrollHeight,ob.clientHeight,board.innerText.slice(0,110)]);}else if(document.body.dataset.mode==="ref"&&document.body.dataset.plate!=="yes"){const st=board.querySelector(".split"),num=board.querySelector(".numbers"),credit=board.querySelector(".refcredit");if(credit.getBoundingClientRect().bottom>597||num.scrollHeight>num.clientHeight+3)throw Error("clip "+board.innerText.slice(0,80)+[credit.getBoundingClientRect().bottom,num.scrollHeight,num.clientHeight]);}return [document.getElementById("words").getBoundingClientRect().bottom,document.getElementById("capt").getBoundingClientRect().top];})()'
   res=await call('Runtime.evaluate',{'expression':js,'awaitPromise':True,'returnByValue':True});assert 'exceptionDetails' not in res,res
   a,b=res['result']['value'];assert a<b,(key,a,b)
   snap=await call('Page.captureScreenshot',{'format':'jpeg','quality':90,'fromSurface':True});(t/(key+'.jpg')).write_bytes(base64.b64decode(snap['data']))
try:asyncio.run(run())
finally:proc.terminate();proc.wait()
print('Rendered',len(objects),'video frames')
