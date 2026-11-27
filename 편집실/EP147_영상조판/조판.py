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

txt(65,50,'같은 1만 달러인데, 시작 연도를 바꾸니 순위가 뒤집혔다',56)
rounded((65,133,1150,183),'#fff0aa')
txt(84,146,'미국 외 선진국 IEFA  vs  신흥국 IEMG  ·  같은 종료일 2025년 말',27)
portrait('천억이_시그니처표정.png',(40,4,249,253),(1458,115),(110,130))
portrait('수건_캐릭터_사용자원본.png',(9,34,180,180),(1685,106),(150,123))
rounded((1265,160,1467,227),'#fffdf7',ink)
d.polygon([(1465,182),(1485,189),(1465,205)],fill='#fffdf7',outline=ink,width=2)
txt(1366,193,'5년만 보면?',26,ink,'mm')
rounded((1562,200,1855,263),'#fffdf7',ink)
d.polygon([(1720,200),(1730,180),(1740,200)],fill='#fffdf7',outline=ink,width=2)
txt(1708,231,'마지막 두 해도 봐!',26,ink,'mm')
rounded((65,279,1855,905),'#fffdfa','#c8bca9')
txt(89,303,'달러 NAV 총수익으로 계산한 가상 잔액',32)
x0=432
s=1000/16000
for v in (0,4000,8000,12000,16000):
    x=x0+round(v*s)
    d.line((x,358,x,806),fill='#b5c4c6',width=3 if v==0 else 1)
    txt(x,824,f'{v:,}',23,ink,'mt')
txt(1497,831,'달러',22)
blue=((19,78,118),(114,210,237))
amber=((133,63,21),(255,184,89))
panels=[('2021년 시작',((15146.25,'IEFA',blue),(12518.96,'IEMG',amber)),(407,499)),
        ('2024년 시작',((13632.54,'IEFA',blue),(14126.27,'IEMG',amber)),(642,734))]
for period, rows, ys in panels:
    rounded((89,ys[0]-15,266,ys[1]+47),'#fff2bd')
    txt(178,(ys[0]+ys[1]+32)//2,period,25,ink,'mm')
    highest=max(row[0] for row in rows)
    for (amount,label,palette),y in zip(rows,ys,strict=True):
        txt(320,y+19,label,28,ink,'mm')
        glass(x0,y,round(amount*s),46,palette)
        rounded((1484,y-9,1825,y+53),'#fcece8' if amount==highest else '#f1f1e9')
        txt(1654,y+20,f'{amount:,.2f}달러',33,red if amount==highest else ink,'mm')
d.line((91,582,1825,582),fill='#c3bbb0',width=2)
rounded((65,925,1855,989),'#fff0aa')
txt(91,944,'먼저 정할 것은 순위가 아니라 내 돈을 쓸 날짜',35,red)
txt(65,1019,'배당 재투자 반영 · 개인 세금·환전·거래비용 제외    |    출처  iShares · IEFA 및 IEMG 팩트시트',24)
out=root/'영상/EP147/시작일_역전.png'
im.save(out)
im.resize((960,540),Image.Resampling.LANCZOS).save(Path(__file__).with_name('축소검수.png'))
