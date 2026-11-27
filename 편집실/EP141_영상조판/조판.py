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

txt(60,45,'집은 3억, 생활비는 매달 100만 원 부족?',67)
rounded((60,138,1150,189),'#fff0aa')
txt(82,151,'일반주택 · 종신 정액형 · 부부 중 나이가 어린 사람 기준',29)
rounded((58,216,540,908),'#f3e4cc','#ba9d7b')
portrait('천억이_시그니처표정.png',(40,3,252,252),(87,241),(192,226))
rounded((260,282,523,393),'#fffdf7',ink)
d.polygon([(260,335),(234,352),(260,365)],fill='#fffdf7',outline=ink,width=2)
txt(388,306,'집주인이',30,ink,'mt')
txt(388,346,'70세인데?',30,ink,'mt')
d.line((85,495,516,495),fill='#b39773',width=3)
portrait('수건_캐릭터_사용자원본.png',(9,34,180,180),(277,570),(229,174))
rounded((76,579,294,716),'#fffdf7',ink)
d.polygon([(294,625),(315,647),(294,651)],fill='#fffdf7',outline=ink,width=2)
txt(184,601,'둘 중',28,ink,'mt')
txt(184,638,'어린 나이를',28,red,'mt')
txt(184,675,'보면 돼.',28,ink,'mt')
txt(91,810,'배우자가 65세면',31)
txt(91,852,'65세 칸을 봐요.',36,red)
rounded((563,216,1860,908),'#fffdfa','#ba9d7b')
txt(602,251,'월 100만 원 중 주택연금으로 채우는 금액',40)
txt(1655,344,'남은 부족액',28,red)
x0=766
scale=780
for v in (0,25,50,75,100):
    x=x0+round(v*scale/100)
    d.line((x,402,x,786),fill='#9caeb0',width=3 if v==0 else 1)
    txt(x,807,str(v),24,ink,'mt')
txt(1545,851,'단위  만 원',21,ink,'rt')
rows=[('65세',758000,468,((133,63,21),(255,184,89))),('70세',923000,657,((19,78,118),(114,210,237)))]
for age,value,y,palette in rows:
    txt(640,y+3,age,36)
    w=round(scale*value/1_000_000)
    glass(x0,y,w,68,palette)
    amt=f'{value//10000}만 {value%10000//1000}천 원'
    txt(x0+w,y-70,amt,34,ink,'rt')
    deficit=1_000_000-value
    rounded((1619,y-8,1834,y+76),'#fcebe7')
    txt(1727,y+20,f'{deficit//10000}만 {deficit%10000//1000}천 원',31,red,'mt')
rounded((58,928,1860,995),'#fff0aa')
txt(82,947,'가입 가능 여부는 공시가격 등으로, 월지급금은 시세·감정평가액으로 확인',34)
txt(60,1014,'기준  2026년 3월 1일 · 월 부족액은 가정    |    출처  한국주택금융공사 · 월지급금 예시',25)
out=root/'영상/EP141/주택연금_두나이.png'
im.save(out)
im.resize((960,540),Image.Resampling.LANCZOS).save(Path(__file__).with_name('축소검수.png'))
