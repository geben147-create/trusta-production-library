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


label(56,41,'배당률은 올랐는데, 내 돈은 왜 줄었지?',57)
panel((56,144,711,875),'#eadcca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(86,173),(147,168))
panel((253,185,680,280),'#fffaf0')
d.polygon([(253,230),(227,241),(253,252)],fill='#fffaf0')
label(276,217,'“4%에서 5%로 올랐네?”',30)
panel((96,357,668,675),'#fffaf0')
label(128,389,'주식 1주의 표시 배당률',33)
label(128,461,'주가 100달러  ·  4달러 ÷ 100',27)
label(605,457,'4%',32,anchor='rt')
label(128,530,'주가 80달러  ·  4달러 ÷ 80',27)
label(605,526,'5%',33,red,'rt')
panel((126,591,634,637),lemon)
label(380,614,'분자 4달러는 그대로',25,anchor='mm')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(493,703),(141,149))
panel((87,733,466,812),'#fffdf8')
d.polygon([(466,751),(497,760),(466,780)],fill='#fffdf8')
label(109,760,'“주가가 먼저 내려갔어.”',26,red)
panel((744,144,1865,875),'#fffaf0')
label(790,184,'먼저 산 사람의 1년 장부',43)
label(790,248,'달러 100으로 산 주식 1주의 가상 결과',27)
base=690
scale=3.2
for value in (0,25,50,75,100):
    y=base-round(value*scale)
    d.line((937,y,1795,y),fill='#d3cbbd',width=2)
    label(915,y,str(value),23,anchor='rm')
label(828,320,'달러',23)
def bar(x,lower,upper,top,light,side):
    right=x+206
    bottom=base-round(lower*scale)
    y=base-round(upper*scale)
    d.polygon([(x,y),(right,y),(right+18,y-13),(x+18,y-13)],fill=light)
    d.polygon([(right,y),(right+18,y-13),(right+18,bottom-13),(right,bottom)],fill=side)
    for row in range(y,bottom):
        fraction=(row-y)/max(1,bottom-y-1)
        for col in range(10):
            fill=tuple(round((a+(b-a)*fraction)*(1-.015*col)) for a,b in zip(top,light))
            d.line((x+col*20,row,x+(col+1)*20+5,row),fill=fill)
    d.line((x+5,y+4,right-5,y+4),fill=light,width=2)

blue=((17,60,119),(81,158,218),'#203d6a')
bar(1040,0,100,*blue)
bar(1460,0,80,*blue)
bar(1460,80,84,(152,77,18),(245,179,73),'#925225')
panel((1038,305,1250,350),'#eee6d9')
label(1144,327,'100달러',28,anchor='mm')
panel((1458,345,1794,393),'#eee6d9')
label(1626,369,'주식 80 + 현금 4',27,anchor='mm')
label(1146,716,'매수 원금',27,anchor='mt')
label(1568,716,'1년 후 84달러',27,anchor='mt')
panel((785,776,1815,835),lemon)
label(1301,806,'보유 결과  −16달러 (−16%)',33,red,'mm')
label(56,935,'가상 달러 1주  ·  1년  ·  배당 재투자 없음  ·  세금·거래·환전 비용 0',25)
label(56,990,'출처  Schwab SCHD 상품 안내  ·  S&P 다우존스 배당지수 방법론  ·  Vanguard VYM 팩트시트',22)
im.save(root/'시각자료/EP015_배당률과_남은돈.png')
im.resize((960,540)).save('/tmp/trusta-ep015-preview.png')
