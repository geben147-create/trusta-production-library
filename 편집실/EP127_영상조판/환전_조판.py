from decimal import Decimal as D
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageColor,ImageFilter

root=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#fbf2e3')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#26383b','#8a252c','#fff0a6'

def text(x,y,s,n,color=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=color,anchor=anchor)

def box(xy,color,edge=ink,r=21):
    d.rounded_rectangle(xy,r,fill=color,outline=edge,width=3)

def art(name,crop,xy,size):
    pic=ImageOps.fit(Image.open(root/'집필인계'/name).crop(crop),size,centering=(.5,.23))
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),17,fill=255)
    im.paste(pic,xy,mask)

text(55,21,'환율 우대 90%인데 왜 더 비싸지?',65)
box((56,121,715,169),lemon,lemon,13)
text(78,131,'원화 1,000만 원 · 같은 시점에 달러 왕복',28)
text(761,131,'기준환율 1달러 = 1,300원으로 고정한 가상 사례',26)

box((56,191,1868,525),'#eddbc0')
art('천억이_시그니처표정.png',(45,0,237,241),(78,225),(144,168))
box((77,405,365,487),'white')
text(221,430,'90%가 더 싸야지!',24,ink,'mm')
text(221,462,'왜 돈이 덜 남지?',24,ink,'mm')

art('수건_캐릭터_사용자원본.png',(16,36,184,183),(1660,228),(169,155))
box((1518,399,1842,490),'white')
text(1680,428,'얼마에서 깎았는지',25,ink,'mm')
text(1680,463,'먼저 봐야지.',26,ink,'mm')
for x,t,base,disc,applied in [(393,'영수증 A','2.00%','90%','0.20%'),(980,'영수증 B','0.50%','70%','0.15%')]:
    box((x,222,x+515,494),'#fffdf7','#bca78b',12)
    text(x+22,243,t,32)
    d.line((x+21,289,x+493,289),fill='#cfbea6',width=3)
    text(x+23,312,'기본 한쪽 스프레드',25)
    text(x+484,324,base,27,ink,'rm')
    text(x+23,363,'스프레드 우대율',25)
    text(x+484,374,disc,27,ink,'rm')
    text(x+23,423,'남은 한쪽 스프레드',25)
    text(x+484,440,applied,35,red,'rm')

box((55,549,1867,902),'#fffdf8')
text(86,572,'원화로 한 번 왕복한 비용',35)
text(587,582,'단위 만 원',22)
zero=459
scale=D('.024')
d.line((zero,640,zero,838),fill='#748e90',width=3)
for tick in (0,10000,20000,30000,40000):
    x=zero+int(tick*scale)
    d.line((x,834,x,846),fill='#748e90',width=3)
    text(x,860,str(tick//10000),21,ink,'mt')
for label,s,y,c0,c1,side in [
    ('A · 90%',D('.002'),674,'#c08243','#f9d69a','#7e5834'),
    ('B · 70%',D('.0015'),776,'#4c91a9','#afe4e7','#3b6672'),
]:
    fee=D(10000000)*(1-(1-s)/(1+s))
    end=zero+round(fee*scale)
    shadow=Image.new('RGBA',im.size)
    ImageDraw.Draw(shadow).rounded_rectangle((zero+10,y+26,end+20,y+43),8,fill=(21,43,46,72))
    shadow=shadow.filter(ImageFilter.GaussianBlur(8))
    im.paste(shadow,(0,0),shadow)
    d.polygon([(zero,y-24),(zero+15,y-39),(end+15,y-39),(end,y-24)],fill=c1,outline=side)
    d.polygon([(end,y-24),(end+15,y-39),(end+15,y+10),(end,y+25)],fill=side)
    a,b=ImageColor.getrgb(c0),ImageColor.getrgb(c1)
    for i in range(50):
        q=i/49
        d.line((zero,y-24+i,end,y-24+i),fill=tuple(round(v*(1-q)+w*q) for v,w in zip(a,b)))
    text(91,y,label,34,ink,'lm')
    box((1471,y-38,1829,y+39),'#f8f2e8','#d6c8b5',13)
    text(1650,y,f'{fee:,.0f}원',38,red,'mm')

text(57,934,'가상 비용 · 환율 변동·별도 수수료·세금 제외 · 원 단위에서 한 번 반올림',23)
text(57,988,'출처  하나은행 · 개인뱅킹 환전지갑 서비스 설명서 및 FX마켓 안내',22)
im.save(root/'영상/EP127/환전_두영수증.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep127-preview.png')
