from decimal import Decimal
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor

root=Path(__file__).resolve().parents[2]
data=json.loads((root/'편집실/FAQ01_원자료/중복_검산.json').read_text())
im=Image.new('RGB',(1920,1080),'#fbf3e4')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#253639','#8b252d','#fff0a6'

def text(x,y,s,n,color=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=color,anchor=anchor)

def panel(xy,color,edge=ink,r=20):
    d.rounded_rectangle(xy,r,fill=color,outline=edge,width=3)

def portrait(label,crop,at,shape):
    art=ImageOps.fit(Image.open(root/'집필인계'/label).crop(crop),shape,centering=(.5,.25))
    mask=Image.new('L',shape)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,shape[0]-1,shape[1]-1),16,fill=255)
    im.paste(art,at,mask)

def speech(xy,tail,s):
    d.polygon(tail,fill='white',outline=ink,width=3)
    panel(xy,'white')
    x,y,w,h=xy
    text((x+w)//2,(y+h)//2,s,29,ink,'mm')

text(54,24,'SOXX와 SMH, 겹침이 같아도 내 계좌는 다르다',62)
panel((56,120,683,167),lemon,lemon,13)
text(74,130,'같은 두 ETF · 가상 계좌 각각 100만 원',27)
text(722,130,'2025년 12월 31일 두 공시의 주식 비중',27)

panel((55,190,1864,382),'#f1dec5')
portrait('천억이_시그니처표정.png',(45,0,237,243),(80,210),(137,150))
speech((204,203,762,265),[(243,253),(210,279),(270,255)],'가중 겹침이 68.81%라고?')
portrait('수건_캐릭터_사용자원본.png',(17,36,183,185),(1657,210),(172,152))
speech((864,299,1690,361),[(1622,305),(1681,274),(1657,304)],'응. 네 돈이 어느 쪽에 더 들어 있는지도 보자!')
text(264,311,'34종목 중 공통 21개',30,red)

panel((54,404,1864,902),'#fffdf7')
text(89,428,'같은 ETF를 다르게 담은 두 계좌의 엔비디아 노출',35)
base=533
scale=Decimal('.0042')
d.line((base,527,base,814),fill='#627c80',width=3)
for tick in (0,50000,100000,150000,200000):
    x=base+int(tick*scale)
    d.line((x,807,x,820),fill='#627c80',width=3)
    text(x,831,f'{tick//10000:,}',24,ink,'mt')
text(1450,842,'만 원',22)

a,b=[Decimal(data['엔비디아_pct'][n]) for n in ('SOXX','SMH')]
for y,aw,bw,top,bottom,side in [
    (581,90,10,'#468ba9','#aae1e9','#395b71'),
    (722,10,90,'#b67836','#f8d28d','#795128'),
]:
    val=(a*aw+b*bw)*100
    end=base+round(val*scale)
    d.polygon([(base,y-29),(base+15,y-45),(end+15,y-45),(end,y-29)],fill=bottom,outline=side)
    d.polygon([(end,y-29),(end+15,y-45),(end+15,y+13),(end,y+29)],fill=side)
    c0,c1=ImageColor.getrgb(top),ImageColor.getrgb(bottom)
    for t in range(59):
        f=t/58
        d.line((base,y+t-29,end,y+t-29),fill=tuple(round(u*(1-f)+v*f) for u,v in zip(c0,c1)))
    d.line((base+4,y-27,end-5,y-27),fill='#f1faf4',width=3)
    text(89,y-22,f'SOXX {aw}% · SMH {bw}%',31)
    panel((1441,y-40,1815,y+41),'#fbf6ec','#d7ccba',12)
    text(1628,y,f'{val:,.0f}원',37,red,'mm')
panel((57,923,1864,977),lemon,lemon,13)
text(79,933,'펀드의 가중 겹침 68.81%는 그대로. 계좌 안 한 기업에 노출된 금액은 달라져요.',27)
text(56,991,'공시 순자산과 개별 주식 식별번호 기준 · 현금성 상품·파생상품 제외 · 원화 평가액 가정',23)
text(56,1031,'출처  미국 SEC · iShares Semiconductor ETF 및 VanEck Semiconductor ETF N-PORT',20)
im.save(root/'영상/FAQ01/실제공시_겹침과노출.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-faq01-preview.png')
