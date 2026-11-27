from decimal import Decimal as D
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

root = Path(__file__).resolve().parents[2]
canvas = Image.new('RGB', (1920,1080), '#fbf4e7')
draw = ImageDraw.Draw(canvas)
ink, red, lemon = '#223036', '#8c2029', '#fff0a2'
font = '/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'

def text(x,y,s,size,color=ink,anchor='la'):
    draw.text((x,y),s,font=ImageFont.truetype(font,size),fill=color,anchor=anchor)

def box(coords,fill,edge=ink):
    draw.rounded_rectangle(coords,20,fill=fill,outline=edge,width=3)

def portrait(name,crop,size,at):
    art = Image.open(root/'집필인계'/name).crop(crop)
    art = ImageOps.fit(art,size,centering=(.5,.3))
    mask = Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),18,fill=255)
    canvas.paste(art,at,mask)

def bubble(coords,tail,s,size):
    draw.polygon(tail,fill='white',outline=ink,width=3)
    box(coords,'white')
    x,y,w,h = coords
    text((x+w)//2,(y+h)//2,s,size,ink,'mm')

text(55,26,'똑같이 2천만 원을 썼는데 450만 원 차이?',68)
draw.rounded_rectangle((57,124,932,168),12,fill=lemon)
text(78,132,'가상 1억 원 · 매년 말 생활비 1,000만 원 · 두 해 누적 수익률 0%',26)
box((55,192,1866,407),'#f0e2cc')
portrait('수건_캐릭터_사용자원본.png',(16,34,181,179),(189,173),(77,213))
portrait('천억이_시그니처표정.png',(45,0,234,228),(151,173),(1686,213))
bubble((282,216,841,285),[(310,277),(265,298),(330,278)],'이체한 돈도, 본 수익률도 같잖아.',31)
bubble((1044,281,1679,353),[(1625,289),(1690,269),(1650,288)],'맞아. 생활비가 빠진 순서부터 보자!',32)
text(445,345,'두 수익률 카드',24)
box((685,320,824,378),'#ffe9d7','#d59058')
text(754,348,'−20%',31,red,'mm')
box((845,320,984,378),'#e0f4fa','#6bb3c4')
text(915,348,'+25%',31,'#126580','mm')

box((55,427,1866,873),'#fffdf7')
text(83,445,'생활비를 뺀 직후 잔액',36)
text(513,454,'단위  만 원',24)
text(1600,455,'2년 뒤 차이',26)
text(1600,505,'450만 원',45,red)
xs = [328,840,1407]
zero_y = 786
ratio = 2.07
for tick in (0,50,100,125):
    y = zero_y - tick*ratio
    draw.line((233,y,1509,y),fill='#bed0cc',width=3 if tick == 0 else 1)
    text(212,y,f'{tick*100:,}',21,ink,'rm')
for x,tag in zip(xs,('출발','첫해 말','둘째 해 말')):
    text(x,816,tag,26,ink,'mt')

def path(factors, palette):
    value = D(100)
    amounts = [value]
    for factor in factors:
        value = value*D(factor)-10
        amounts.append(value)
    pts = [(x,round(zero_y-float(val)*ratio)) for x,val in zip(xs,amounts)]
    shadow=Image.new('RGBA',canvas.size)
    sh=ImageDraw.Draw(shadow)
    sh.line([(x+8,y+12) for x,y in pts],fill=(13,41,54,75),width=20,joint='curve')
    shadow=shadow.filter(ImageFilter.GaussianBlur(8))
    canvas.paste(shadow,(0,0),shadow)
    for offset, color, width in [(3,palette[0],12),(0,palette[1],9),(-2,palette[2],3)]:
        draw.line([(x,y+offset) for x,y in pts],fill=color,width=width,joint='curve')
    for x,y in pts[1:]:
        draw.ellipse((x-7,y-7,x+7,y+7),fill=palette[2],outline=palette[0],width=3)
    return amounts,pts

down, dp = path(('0.8','1.25'),('#863907','#ca692c','#ffd18b'))
up, upoints = path(('1.25','0.8'),('#1b537c','#3386af','#a5e6f1'))
assert down == [100,70,77.5] and up == [100,115,82]
for x,y,s,c in [(328,544,'10,000',ink),(840,510,'11,500',ink),(840,688,'7,000',ink),(1407,576,'8,200',ink),(1407,663,'7,750',red)]:
    box((x-72,y-21,x+72,y+22),'#fffdf7','#ded8ca')
    text(x,y,s,28,c,'mm')
text(1568,611,'상승 먼저',24,'#1b537c')
text(1568,665,'하락 먼저',24,'#863907')

box((56,892,1865,977),lemon)
text(83,918,'첫해 생활비만 현금 1,000만 원으로 내면?',34)
text(1063,918,'이 예에서는 둘 다 8,000만 원',34,red)
text(62,990,'원화 · 연말 인출 · 분배금 재투자 · 세금·비용·물가·환율 제외',23)
text(62,1030,'출처  Morningstar · The State of Retirement Income  /  Vanguard · Retirement risks and how to manage them',20)
canvas.save(root/'영상/EP113/생활비_순서차트.png')
canvas.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep113-preview.png')
