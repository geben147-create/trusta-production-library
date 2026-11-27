from decimal import Decimal
from pathlib import Path
from PIL import Image, ImageDraw, ImageColor, ImageFont, ImageOps

root=Path(__file__).resolve().parents[2]
canvas=Image.new('RGB',(1920,1080),'#faf2e2')
d=ImageDraw.Draw(canvas)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#263437','#89282c','#fff0a6'

def text(x,y,s,size,color=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,size),fill=color,anchor=anchor)

def gradient(x0,y0,x1,y1,top,bottom):
    c0,c1=ImageColor.getrgb(top),ImageColor.getrgb(bottom)
    for y in range(y0,y1+1):
        f=(y-y0)/(y1-y0)
        d.line((x0,y,x1,y),fill=tuple(round(a*(1-f)+b*f) for a,b in zip(c0,c1)))

def box(xy,fill,outline=ink,r=20):
    d.rounded_rectangle(xy,r,fill=fill,outline=outline,width=3)

def character(filename,crop,pos,size):
    art=ImageOps.fit(Image.open(root/'집필인계'/filename).crop(crop),size,centering=(.5,.28))
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),20,fill=255)
    canvas.paste(art,pos,mask)

def bubble(xy,tip,s):
    a,b,c,e=xy
    d.polygon(tip,fill='white',outline=ink,width=3)
    box(xy,'white')
    text((a+c)//2,(b+e)//2,s,27,ink,'mm')

text(55,24,'부모님께 ETF 설명할 때 먼저 볼 TOP 7',66)
box((56,120,688,168),lemon,lemon,13)
text(74,130,'원금 1,000만 원 · 내년 필수 지출 400만 원',28)
text(731,132,'가상 가족의 확인 순서',28)

box((54,187,1206,937),'#fffaf0')
text(83,208,'ETF를 고르기 전에 확인할 순서',34)
cx=630
labels=['돈이 필요한 날','편입 자산과 중복','원화 환산·환노출','분배금과 평가액 합계','보유 비용과 거래 비용','수익률 기간과 기준 맞추기','세금·결제일·실제 출금 가능액']
for i,label in enumerate(labels,1):
    width=475+(i-1)*96
    y=278+(i-1)*86
    lo,hi=cx-width//2,cx+width//2
    dark='#8e682e' if i==1 else '#406679'
    front='#ffeda2' if i==1 else '#c3e1e7'
    lighter='#f9dd8a' if i==1 else '#a5cbd3'
    d.polygon([(lo,y),(lo+19,y-15),(hi+19,y-15),(hi,y)],fill=lighter,outline=dark)
    d.polygon([(hi,y),(hi+19,y-15),(hi+19,y+45),(hi,y+60)],fill=dark)
    gradient(lo,y,hi,y+60,lighter,front)
    d.rectangle((lo,y,hi,y+60),outline=dark,width=2)
    text(cx,y+30,f'{i}위  {label}',32,red if i==1 else ink,'mm')

box((1229,187,1867,937),'#f1dfc5')
character('수건_캐릭터_사용자원본.png',(16,35,181,180),(1258,218),(153,145))
bubble((1376,198,1844,253),[(1412,248),(1394,269),(1440,250)],'내년에 400만 원이 필요해.')
character('천억이_시그니처표정.png',(45,0,237,241),(1688,282),(146,151))
bubble((1248,350,1733,406),[(1687,356),(1721,335),(1735,357)],'그럼 하락 뒤 남는 돈부터!')

text(1265,462,'ETF가 1년간 25% 하락한다면',31,red)
text(1265,507,'400만 원 지출 뒤 · 단위 만 원',24)
base=1275
for name,amount,y,color in [
    ('1,000만 원 전액 투자',Decimal(1000)*Decimal('.75')-400,575,'#578fae'),
    ('400만 원 현금으로 보관',Decimal(600)*Decimal('.75'),712,'#bf8244'),
]:
    text(1265,y,name,26)
    end=base+int(amount*Decimal('.93'))
    d.polygon([(base,y+47),(base+14,y+36),(end+14,y+36),(end,y+47)],fill='#dae2e1',outline=ink)
    d.polygon([(end,y+47),(end+14,y+36),(end+14,y+79),(end,y+90)],fill='#526a6c')
    gradient(base,y+47,end,y+90,color,'#abd9e6' if amount==350 else '#f3cc90')
    d.rectangle((base,y+47,end,y+90),outline=ink,width=2)
    box((1712,y+39,1846,y+94),'#fff8ed','#cfbc9c',11)
    text(1779,y+66,f'{amount:.0f}',32,red,'mm')
d.line((base,618,base,815),fill=ink,width=3)
text(base,829,'0',18,ink,'mt')
text(1265,876,'25% 상승하면 전액 투자 쪽이 100만 원 더 남아요.',20)

text(58,963,'가상 원화 비교 · 현금 이자와 분배금 0 · 세금·비용·환율·재투자 미반영',23)
text(58,1006,'출처  미국 SEC · ETF 투자자 안내 및 비용 안내 / FINRA · 자산 배분과 분산투자',21)
canvas.save(root/'영상/EP121/부모님_ETF_피라미드.png')
canvas.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep121-preview.png')
