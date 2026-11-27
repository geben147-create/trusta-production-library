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


label(58,39,'퇴직을 1년 미루면 장부는 얼마나 달라질까?',62)
panel((57,135,1860,366),'#e9dcc9')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(88,167),(151,159))
panel((260,174,820,266),'#fffdf8')
label(287,202,'“이번 해에 천만 원을 꺼낼까?”',33)
d.polygon([(261,217),(232,237),(261,244)],fill='#fffdf8')
portrait('천억이_시그니처표정.png',(39,8,251,249),(1657,160),(160,178))
panel((1069,206,1634,300),'#fffdf8')
label(1093,233,'“더 일하면 천만 원을 넣는다면?”',33,red)
d.polygon([(1634,248),(1665,229),(1634,272)],fill='#fffdf8')

panel((57,389,1860,937),'#fffdf8')
label(97,415,'원화 1억 원으로 시작한 가상 2년 잔액',37)
panel((1109,407,1809,474),lemon)
label(1459,441,'A 첫해 1천만 원 납입  ·  B 첫해 1천만 원 출금',26,anchor='mm')
base=823
scale=0.0027
for value in (0,2500,5000,7500,10000):
    y=base-round(value*scale*1000/100)
    d.line((212,y,1780,y),fill='#cbc5b9',width=2)
    label(186,y,f'{value:,}',23,anchor='rm')
label(97,501,'만 원',23)
for center,period,a,b in ((576,'하락 먼저',10250,7750),(1335,'상승 먼저',9800,8200)):
    for shift,value,tint,start,end,edge in [(-139,a,'A',(16,58,113),(79,156,217),'#163e75'),(33,b,'B',(133,67,19),(233,161,62),'#81501d')]:
        x=center+shift
        y=base-round(value*scale*1000/100)
        end_x=x+105
        d.polygon([(x,y),(end_x,y),(end_x+15,y-13),(x+15,y-13)],fill=end)
        d.polygon([(end_x,y),(end_x+15,y-13),(end_x+15,base-13),(end_x,base)],fill=edge)
        for row in range(y,base):
            progress=(row-y)/max(1,base-y-1)
            for col in range(9):
                shade=1-col*.015
                color=tuple(round((c+(e-c)*progress)*shade) for c,e in zip(start,end))
                d.line((x+col*12,row,min(end_x,x+(col+1)*12),row),fill=color)
        d.line((x+4,y+5,end_x-4,y+5),fill=end,width=2)
        panel((x-27,y-54,x+131,y-16),'#f6ede0')
        label(x+52,y-34,f'{tint} {value:,}',23,red if period=='하락 먼저' and tint=='A' else ink,'mm')
    label(center,860,period,29,anchor='mt')
label(58,955,'연간 −20%와 +25% 순서만 변경  ·  둘째 해 둘 다 1천만 원 인출  ·  세금·비용 제외, 분배 재투자',25)
label(58,1007,'출처  미국 SEC 복리계산기  ·  Vanguard Research 약세장과 은퇴 인출 연구',23)
im.save(root/'시각자료/EP033_퇴직일_두장부.png')
im.resize((960,540)).save('/tmp/trusta-ep033-preview.png')
