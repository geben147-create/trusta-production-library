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


label(54,40,'IRP에 현금 350만 원, 왜 ETF는 50만 원만?',62)
panel((53,144,1868,373),'#f2e0cb')
portrait('천억이_시그니처표정.png',(39,8,251,249),(82,162),(167,183))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1645,164),(181,180))
panel((260,174,945,274),'#fffefa')
panel((963,240,1629,338),'#fffefa')
d.polygon([(262,211),(229,228),(262,234)],fill='#fffefa')
d.polygon([(1627,261),(1651,249),(1627,285)],fill='#fffefa')
label(604,203,'“현금은 350만 원인데?”',38,anchor='mt')
label(1296,270,'“이미 담은 금액부터 빼 봐.”',35,anchor='mt')

panel((53,397,1868,953),'#fffdf9')
label(89,435,'전체 1,000만 원 × 70% = 위험자산 한도액 700만 원',43)
label(90,505,'일반 위험자산으로 분류된 ETF의 원화 가상 주문',29)
x0,scale,y=170,1.43,675
for tick in (0,200,400,600,800,1000):
    x=x0+round(tick*scale)
    d.line((x,601,x,766),fill='#b4a48e' if tick==0 else '#e6dfd4',width=2)
    label(x,779,f'{tick:,}',24,anchor='mt')
label(1662,777,'만 원',23)
for lo,hi,light,dark in [(0,650,(145,207,234),(31,79,134)),(650,700,(248,194,109),(165,73,25))]:
    left,right=x0+round(lo*scale),x0+round(hi*scale)
    d.polygon([(left,y-28),(left+17,y-44),(right+17,y-44),(right,y-28)],fill=light)
    d.polygon([(right,y-28),(right+17,y-44),(right+17,y+12),(right,y+28)],fill=dark)
    for dx in range(right-left):
        for dy in range(56):
            f=.12+.27*dx/(right-left)+.43*(1-dy/56)
            im.putpixel((left+dx,y-28+dy),tuple(round(a+(b-a)*f) for a,b in zip(light,dark)))
    d.line((left+5,y-23,right-5,y-23),fill='#fff8e8',width=2)
label(605,566,'이미 담은 650만 원',28,anchor='mt')
label(1184,566,'추가 여력 50만 원',29,red,'mt')
d.line((x0+round(700*scale),617,x0+round(700*scale),754),fill=red,width=4)
panel((90,837,1812,912),lemon)
label(950,861,'700만 원 − 650만 원 = 추가 주문 여력 50만 원',36,red,'mt')
label(57,976,'가격·비용·미체결 주문 반영 전 가정 · 실제 분류와 주문 가능액은 금융회사에서 확인',24)
label(57,1018,'출처  미래에셋증권 · 개인형 IRP 설명서',22)
with (root/'시각자료/EP023_IRP현금과_주문여력.png').open('xb') as stream:im.save(stream,format='PNG')
im.resize((960,540)).save('/tmp/trusta-ep023-preview.png')
