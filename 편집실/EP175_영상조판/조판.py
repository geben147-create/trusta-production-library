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


label(53,35,'국민연금이 올랐는데, 생활비는 왜 더 모자랄까?',60)
panel((52,142,1868,903),'#fffdfa')
panel((77,172,595,873),'#efdeca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(124,302),(217,241))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(358,521),(177,189))
panel((105,202,567,276),'#fffdfa')
d.polygon([(223,275),(248,275),(235,296)],fill='#fffdfa')
label(336,225,'“입금이 올랐는데?”',33,anchor='mt')
panel((107,742,566,825),'#fffdfa')
d.polygon([(428,743),(450,743),(443,717)],fill='#fffdfa')
label(335,765,'“오른 항목만 계산해 봐.”',30,anchor='mt')

label(627,186,'늘어난 돈과 더 드는 돈',45)
panel((628,251,1823,306),lemon)
label(652,266,'국민연금 80만 원 + 고정 지급 40만 원 · 생활비 150만 원',29)
x0,scale=1003,.018
for tick in (0,10000,20000,30000):
    x=x0+round(tick*scale)
    d.line((x,367,x,706),fill='#a3988a' if not tick else '#e6dbcb',width=2)
    label(x,726,f'{tick:,}',25,anchor='mt')
for y,value,title,low,high in [(441,16800,'월 수입 증가액',(143,202,233),(29,74,137)),(620,31500,'월 생활비 증가액',(251,204,134),(164,81,27))]:
    end=x0+round(value*scale)
    shade=Image.new('L',im.size)
    ImageDraw.Draw(shade).ellipse((x0,y+20,end+22,y+56),fill=126)
    im.paste('#776050',(0,0,*im.size),shade.filter(ImageFilter.GaussianBlur(12)))
    d.polygon([(x0,y-28),(x0+18,y-44),(end+18,y-44),(end,y-28)],fill=low)
    d.polygon([(end,y-28),(end+18,y-44),(end+18,y+12),(end,y+28)],fill=high)
    for dx in range(end-x0):
        for dy in range(56):
            f=.10+.33*dx/(end-x0)+.35*(1-dy/56)
            im.putpixel((x0+dx,y-28+dy),tuple(round(a+(b-a)*f) for a,b in zip(low,high)))
    d.line((x0+4,y-24,end-4,y-24),fill='#fff6e4',width=2)
    label(646,y,title,32,anchor='lm')
    panel((1624,y-37,1828,y+37),'#f7eee3')
    label(1725,y,f'{value:,}원',32,red if value==31500 else ink,'mm')
label(1624,727,'원',24)
panel((631,787,1828,862),lemon)
label(1230,811,'부족액은 월 30만 원 → 31만 4,700원',35,red,'mt')
label(56,938,'원화 월 장부 가상 사례 · 생활비와 국민연금에 2.1% 적용 · 고정 지급액은 그대로',26)
label(56,994,'출처  국민연금공단 · 노령연금 안내 및 국민연금액 인상 안내',23)
with (root/'시각자료/EP175_연금통지서와_월생활비.png').open('wb') as stream:im.save(stream,format='PNG')
im.resize((960,540)).save('/tmp/trusta-ep175-preview.png')
