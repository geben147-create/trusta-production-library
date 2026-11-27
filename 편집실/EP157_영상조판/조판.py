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

# Two calendars lead into the same withdrawal experiment.
txt(60,49,'퇴직금 1억, 생활비를 빼면 얼마나 남을까?',65)
rounded((62,135,1560,194),'#fff0aa')
txt(84,150,'같은 출발금 1억 원  ·  같은 연말 인출 1,200만 원  ·  2년 가상 실험',34)
rounded((62,217,1190,474),'#f1e4d4','#b59b7c')
portrait('천억이_시그니처표정.png',(37,8,251,249),(87,238),(201,216))
rounded((314,248,1149,427),'#fffdf8',ink)
d.polygon([(314,306),(290,330),(314,348)],fill='#fffdf8',outline=ink,width=2)
txt(350,278,'같은 1억으로 시작했는데…',44)
txt(350,351,'왜 통장에 540만 원이나 차이 나지?',39,red)
rounded((1212,217,1857,474),'#edddc4','#b59b7c')
portrait('수건_캐릭터_사용자원본.png',(9,34,180,180),(1641,243),(189,180))
rounded((1234,250,1626,419),'#fffdf8',ink)
d.polygon([(1626,304),(1647,327),(1626,338)],fill='#fffdf8',outline=ink,width=2)
txt(1261,281,'첫해에 생활비를 빼면',32)
txt(1261,345,'반등할 돈이 달라져.',33,red)
rounded((62,501,1857,979),'#fffdf8','#b59b7c')
txt(95,526,'두 번 인출한 뒤 2년 말 잔액',44)
x0,y0,plot_width=500,623,948
for tick in (0,2000,4000,6000,8000):
    x=x0+round(tick*plot_width/8000)
    d.line((x,y0,x,888),fill='#a6afb1',width=3 if tick==0 else 1)
    txt(x,913,f'{tick:,}',25,anchor='mt')
rows=[('−20% 다음 +25%',7300,657,((27,75,139),(121,216,244))),
      ('+25% 다음 −20%',7840,785,((143,69,16),(250,181,71)))]
for label,value,y,colors in rows:
    txt(104,y+12,label,36)
    glass(x0,y,round(value*plot_width/8000),55,colors)
    rounded((1515,y-6,1825,y+63),'#f5f3ec')
    txt(1670,y+10,f'{value:,}만 원',42,anchor='mt')
txt(1803,914,'단위  만 원',28,anchor='rt')
txt(80,1012,'분배금 재투자 가정 · 세금·비용·물가 제외 · 월 100만 원 부족분을 연말에 한 번씩 인출',28)
path=root/'시각자료/EP157_퇴직금_두달력.png'
im.save(path)
