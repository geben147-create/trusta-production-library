"""Render the front-facing annotation layer independently of the 3-D mesh."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,os,sys
P=Path(__file__).resolve().parent;D=P/'glass'
fontfile=Path('/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf')
assert fontfile.is_file()
def ff(n):return ImageFont.truetype(str(fontfile),n)
categories={'closing':('만원','최초 원금|기말 ETF|현금 포함'),'pockets':('만원','기말 ETF|받은 현금|기말 합계'),'boundary':('만원','주가 8,700원|주가 8,800원|주가 8,900원'),'stub':('원','분배락 전|잔여 순자산|받을 돈'),'bothdays':('원','출발|시장 +200원|시장 −200원'),'rights':('만원','연중 1천 주|후반만 보유|하반기 절반'),'reinvest':('원','현금 보관|1주 재매수'),'rise':('원','현금 보관|1주 재매수'),'spent':('만원','소비 전 합계|소비 후 합계|ETF만'),'currency':('만원','연초 원화|기말 원화'),'compare':('만원','월분배+현금|무분배 ETF'),'ending':('만원','ETF 800만|ETF 850만|ETF 1천만')}
if len(sys.argv)>1:
 config=Path(sys.argv[1]);plan=json.loads(config.read_text());D=Path(plan['directory']);P=config.parent
 categories={k:(v['unit'],'|'.join(v['labels'])) for k,v in plan['charts'].items()}
g=json.loads((D/'geometry.json').read_text());report={}
def overlaps(a,b):return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
for key,(unit,s) in categories.items():
 info=g[key];base=Image.open(D/(key+'.png')).convert('RGB')
 W,H=base.size;bottom=round(H*.918)
 canvas=Image.new('RGB',(W,bottom+153),'#f8f4ea');canvas.paste(base.crop((0,0,W,bottom)),(0,0));d=ImageDraw.Draw(canvas)
 labels=[];colors=['#b05226','#2d5e9b','#176858']
 def label(cx,cy,txt,size,maxw,cls,color='#132133',bg=None):
  while size>21 and d.textlength(txt,font=ff(size))>maxw:size-=1
  f=ff(size);box=d.textbbox((cx,cy),txt,font=f,anchor='mm')
  assert box[0]>=0 and box[2]<W and box[1]>=0 and box[3]<canvas.height,(key,txt,box)
  assert all(not overlaps(box,z['box']) for z in labels),(key,txt,box,labels)
  if bg:d.rounded_rectangle((box[0]-5,box[1]-3,box[2]+5,box[3]+3),4,fill=bg)
  d.text((cx,cy),txt,font=f,fill=color,anchor='mm')
  labels.append({'text':txt,'type':cls,'font_px':size,'box':list(box)})
 # Reserve a separate opaque vertical axis lane. Ticks connect the lane to the model.
 ticks=info['ticks'];axisx=int(ticks[0][0]*W-7)
 d.rounded_rectangle((7,10,axisx-5,bottom-5),radius=12,fill='#faf7ed')
 label((axisx-3)//2,33,unit,31,axisx-18,'단위')
 for i in (0,2,4):
  x,y,value=ticks[i];ty=round(y*H);d.line((axisx-5,ty,round(x*W)+4,ty),fill='#38444a',width=3)
  vs=f'{value:,.1f}'.rstrip('0').rstrip('.') if value%1 else f'{value:,.0f}'
  label((axisx-5)//2,ty,vs,29,axisx-18,'눈금')
 # Parallel lanes match each column's center. Type never sits on the glass or the shadow.
 pts=info['points'];centers=[int(px*W) for px,py in pts];lane=min(centers[j+1]-centers[j] for j in range(len(centers)-1))-10
 for j,(value,cx,caption) in enumerate(zip(info['values'],centers,s.split('|'))):
  l,r=cx-lane//2,cx+lane//2
  d.rounded_rectangle((l,bottom+3,r,bottom+147),radius=14,fill='#fffdf6',outline='#b4a690',width=2)
  d.rounded_rectangle((l+13,bottom+10,r-13,bottom+16),radius=3,fill=colors[j])
  label(cx,bottom+48,caption,32,lane-16,'범주','#303737')
  val=f'{value:,.2f}'.rstrip('0').rstrip('.') if value%1 else f'{value:,.0f}'
  label(cx,bottom+105,val,54,lane-14,'값','#152131')
 canvas.save(D/(key+'_표기.png'))
 report[key]={'숫자영역':'불투명 무광 하단 고정 행','폰트':str(fontfile),'canvas':canvas.size,'labels':labels}
(P/'숫자검수.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('실측 경계·겹침 확인',len(report),'장')
