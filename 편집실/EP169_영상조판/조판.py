from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

root=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#f6eedf')
d=ImageDraw.Draw(im)
ink,red,lemon='#172b36','#90222d','#fff0a5'
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'

def label(x,y,s,size=32,color=ink,anchor='lt'):
    d.text((x,y),s,font=ImageFont.truetype(font,size),fill=color,anchor=anchor)

def panel(box,fill):
    d.rounded_rectangle(box,20,fill=fill,outline='#b4a48e',width=2)

def face(name,crop,xy,size):
    art=ImageOps.fit(Image.open(root/'집필인계'/name).crop(crop),size)
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),18,fill=255)
    im.paste(art,xy,mask)

label(56,35,'물가 2.1%라는데, 왜 은퇴 생활비는 더 오를까?',61)
panel((58,134,1861,365),'#f0e0cc')
face('천억이_시그니처표정.png',(39,8,251,249),(80,151),(162,191))
face('수건_캐릭터_사용자원본.png',(23,30,184,187),(1657,150),(173,193))
panel((244,162,1000,246),'#fffdf8')
panel((889,255,1655,339),'#fffdf8')
d.polygon([(246,201),(219,223),(246,222)],fill='#fffdf8')
d.polygon([(1653,287),(1680,274),(1653,308)],fill='#fffdf8')
label(616,187,'“장을 덜 봤는데 카드값이 그대로야.”',36,anchor='mt')
label(1272,279,'“어디에 많이 쓰는지부터 보자.”',36,anchor='mt')

panel((58,392,1861,919),'#fffdfa')
label(85,423,'같은 100만 원 예산, 2025년 가격으로 다시 사면',42)
label(86,484,'공식 전년 대비 연평균  ·  식료품 +3.2%  ·  주거 관련 +1.6%',30)
x0=616
scale=.027
for n in (0,10000,20000,30000):
    x=x0+round(n*scale)
    d.line((x,553,x,836),fill='#a9a296' if not n else '#e4dccc',width=3)
    label(x,850,f'{n:,}',23,anchor='mt')
label(1480,850,'원',23)

shadow=Image.new('L',im.size)
sd=ImageDraw.Draw(shadow)
for y,value in [(607,27200),(756,20800)]:
    sd.ellipse((x0,y+26,x0+round(value*scale)+26,y+56),fill=122)
im.paste('#785f50',(0,0,*im.size),shadow.filter(ImageFilter.GaussianBlur(12)))

for y,name,share,val,light,dark in [
    (607,'식료품 비중 70%','주거 관련 30%',27200,(250,201,122),(153,71,24)),
    (756,'식료품 비중 30%','주거 관련 70%',20800,(141,207,239),(27,78,140)),
]:
    end=x0+round(val*scale)
    d.polygon([(x0,y-36),(x0+21,y-52),(end+21,y-52),(end,y-36)],fill=light,outline=dark)
    d.polygon([(end,y-36),(end+21,y-52),(end+21,y+16),(end,y+32)],fill=dark)
    for a in range(end-x0):
        for b in range(68):
            ratio=.10+.32*(a/(end-x0))+.36*(1-b/68)
            color=tuple(round(u+(v-u)*ratio) for u,v in zip(light,dark))
            im.putpixel((x0+a,y-36+b),color)
    d.line((x0+5,y-32,end-4,y-32),fill='#fff8de',width=3)
    panel((87,y-40,500,y+3),lemon)
    label(108,y-30,name,28)
    label(108,y+12,share,24)
    panel((1520,y-38,1818,y+38),'#f8f1e5')
    label(1669,y,f'+{val:,}원',43,red,'mm')

panel((58,936,1861,998),lemon)
label(960,954,'차이 6,400원   ·   우리 집 예산은 자주 쓰는 항목부터 확인',33,red,'mt')
label(61,1015,'같은 소비량 가정 · 두 항목만의 원화 월예산 예시  |  출처 국가데이터처 · 소비자물가지수 분석 사례',23)
with (root/'시각자료/EP169_장바구니와_생활비.png').open('xb') as target:
    im.save(target,format='PNG')
im.resize((960,540)).save('/tmp/trusta-ep169-preview.png')
