from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

root=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#f2eadd')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#172b36','#92252e','#fff0aa'

def label(x,y,s,size,color=ink,anchor='lt'):
    d.text((x,y),s,font=ImageFont.truetype(font,size),fill=color,anchor=anchor)

def panel(box,fill):
    d.rounded_rectangle(box,22,fill=fill,outline='#b7a593',width=2)

def portrait(name,crop,xy,size):
    img=ImageOps.fit(Image.open(root/'집필인계'/name).crop(crop),size)
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),16,fill=255)
    im.paste(img,xy,mask)


label(57,46,'반씩 담았는데, 왜 80%가 미국일까?',62)
panel((56,145,1863,385),'#e9dcc9')
portrait('천억이_시그니처표정.png',(39,8,251,249),(87,178),(170,184))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1668,183),(150,161))
panel((281,190,940,282),'#fffdf8')
label(307,219,'“미국과 세계, 딱 반씩 담았는데?”',34)
d.polygon([(281,231),(251,248),(281,253)],fill='#fffdf8')
panel((1000,258,1643,350),'#fffdf8')
label(1023,286,'“세계 바구니에도 미국이 들어 있어.”',32,red)
d.polygon([(1643,291),(1674,269),(1643,310)],fill='#fffdf8')
panel((57,411,1862,936),'#fffaf0')
label(94,443,'ETF마다 50만 원씩 넣은 가상 계좌',39)
x0=448
width=1200
for v in (0,20,40,60,80,100):
    x=x0+round(width*v/100)
    d.line((x,531,x,750),fill='#cec7bb',width=2)
    label(x,768,str(v),23,anchor='mt')
label(1700,768,'만 원',23)
for y,title,segments in (
    (553,'상품별 배분',((50,'미국 대형주 50만',(34,76,121),(82,148,199)),(50,'세계주식 50만',(130,74,34),(212,153,86)))),
    (672,'국가별 배분',((80,'미국 80만',(34,76,121),(82,148,199)),(20,'비미국 20만',(130,74,34),(212,153,86))))):
    label(93,y+29,title,34)
    left=x0
    for value,name,top,low in segments:
        right=left+round(width*value/100)
        d.polygon([(left,y),(right,y),(right+14,y-13),(left+14,y-13)],fill=low)
        if right==x0+width:
            d.polygon([(right,y),(right+14,y-13),(right+14,y+54),(right,y+67)],fill=top)
        for row in range(y,y+67):
            progress=(row-y)/66
            fill=tuple(round(a+(b-a)*progress) for a,b in zip(top,low))
            d.line((left,row,right-1,row),fill=fill)
        mid=(left+right)//2
        label(mid,y+35,name,26 if value==20 else 31,'#fffdf8','mm')
        left=right
panel((95,829,1805,900),lemon)
label(123,852,'세계주식의 가상 미국 비중 60%',28)
label(930,849,'미국 50만 원 + 30만 원 = 80만 원',35,red)
label(57,957,'한 시점의 원화 구성 비교  ·  환헤지와 파생 노출 없음  ·  비용·세금·분배금 계산 제외',24)
label(57,1002,'출처  Vanguard 전세계 주식 ETF 팩트시트  ·  S&P 다우존스 지수 산출기관',23)
im.save(root/'시각자료/EP013_두바구니_미국비중.png')
im.resize((960,540)).save('/tmp/trusta-ep013-preview.png')
