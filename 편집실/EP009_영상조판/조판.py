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


label(55,42,'같은 ETF인데, 이겼다가 졌다고?',61)
panel((53,141,1865,754),'#fffaf0')
label(93,180,'원화 100만 원으로 시작한 1년 가상 수익률',37)
base=651
for value in (0,3,6,9):
    y=base-value*40
    d.line((202,y,1770,y),fill='#cdc6bb',width=2)
    label(173,y,f'{value}%',27,anchor='rm')
for x,name,value,top,bottom,side in [
    (351,'가격지수',6,(118,65,25),(218,149,70),'#814612'),
    (821,'같은 ETF',8,(26,67,120),(84,160,217),'#234571'),
    (1291,'총수익지수',9,(118,65,25),(218,149,70),'#814612')]:
    panel((x,670,x+250,728),lemon)
    label(x+125,698,name,27,anchor='mm')
    y=base-value*40
    right=x+250
    d.polygon([(x,y),(right,y),(right+19,y-16),(x+19,y-16)],fill=bottom)
    d.polygon([(right,y),(right+19,y-16),(right+19,base-16),(right,base)],fill=side)
    for row in range(y,base):
        t=(row-y)/(base-y-1)
        for col in range(10):
            color=tuple(round((a+(b-a)*t)*(1-.018*col)) for a,b in zip(top,bottom))
            d.line((x+25*col,row,x+25*(col+1),row),fill=color)
    d.line((x+6,y+7,right-6,y+7),fill=bottom,width=3)
    panel((x+62,y-72,x+194,y-21),'#f6ede0')
    label(x+128,y-47,f'+{value}%',30,anchor='mm')

portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(71,777),(141,145))
panel((239,790,888,897),'#fffdf8')
d.polygon([(239,827),(208,841),(239,855)],fill='#fffdf8')
label(261,818,'“가격지수보다 2%p 앞섰네.”',34)
portrait('천억이_시그니처표정.png',(39,8,251,249),(1659,767),(162,173))
panel((933,795,1638,907),'#fffdf8')
d.polygon([(1638,824),(1666,845),(1638,862)],fill='#fffdf8')
label(959,823,'“배당 포함 지수에는 1%p 뒤졌어!”',34,red)
label(55,959,'ETF 펀드비용 반영·분배금 재투자  ·  개인 거래비용·세금 제외  ·  같은 기간·통화의 가상 비교',23)
label(55,1002,'출처  미국 SEC 펀드 거래방식 비교  ·  S&P 다우존스 지수 산출기관',23)
im.save(root/'시각자료/EP009_두가지_ETF성적표.png')
im.resize((960,540)).save('/tmp/trusta-ep009-preview.png')
