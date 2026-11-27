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


label(55,45,'마지막 출근날, 401(k) 3,000달러는 다 내 돈일까?',54)
panel((56,140,1864,358),'#eadcca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(84,164),(152,170))
panel((259,166,947,255),'#fffaf0')
label(283,196,'“잔액이 3,000달러라고 나오는데?”',31)
d.polygon([(260,209),(230,234),(260,231)],fill='#fffaf0')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1679,173),(138,148))
panel((969,234,1651,323),'#fffaf0')
label(993,263,'“회사가 넣은 돈은 귀속률을 확인해.”',31,red)
d.polygon([(1650,269),(1683,250),(1650,287)],fill='#fffaf0')
panel((56,382,1864,917),'#fffaf0')
label(94,411,'가상 퇴직일 장부',41)
panel((1074,399,1814,463),lemon)
label(1444,432,'본인 2,000달러 + 회사 1,000달러',30,anchor='mm')
x0=461
step=0.348
for value in (0,500,1000,1500,2000,2500,3000):
    x=x0+round(value*step)
    d.line((x,513,x,787),fill='#cdc5b8',width=2)
    label(x,804,f'{value:,}',22,anchor='mt')
label(1558,804,'달러',23)
for y,rate,company in [(560,'회사분 40% 귀속',400),(698,'회사분 전액 귀속',1000)]:
    label(94,y+21,rate,30)
    left=x0
    for value,top,light,side in [
        (2000,(22,64,118),(80,151,210),'#234778'),
        (company,(133,69,23),(223,156,72),'#83491d')]:
        right=left+round(value*step)
        d.polygon([(left,y),(right,y),(right+17,y-13),(left+17,y-13)],fill=light)
        if value==company:
            d.polygon([(right,y),(right+17,y-13),(right+17,y+55),(right,y+68)],fill=side)
        for row in range(68):
            for col in range(8):
                rgb=tuple(round((a+(b-a)*row/67)*(1-.017*col)) for a,b in zip(top,light))
                d.line((left+(right-left)*col//8,y+row,left+(right-left)*(col+1)//8-1,y+row),fill=rgb)
        mid=(left+right)//2
        d.rounded_rectangle((mid-56,y+12,mid+56,y+55),9,fill=side)
        label(mid,y+34,f'{value:,}',26,'#fffaf0','mm')
        left=right
    panel((1540,y+6,1817,y+62),'#efe5d8')
    label(1679,y+35,f'{2000+company:,}달러 귀속',27,red if company==400 else ink,'mm')
label(94,860,'귀속 금액과 실제 지급 가능액은 각각 확인',26)
label(55,949,'가상 플랜 1년 · 달러 기준 · 시장수익·세금·거래비용·분배금 0 · 재투자 없음',24)
label(55,992,'출처  미국 IRS 퇴직플랜 귀속 안내  ·  미국 IRS 401(k) 안내',23)
im.save(root/'시각자료/EP029_회사매칭_귀속잔액.png')
im.resize((960,540)).save('/tmp/trusta-ep029-preview.png')
