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


label(56,39,'채권도 금리 뉴스에 잔고가 줄어들까?',57)
panel((55,138,1865,357),'#eadcca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(87,162),(151,167))
panel((265,167,892,263),'#fffaf0')
d.polygon([(266,215),(232,232),(266,239)],fill='#fffaf0')
label(292,196,'“다음 달 병원비인데, 왜 줄었지?”',34)
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1670,174),(146,155))
panel((947,229,1643,323),'#fffaf0')
d.polygon([(1643,268),(1676,253),(1643,291)],fill='#fffaf0')
label(970,257,'“같은 금리 충격도 민감도가 달라.”',33,red)

panel((55,380,1865,908),'#fffaf0')
label(95,412,'가상 채권 ETF의 순간 하락액',40)
panel((1100,403,1813,471),lemon)
label(1456,438,'비교 기준  ·  원화 100만 원  /  금리 +1%포인트',26,anchor='mm')
x0,scale=493,15
for mark in (0,1,2,3,4,5,6):
    x=x0+mark*100*scale//10
    d.line((x,520,x,780),fill='#cbc5b9',width=2)
    label(x,798,str(mark),25,anchor='mt')
label(1448,798,'만 원',25)
for y,years,amount,top,light,side in [
    (552,2,2,(24,70,126),(92,165,221),'#203d6a'),
    (680,6,6,(140,68,23),(235,161,79),'#914e21')]:
    label(95,y+21,f'수정듀레이션 {years}년',32)
    x=x0+amount*150
    d.rounded_rectangle((x0,y+67,x+21,y+77),5,fill='#e3dad0')
    d.polygon([(x0,y),(x,y),(x+18,y-14),(x0+18,y-14)],fill=light)
    d.polygon([(x,y),(x+18,y-14),(x+18,y+53),(x,y+67)],fill=side)
    for row in range(67):
        for step in range(10):
            col=tuple(round((a+(b-a)*row/66)*(1-.017*step)) for a,b in zip(top,light))
            d.line((x0+(x-x0)*step//10,y+row,x0+(x-x0)*(step+1)//10,y+row),fill=col)
    panel((1530,y+4,1790,y+63),'#f4eadf')
    label(1660,y+34,f'약 {amount}만 원 하락',30,red if years==6 else ink,'mm')
label(96,853,'팔 때의 가격을 비교합니다. 이자·분배금이나 보유기간 총수익은 별도입니다.',25)
label(55,942,'가상 원화 예시  ·  수익률곡선 평행 이동  ·  이자·분배·재투자·세금·비용 제외',25)
label(55,993,'출처  FINRA 금리 변화와 듀레이션  ·  Vanguard BND 팩트시트',23)
im.save(root/'시각자료/EP017_채권ETF_금리충격.png')
im.resize((960,540)).save('/tmp/trusta-ep017-preview.png')
