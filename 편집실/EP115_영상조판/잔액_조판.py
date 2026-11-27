import json
from decimal import Decimal
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

root = Path(__file__).resolve().parents[2]
data = json.loads((root/'편집실/EP115_원자료/복리_검산.json').read_text())['반올림전잔액']
im = Image.new('RGB',(1920,1080),'#fcf7ec')
draw = ImageDraw.Draw(im)
font = '/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink, red = '#243138','#8e242b'

def text(x,y,s,size,color=ink,anchor='la'):
    draw.text((x,y),s,font=ImageFont.truetype(font,size),fill=color,anchor=anchor)

def box(coords,color,edge=ink,r=24,w=3):
    draw.rounded_rectangle(coords,r,fill=color,outline=edge,width=w)

def portrait(name,crop,xy,size):
    art = Image.open(root/'집필인계'/name).crop(crop)
    art = ImageOps.fit(art,size,centering=(.5,.25))
    mask = Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),18,fill=255)
    im.paste(art,xy,mask)

def bubble(coords,tail,s,size):
    draw.polygon(tail,fill='white',outline=ink,width=3)
    box(coords,'white')
    x1,y1,x2,y2 = coords
    text((x1+x2)//2,(y1+y2)//2,s,size,ink,'mm')

text(58,22,'주식 ETF와 채권 ETF에 각각 1만 달러를 넣었다면?',58)
box((58,111,544,160),'#fff0a6','#fff0a6',14)
text(80,121,'같은 시작 원금 · 같은 비교 기간',28)
text(583,123,'공시 기준가 총수익률로 만든 달러 장부',26)
box((56,179,1436,901),'#fffdf8')
box((1457,179,1868,901),'#eedfc9')

portrait('수건_캐릭터_사용자원본.png',(16,36,180,178),(1508,225),(220,186))
bubble((1482,386,1844,454),[(1555,391),(1584,365),(1606,393)],'내년에 쓸 돈인데?',31)
portrait('천억이_시그니처표정.png',(43,0,237,240),(1652,504),(178,209))
bubble((1476,694,1848,765),[(1682,702),(1713,675),(1733,702)],'그럼 1년 장부부터!',30)
text(1659,817,'필요한 날에 얼마 있지?',27,red,'mm')

x0, y0 = 176, 768
scale = 0.020
for tick in [0,5000,10000,15000,20000]:
    y = y0-int(tick*scale)
    draw.line((x0,y,1395,y),fill='#7c9392' if tick in (0,10000) else '#d4deda',width=3 if tick in (0,10000) else 1)
    text(x0-17,y,f'${tick:,}',20,ink,'rm')

def mix(a,b,t):
    return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))

palettes = {'IVV':((132,235,245),(18,76,119)), 'AGG':((255,213,129),(139,66,12))}
def column(x, amount, ticker):
    top = y0-round(Decimal(str(scale))*amount)
    light,dark = palettes[ticker]
    shade=Image.new('RGBA',im.size)
    ImageDraw.Draw(shade).rounded_rectangle((x-48,y0-1,x+77,y0+21),9,fill=(29,53,58,80))
    shade=shade.filter(ImageFilter.GaussianBlur(9))
    im.paste(shade,(0,0),shade)
    draw.polygon([(x-47,top),(x-29,top-17),(x+66,top-17),(x+48,top)],fill=mix(light,dark,.34),outline=dark)
    draw.polygon([(x+48,top),(x+66,top-17),(x+66,y0-17),(x+48,y0)],fill=dark)
    for dy in range(y0-top):
        t=dy/(y0-top)
        draw.line((x-47,top+dy,x+48,top+dy),fill=mix(light,dark,.49-.43*t+.18*t**4))
    draw.line((x-43,top+4,x+43,top+4),fill=mix(light,(255,255,255),.7),width=3)
    label_y=top-35
    box((x-116,label_y-24,x+116,label_y+25),'#fffdf8','#d9dbd1',11,2)
    text(x,label_y,f'${amount:,.2f}',29,ink,'mm')
    text(x,y0+39,ticker,27,ink,'mm')

for period,ab in [('2020년 말~2025년 말',(390,661)),('2021년 말~2022년 말',(1020,1285))]:
    for ticker,x in zip(('IVV','AGG'),ab):
        column(x,Decimal(data[period][ticker]),ticker)
text(523,840,'2020년 말 → 2025년 말',29,ink,'mm')
text(1154,840,'2021년 말 → 2022년 말',29,ink,'mm')
draw.line((821,300,821,877),fill='#c8b9a7',width=2)
text(205,210,'5년을 기다렸다면',41)
text(852,210,'이듬해에 써야 했다면',38)
text(205,269,'IVV가 $9,782.85 앞섰어요.',28,red)
text(852,269,'AGG가 $507 앞섰어요.',28,red)

box((55,917,1868,979),'#fff0a6','#fff0a6',15)
text(80,932,'2022년 말에 9,000달러가 필요했다면 두 상품 모두 부족했어요.',32)
text(60,995,'미국달러 · 분배금 재투자 · 개인 세금·거래비·환전 제외',24)
text(60,1033,'출처  iShares · IVV 팩트시트 · AGG 팩트시트',22)
im.save(root/'영상/EP115/같은원금_다른달력.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep115-preview.png')
