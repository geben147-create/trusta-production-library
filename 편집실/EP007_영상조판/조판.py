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


label(58,39,'보수 0.1%가 더 비싼 순간',62)
panel((57,135,1860,366),'#e9dcc9')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(88,167),(151,159))
panel((260,174,820,266),'#fffdf8')
label(287,202,'“그 돈, 석 달 뒤에 쓰잖아!”',33)
d.polygon([(261,217),(232,237),(261,244)],fill='#fffdf8')
portrait('천억이_시그니처표정.png',(39,8,251,249),(1657,160),(160,178))
panel((1069,206,1634,300),'#fffdf8')
label(1093,233,'“0.1%인데 2만 원 더 든다고?”',33,red)
d.polygon([(1634,248),(1665,229),(1634,272)],fill='#fffdf8')

panel((57,389,1860,937),'#fffdf8')
label(97,415,'원화 1,000만 원의 보유 기간별 가상 비용',37)
panel((1109,407,1809,474),lemon)
label(1459,441,'비교 기준  ·  연 비용 + 사고팔 때 비용',26,anchor='mm')
base=823
scale=0.44
for value in (0,20000,40000,60000):
    y=base-round(value/100*scale)
    d.line((212,y,1780,y),fill='#cbc5b9',width=2)
    label(186,y,f'{value:,}',23,anchor='rm')
label(113,501,'원',23)
for center,period,a,b in ((457,'석 달',32500,12500),(981,'15개월',42500,42500),(1510,'2년',50000,65000)):
    for shift,value,tint,start,end,edge in [(-139,a,'A',(16,58,113),(79,156,217),'#163e75'),(33,b,'B',(133,67,19),(233,161,62),'#81501d')]:
        x=center+shift
        y=base-round(value/100*scale)
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
        label(x+52,y-34,f'{tint} {value:,}',23,red if period=='석 달' and tint=='A' else ink,'mm')
    label(center,860,period,29,anchor='mt')
label(58,955,'세금·환전·분배금 0원  ·  기간 시장수익 0%  ·  재투자 없음  ·  연 비용률 단순 배분',25)
label(58,1007,'출처  미국 SEC ETF 투자자 안내  ·  미국 SEC 펀드 거래방식 비교',23)
im.save(root/'시각자료/EP007_은퇴후_ETF비용.png')
im.resize((960,540)).save('/tmp/trusta-ep007-preview.png')
