from pathlib import Path
import asyncio,base64,json,subprocess,tempfile,urllib.request,re,hashlib,os
from 페이지 import page,outline,P,C
import websockets
from PIL import Image
import io
def render(entries):
 tasks={}
 for (g,p,v,mode) in entries:
  key=f's{g:02d}-{p:02d}-{v}-{mode}';markup=page(g,p,v,mode)
  digest=hashlib.sha256(markup.encode()).hexdigest()
  file=C/(key+'.jpg');sig=C/(key+'.sha256')
  if file.exists() and sig.exists() and sig.read_text()==digest:continue
  tasks[key]=(markup,digest)
 if not tasks:return
 with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
  tmp=Path(tmp);start=P/'빈페이지.html'
  if not start.exists():start.write_text('<!doctype html><meta charset="utf-8">')
  chrome=subprocess.Popen(['google-chrome','--headless','--no-sandbox','--hide-scrollbars','--disable-gpu','--disable-dev-shm-usage','--allow-file-access-from-files','--remote-allow-origins=*','--remote-debugging-port=0','--user-data-dir='+str(tmp),start.as_uri()],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  async def run():
   url=None
   for _ in range(100):
    try:
     port=(tmp/'DevToolsActivePort').read_text().splitlines()[0];tabs=json.load(urllib.request.urlopen('http://127.0.0.1:'+port+'/json/list'));url=next(x['webSocketDebuggerUrl'] for x in tabs if x['type']=='page');break
    except (OSError,StopIteration):await asyncio.sleep(.1)
   if not url:raise RuntimeError('컷 렌더 브라우저 연결 실패')
   async with websockets.connect(url,max_size=12_000_000) as ws:
    index=0
    async def call(method,params):
     nonlocal index
     index+=1;cid=index;await ws.send(json.dumps({'id':cid,'method':method,'params':params}))
     while True:
      res=json.loads(await ws.recv())
      if res.get('id')==cid:
       if 'error'in res:raise RuntimeError(res['error'])
       return res['result']
    await call('Emulation.setDeviceMetricsOverride',dict(width=1280,height=720,deviceScaleFactor=1.5,mobile=False))
    for key,(markup,digest) in tasks.items():
     expression='(async()=>{document.open();document.write('+json.dumps(markup,ensure_ascii=False)+');document.close();await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const a=document.querySelector(".source"), cap=document.querySelector(".cap"), obj=document.querySelector(".proof");return [a.getBoundingClientRect().bottom,cap.getBoundingClientRect().top,obj.scrollHeight,obj.clientHeight]})()'
     res=await call('Runtime.evaluate',dict(expression=expression,awaitPromise=True,returnByValue=True))
     if 'exceptionDetails'in res:raise RuntimeError((key,res['exceptionDetails']))
     b,top,sh,ch=res['result']['value']
     if b>top-1 or sh>ch+4:raise RuntimeError((key,'overflow',b,top,sh,ch))
     snap=await call('Page.captureScreenshot',dict(format='jpeg',quality=92,fromSurface=True));data=base64.b64decode(snap['data'])
     assert Image.open(io.BytesIO(data)).size==(1920,1080);tmpfile=C/(key+f'.{os.getpid()}.jpg');tmpfile.write_bytes(data);os.replace(tmpfile,C/(key+'.jpg'));(C/(key+'.sha256')).write_text(digest)
  try:asyncio.run(run())
  finally:chrome.terminate();chrome.wait()
if __name__=='__main__':
 render([(g,i,v,kind) for g,group in enumerate(outline,1) for i,_ in enumerate(group) for v in (0,1) for kind in ['ref','story']]+[(g,p,0,'doc') for g,p in [(6,0),(6,2),(6,3),(6,4),(6,5),(8,2),(8,3)]])
 print('렌더된 가로 컷',len(list(C.glob('*.jpg'))),flush=True)
