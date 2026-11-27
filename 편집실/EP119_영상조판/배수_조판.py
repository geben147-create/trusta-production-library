from decimal import Decimal
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

root=Path(__file__).resolve().parents[2]
obs=json.loads((root/'편집실/EP119_원자료/배수_검산.json').read_text())['NASDAQCOM']['관측']
im=Image.new('RGB',(1920,1080),'#fbf2e2')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink, red, lemon='#24353a','#8e242b','#fff1a6'

def txt(x,y,s,n,fill=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=fill,anchor=anchor)

def panel(xy,fill,edge=ink,r=21):
    d.rounded_rectangle(xy,r,fill=fill,outline=edge,width=3)

def person(name,crop,pos,size):
    face=ImageOps.fit(Image.open(root/'집필인계'/name).crop(crop),size,centering=(.5,.25))
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),20,fill=255)
    im.paste(face,pos,mask)

def talk(xy,tail,s):
    d.polygon(tail,fill='white',outline=ink,width=3)
    panel(xy,'white')
    a,b,c,e=xy
    txt((a+c)//2,(b+e)//2,s,32,ink,'mm')

txt(53,23,'나스닥 종합, 두 배까지 318일 vs 1,750일',63)
panel((56,116,555,167),lemon,lemon,15)
txt(75,126,'같은 지수 · 33일 다른 시작일',29)
txt(588,129,'일별 종가가 시작값의 2배 이상인 첫날',26)

panel((55,188,1864,409),'#efddc2')
person('수건_캐릭터_사용자원본.png',(16,36,182,186),(80,214),(196,170))
talk((269,201,951,269),[(293,261),(258,283),(310,263)],'두 배까지 318일? 난 한 달 먼저 들어갔는데.')
person('천억이_시그니처표정.png',(44,0,236,244),(1677,221),(159,169))
talk((1079,307,1694,376),[(1630,313),(1687,281),(1657,316)],'앗, 첫날이 다르면 목표 종가도 다르네!')
txt(309,334,'시작 종가를 기준으로 계산',28,red)

panel((56,430,1864,871),'#fffdf6')
txt(85,452,'처음 두 배를 찍기까지 걸린 시간',36)
txt(1324,456,'첫 2배까지 / 마지막 배수',26)
zero=515
scale=.452
d.line((zero,531,zero,790),fill='#64777b',width=3)

def mix(a,b,t):
    return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))

for start,center,colors in [
    ('2020-03-23',592,((141,220,242),(18,84,123))),
    ('2020-02-19',716,((255,219,142),(139,69,17))),
]:
    r=obs[start]
    days=r['기준통과'][0]['경과일']
    x=zero+round(days*scale)
    light,dark=colors
    y=center-26
    shadow=Image.new('RGBA',im.size)
    ImageDraw.Draw(shadow).rounded_rectangle((zero+8,y+45,x+19,y+71),11,fill=(30,54,62,92))
    shadow=shadow.filter(ImageFilter.GaussianBlur(9))
    im.paste(shadow,(0,0),shadow)
    d.polygon([(zero,y),(zero+16,y-16),(x+16,y-16),(x,y)],fill=mix(light,dark,.26),outline=dark)
    d.polygon([(x,y),(x+16,y-16),(x+16,y+36),(x,y+52)],fill=dark)
    for dy in range(53):
        d.line((zero,y+dy,x,y+dy),fill=mix(light,dark,.65-.47*dy/52))
    d.line((zero+4,y+3,x-3,y+3),fill=mix(light,(255,255,255),.45),width=3)
    month='3월 23일' if start.endswith('03-23') else '2월 19일'
    txt(85,center,f'2020년 {month} 출발',28,ink,'lm')
    panel((1352,center-42,1826,center+42),'#fbf6ec','#ddd1bd',13)
    txt(1459,center,f'{days:,}일',38,red,'mm')
    txt(1700,center,f'{Decimal(r["종료배수"]):.2f}배',33,ink,'mm')
for tick in (0,500,1000,1500):
    px=zero+round(tick*scale)
    d.line((px,781,px,795),fill='#64777b',width=3)
    txt(px,807,f'{tick:,}',21,ink,'mt')
txt(1297,817,'달력일',20,ink,'mm')

panel((54,889,1865,973),lemon,lemon,16)
txt(82,907,'2월 출발은 12월 초 두 배를 넘겼지만, 2024년 말에는 약 1.97배였어요.',32)
txt(60,992,'미국 거래일 종가 · 배당·세금·비용·환율 제외 · 종료일 2024년 12월 31일',23)
txt(60,1031,'출처  세인트루이스 연방준비은행 FRED · NASDAQ Composite',22)
im.save(root/'영상/EP119/첫두배_두달력.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep119-preview.png')
