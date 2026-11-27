from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

root=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#fbf3e3')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#27373a','#8a252a','#fff0a6'

def text(x,y,s,n,color=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=color,anchor=anchor)

def box(coords,color,edge=ink,r=21):
    d.rounded_rectangle(coords,r,fill=color,outline=edge,width=3)

def art(p,crop,xy,size):
    pic=ImageOps.fit(Image.open(root/'집필인계'/p).crop(crop),size,centering=(.5,.3))
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),19,fill=255)
    im.paste(pic,xy,mask)

def bubble(coords,tail,s):
    d.polygon(tail,fill='white',outline=ink,width=3)
    box(coords,'white')
    x,y,w,h=coords
    text((x+w)//2,(y+h)//2,s,29,ink,'mm')

text(53,25,'같은 일봉인데 왜 내 계좌엔 매도 기록이 없을까?',61)
box((57,119,934,170),lemon,lemon,13)
text(76,129,'가상 1거래일 · 시가 10만, 고가 11만, 저가 9만, 종가 10만 원',27)
text(973,133,'매수 체결 뒤에만 매도 주문',26)

box((54,187,1866,380),'#f1dec4')
art('천억이_시그니처표정.png',(45,0,237,244),(82,209),(143,146))
bubble((219,201,760,261),[(248,251),(217,274),(265,254)],'9만 원에 사서 10만 5천 원에 팔면?')
art('수건_캐릭터_사용자원본.png',(16,35,181,180),(1643,205),(180,150))
bubble((1024,293,1669,355),[(1605,299),(1655,275),(1637,300)],'내가 주식을 산 다음에도 그 가격이 왔어?')
text(287,313,'원금 70만 원 중 한 칸에서만 주문',26,red)

def plot(x,prices,title,result,color):
    box((x,407,x+884,865),'#fffdf8')
    text(x+28,431,title,37)
    text(x+29,485,'시가 대비 변동 · 원',20)
    xs=[x+180,x+380,x+587,x+780]
    middle=645
    def y(delta):return round(middle-delta*.0086)
    for tick in (10000,5000,0,-10000):
        col='#b86c71' if tick==5000 else '#c5d1cc'
        d.line((x+153,y(tick),x+822,y(tick)),fill=col,width=3 if tick in (0,5000) else 1)
        text(x+143,y(tick),f'{tick:+,}' if tick else '0',18,red if tick==5000 else ink,'rm')
    coords=list(zip(xs,map(y,prices)))
    d.line([(i+4,j+7) for i,j in coords],fill='#c6c6b4',width=16,joint='curve')
    d.line(coords,fill=color,width=12,joint='curve')
    d.line([(i,j-3) for i,j in coords],fill='#9bd3c7' if color=='#236e64' else '#f0ad7c',width=4,joint='curve')
    for i,j in coords:
        d.ellipse((i-7,j-7,i+7,j+7),fill='white',outline=color,width=3)
    text(x+781,752,'시간 →',21,ink,'rm')
    box((x+27,788,x+858,851),'#fff1b5','#e8d189',12)
    text(x+445,819,result,29,red,'mm')

plot(55,[0,-10000,10000,0],'저가를 먼저 찍은 날','매수·매도 체결  ·  현금 715,000원','#236e64')
plot(981,[0,10000,-10000,0],'고가를 먼저 찍은 날','매수만 체결  ·  현금 + 주식 710,000원','#995331')

box((55,889,1866,964),'#ffeea0','#ffeea0')
text(85,908,'저가에 닿아도 내 매수가 미체결이면? 주식 없이 현금 700,000원이 남아요.',33)
text(58,985,'가상 원화 장부 · 비용·세금·분배금 제외 · 두 기본 경로는 지정가 체결 가정',22)
text(58,1026,'출처  미국 SEC · Understanding Order Types  /  한국거래소 · 코스닥시장 매매계약체결방법',21)
im.save(root/'영상/EP123/같은일봉_두영수증.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep123-preview.png')
