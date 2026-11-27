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
