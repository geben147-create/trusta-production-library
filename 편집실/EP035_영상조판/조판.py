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


label(55,45,'관리비 10만 원, 분배금과 일부 매도 뒤에 남는 돈',54)
panel((56,140,1864,358),'#eadcca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(84,164),(152,170))
panel((259,166,947,255),'#fffaf0')
label(283,196,'“나는 한 주도 안 팔았어.”',31)
d.polygon([(260,209),(230,234),(260,231)],fill='#fffaf0')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1679,173),(138,148))
panel((969,234,1651,323),'#fffaf0')
label(993,263,'“관리비 내고 남은 돈을 비교해 봐.”',31,red)
d.polygon([(1650,269),(1683,250),(1650,287)],fill='#fffaf0')
panel((56,382,1864,917),'#fffaf0')
label(94,411,'가상 원화 100만 원의 하루 장부',41)
panel((1074,399,1814,463),lemon)
label(1444,432,'둘 다 현금 10만 원을 생활비로 사용',30,anchor='mm')
x0=461
step=10.45
for value in (0,20,40,60,80,100):
    x=x0+round(value*step)
    d.line((x,513,x,787),fill='#cdc5b8',width=2)
    label(x,804,f'{value:,}',22,anchor='mt')
label(1558,804,'만 원',23)
for y,rate in [(560,'분배금 사용'),(698,'10주 매도')]:
    label(94,y+21,rate,30)
    left=x0
    for value,top,light,side in [
        (90,(22,64,118),(80,151,210),'#234778'),
        (10,(133,69,23),(223,156,72),'#83491d')]:
        right=left+round(value*step)
        d.polygon([(left,y),(right,y),(right+17,y-13),(left+17,y-13)],fill=light)
        if value==10:
            d.polygon([(right,y),(right+17,y-13),(right+17,y+55),(right,y+68)],fill=side)
        for row in range(68):
            for col in range(8):
                rgb=tuple(round((a+(b-a)*row/67)*(1-.017*col)) for a,b in zip(top,light))
                d.line((left+(right-left)*col//8,y+row,left+(right-left)*(col+1)//8-1,y+row),fill=rgb)
        mid=(left+right)//2
        d.rounded_rectangle((mid-42,y+12,mid+42,y+55),9,fill=side)
        label(mid,y+34,f'{value:,}',26,'#fffaf0','mm')
        left=right
    panel((1540,y+6,1817,y+62),'#efe5d8')
    label(1679,y+35,f'90만 원 남음',27,red,'mm')
label(94,860,'파란색은 남은 ETF 평가액 · 주황색은 사용한 현금',26)
label(55,949,'가상 하루  ·  시장수익·세금·비용 0  ·  재투자 없음  ·  A만 주당 1천 원 분배',24)
label(55,992,'출처  미국 SEC 펀드 분배금 투자자 안내  ·  미국 SEC ETF 투자자 안내',23)
im.save(root/'시각자료/EP035_관리비_분배와매도.png')
im.resize((960,540)).save('/tmp/trusta-ep035-preview.png')
