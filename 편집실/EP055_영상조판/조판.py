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


label(55,39,'지수는 제자리인데, 인버스 ETF는 왜 손해일까?',54)
panel((55,143,1865,345),'#eadcca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(86,158),(147,167))
panel((254,168,903,257),'#fffaf0')
label(278,197,'“지수가 원래 자리로 돌아왔잖아!”',32)
d.polygon([(254,198),(226,212),(254,222)],fill='#fffaf0')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1679,175),(135,145))
panel((956,232,1656,320),'#fffaf0')
label(980,260,'“하루씩 반대로 움직인 결과를 더 봐.”',31,red)
d.polygon([(1656,259),(1683,245),(1656,276)],fill='#fffaf0')

panel((55,371,1865,918),'#fffaf0')
label(97,399,'이틀 동안 잔액이 움직이는 순서',38)
for x,day in [(505,'출발'),(961,'첫날 마감'),(1418,'둘째 날 마감')]:
    panel((x-145,487,x+145,542),lemon)
    label(x,514,day,29,anchor='mm')
for y,title,values in [(580,'가상 지수',['100','110','100']),(720,'가상 인버스',['1,000,000원','900,000원','981,818원'])]:
    label(92,y+35,title,26)
    for i,(x,value) in enumerate(zip((505,961,1418),values)):
        d.rounded_rectangle((x-150,y+12,x+165,y+105),20,fill='#bcb2a5')
        d.polygon([(x-155,y+12),(x-137,y-7),(x+158,y-7),(x+155,y+12)],fill='#a7c8e0')
        d.rounded_rectangle((x-155,y+12,x+155,y+95),17,fill='#e0ebf3',outline='#86a7bf',width=2)
        label(x,y+54,value,35,red if i==2 and y==720 else ink,'mm')
        if i<2:
            d.line((x+173,y+53,x+265,y+53),fill='#997d64',width=4)
            d.polygon([(x+265,y+43),(x+279,y+53),(x+265,y+63)],fill='#997d64')
label(96,865,'지수의 이틀 수익률 0%  ·  인버스 계좌의 이틀 손실 약 18,182원',29,red)
label(55,949,'가상 원화 100만 원 · 매일 비용 전 −1배 목표를 정확히 달성 · 세금·비용·환율·분배 제외',24)
label(55,995,'출처  미국 SEC 레버리지·인버스 ETF 안내  ·  ProShares SH 일일 목표',23)
im.save(root/'시각자료/EP055_인버스_이틀장부.png')
im.resize((960,540)).save('/tmp/trusta-ep055-preview.png')
