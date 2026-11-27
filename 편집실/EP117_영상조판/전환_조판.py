from decimal import Decimal as D
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

root = Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#faf2e3')
draw=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#263338','#8c2529','#fff0a7'

def text(x,y,s,size,color=ink,anchor='la'):
    draw.text((x,y),s,font=ImageFont.truetype(font,size),fill=color,anchor=anchor)

def panel(coords,color,outline=ink,r=22):
    draw.rounded_rectangle(coords,r,fill=color,outline=outline,width=3)

def bubble(coords,tail,s,size):
    draw.polygon(tail,fill='white',outline=ink,width=3)
    panel(coords,'white')
    a,b,c,d=coords
    text((a+c)//2,(b+d)//2,s,size,ink,'mm')

def character(filename,crop,xy,size):
    art=Image.open(root/'집필인계'/filename).crop(crop)
    art=ImageOps.fit(art,size,centering=(.5,.2))
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),18,fill=255)
    im.paste(art,xy,mask)

text(56,20,'ISA 만기 3,000만 원, 연금으로 옮기면?',66)
text(60,112,'일반 공제 한도를 이미 채웠고 공제할 소득세가 충분한 가상 사례',31)

panel((56,169,1860,433),'#f3e2ca')
character('천억이_시그니처표정.png',(45,0,237,244),(77,213),(158,188))
bubble((221,192,650,259),[(261,247),(221,283),(280,248)],'앗, 300만 원 받는 거야?',31)
character('수건_캐릭터_사용자원본.png',(16,37,182,185),(1645,208),(188,180))
bubble((1245,194,1658,262),[(1601,250),(1660,282),(1632,245)],'그건 공제 대상 한도야.',31)
panel((516,284,1380,408),'#fffaf0','#d0b99f')
text(949,313,'전환금액 3,000만 원  ×  10%',34,ink,'mm')
text(949,373,'추가 공제 대상 한도 300만 원',40,red,'mm')

panel((56,452,1860,891),'#fffdf7')
text(90,474,'줄어드는 소득세',42)
draw.rounded_rectangle((538,479,921,525),13,fill=lemon)
text(557,487,'추가 공제 대상 한도 × 공제율',25)

def mix(a,b,t):
    return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))

x0,xscale=523,21
draw.line((x0,562,x0,807),fill='#58777b',width=4)
for tick in (0,10,20,30,40,50):
    x=x0+tick*xscale
    draw.line((x,800,x,813),fill='#58777b',width=3)
    text(x,828,str(tick),25,ink,'mt')
text(1740,833,'만 원',24,ink,'mm')

for rate,y,light,dark in [
    (D('.12'),610,(140,226,243),(20,75,119)),
    (D('.15'),727,(255,213,127),(145,68,14)),
]:
    amount=D(3000000)*rate/D(10000)
    x1=x0+int(amount*xscale)
    shadow=Image.new('RGBA',im.size)
    ImageDraw.Draw(shadow).rounded_rectangle((x0+8,y+29,x1+20,y+52),10,fill=(22,46,52,82))
    shadow=shadow.filter(ImageFilter.GaussianBlur(10))
    im.paste(shadow,(0,0),shadow)
    draw.polygon([(x0,y-31),(x0+15,y-47),(x1+15,y-47),(x1,y-31)],fill=mix(light,dark,.25),outline=dark)
    draw.polygon([(x1,y-31),(x1+15,y-47),(x1+15,y+11),(x1,y+27)],fill=dark)
    for n in range(59):
        for start,end,depth in [(x0,x1,.0),(x1-5,x1,.18)]:
            draw.line((start,y-31+n,end,y-31+n),fill=mix(light,dark,.6-.48*n/58+depth))
    draw.line((x0+5,y-27,x1-6,y-27),fill=mix(light,(255,255,255),.55),width=3)
    text(94,y,f'소득세 공제율 {rate:.0%}',34,ink,'lm')
    panel((1540,y-40,1807,y+40),'#faf5eb','#d9ccbb',14)
    text(1673,y,f'{amount:.0f}만 원',45,red,'mm')

panel((57,909,1860,973),lemon,lemon,15)
text(81,924,'확인할 것  ·  ISA 만기일부터 60일 이내 납입  ·  처리일과 남은 소득세 확인',32)
text(61,990,'가상 원화 예시 · 국세만 비교 · 지방소득세와 연금 인출 시 과세 제외',23)
text(61,1030,'출처  국가법령정보센터 · 소득세법 / 국세청 · 연금계좌 안내',21)
im.save(root/'영상/EP117/삼백만원의_자리.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep117-preview.png')
