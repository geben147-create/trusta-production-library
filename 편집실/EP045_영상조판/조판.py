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


label(55,42,'월분배 ETF 네 개, 같은 1년의 성적표',61)
panel((53,141,1865,754),'#fffaf0')
label(93,180,'2025년 9월 30일~2026년 9월 30일 · 달러 NAV 총수익률',37)
base=651
for value in (0,5,10,15,20):
    y=base-round(value*17.5)
    d.line((202,y,1770,y),fill='#cdc6bb',width=2)
    label(173,y,f'{value}%',27,anchor='rm')
for x,name,value,top,bottom,side in [
    (267,'JEPI',6.62,(26,67,120),(84,160,217),'#234571'),
    (645,'SPYI',14.62,(118,65,25),(218,149,70),'#814612'),
    (1024,'QQQI',17.97,(118,65,25),(218,149,70),'#814612'),
    (1403,'JEPQ',19.45,(26,67,120),(84,160,217),'#234571')]:
    panel((x,670,x+250,728),lemon)
    label(x+125,698,name,27,anchor='mm')
    y=base-round(value*17.5)
    right=x+250
    d.polygon([(x,y),(right,y),(right+19,y-16),(x+19,y-16)],fill=bottom)
    d.polygon([(right,y),(right+19,y-16),(right+19,base-16),(right,base)],fill=side)
    for row in range(y,base):
        t=(row-y)/(base-y-1)
        for col in range(10):
            color=tuple(round((a+(b-a)*t)*(1-.018*col)) for a,b in zip(top,bottom))
            d.line((x+25*col,row,x+25*(col+1),row),fill=color)
    d.line((x+6,y+7,right-6,y+7),fill=bottom,width=3)
    panel((x+40,y-72,x+214,y-21),'#f6ede0')
    label(x+128,y-47,f'+{value:.2f}%',30,anchor='mm')

portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(71,777),(141,145))
panel((239,790,888,897),'#fffdf8')
d.polygon([(239,827),(208,841),(239,855)],fill='#fffdf8')
label(261,818,'“1년 성적을 같은 기간으로 맞췄어.”',34)
portrait('천억이_시그니처표정.png',(39,8,251,249),(1659,767),(162,173))
panel((933,795,1638,907),'#fffdf8')
d.polygon([(1638,824),(1666,845),(1638,862)],fill='#fffdf8')
label(959,823,'“다음 달 입금은 분배 이력을 봐.”',34,red)
label(55,959,'분배금 재투자와 펀드 비용 반영  ·  개인 거래비용·세금·환전 제외  ·  과거 1년 공시값',23)
label(55,1002,'출처  J.P. Morgan JEPI·JEPQ 팩트시트  ·  NEOS SPYI·QQQI 상품 안내',23)
im.save(root/'시각자료/EP045_월분배ETF_1년성적표.png')
im.resize((960,540)).save('/tmp/trusta-ep045-preview.png')
