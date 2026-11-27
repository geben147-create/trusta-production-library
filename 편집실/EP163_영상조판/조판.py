from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

root=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#f8f2e7')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink='#172b36'
red='#91212d'

def txt(x,y,s,n,fill=ink,anchor='lt'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=fill,anchor=anchor)

def rounded(bounds,fill,outline=None):
    d.rounded_rectangle(bounds, radius=20,fill=fill,outline=outline,width=3)

def portrait(file,crop,at,size):
    art=ImageOps.fit(Image.open(root/'집필인계'/file).crop(crop),size)
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),radius=20,fill=255)
    im.paste(art,at,mask)

def mix(a,b,t):
    return tuple(round(x+(y-x)*t) for x,y in zip(a,b))

def glass(x,y,w,h,palette):
    depth=22
    shadow=Image.new('RGBA',im.size)
    sh=ImageDraw.Draw(shadow)
    sh.rounded_rectangle((x+11,y+18,x+w+45,y+h+19),radius=16,fill=(28,43,52,84))
    shadow=shadow.filter(ImageFilter.GaussianBlur(11))
    im.paste(shadow,(0,0),shadow)
    d.polygon([(x,y),(x+depth,y-depth),(x+w+depth,y-depth),(x+w,y)],fill=palette[1],outline=palette[0],width=2)
    d.polygon([(x+w,y),(x+w+depth,y-depth),(x+w+depth,y+h-depth),(x+w,y+h)],fill=palette[0])
    colors=Image.new('RGB',(w,h))
    px=colors.load()
    for yi in range(h):
        for xi in range(w):
            v=yi/(h-1)
            u=xi/(w-1)
            shade=.65+.26*v-.22*u
            if .17<v<.24:
                shade+=.12
            px[xi,yi]=mix(palette[0],palette[1],min(1,shade))
    im.paste(colors,(x,y))
    d.line((x+2,y+2,x+w-2,y+2),fill='#fff7ec',width=3)
    d.line((x+w-1,y+1,x+w-1,y+h),fill=palette[0],width=3)

txt(60,49,'은퇴 생활비 1,000만 원, 어디서 빼면 달라질까?',58)
rounded((62,139,1857,190),'#fff0aa')
txt(80,150,'가상 비교  ·  인출 전 주식 7,000만 원 / 채권 3,000만 원  ·  인출 뒤 총액 9,000만 원',29)
rounded((60,214,476,960),'#ebdecb','#b19983')
portrait('천억이_시그니처표정.png',(39,8,251,249),(171,237),(177,194))
rounded((85,447,450,560),'#fffdf8')
d.polygon([(249,447),(259,426),(276,447)],fill='#fffdf8')
txt(267,462,'똑같이 천만 원인데?',29,anchor='mt')
txt(267,514,'남은 비중을 봐!',31,red,'mt')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(156,591),(214,203))
txt(268,839,'남겨 둘 주식 비중',27,anchor='mt')
txt(268,884,'가상 목표 65%',35,red,'mt')

rounded((500,214,1858,960),'#fffdfa','#b19983')
txt(541,244,'인출 뒤 주식 비중',42)
x0, span=817,781
for mark in (0,20,40,60,80,100):
    x=x0+round(mark*span/100)
    d.line((x,379,x,876),fill='#b2c0c4',width=3 if mark==0 else 1)
    txt(x,902,f'{mark}%',25,anchor='mt')
rows=[('주식에서 전액',6000/9000,418,((28,72,140),(122,203,244))),
      ('기존 비중대로',6300/9000,589,((28,104,104),(117,212,181))),
      ('채권에서 전액',7000/9000,760,((140,73,22),(249,175,86)))]
for label,value,y,colors in rows:
    txt(542,y+10,label,29)
    glass(x0,y,round(value*span),50,colors)
    rounded((1620,y-9,1824,y+63),'#f2eee4')
    txt(1722,y+12,f'{value:.2%}',37,anchor='mt')
x=x0+round(.65*span)
d.line((x,380,x,865),fill=red,width=4)
txt(x,335,'목표 65%',27,red,'mt')
txt(75,999,'같은 날 인출 · 세금·비용·가격 변화 제외 · 다음 달 수익률은 별도',27)
im.save(root/'시각자료/EP163_생활비_인출후비중.png')
