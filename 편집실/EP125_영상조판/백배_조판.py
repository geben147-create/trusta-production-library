from decimal import Decimal
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageColor,ImageFilter
import json

root=Path(__file__).resolve().parents[2]
audit=json.loads((root/'편집실/EP125_원자료/복리_검산.json').read_text())
im=Image.new('RGB',(1920,1080),'#fbf3e4')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#27373c','#87242c','#fff0a7'

def text(x,y,s,n,color=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=color,anchor=anchor)

def box(xy,color,stroke=ink,r=20):
    d.rounded_rectangle(xy,r,fill=color,outline=stroke,width=3)

def mascot(name,crop,pos,size):
    pic=ImageOps.fit(Image.open(root/'집필인계'/name).crop(crop),size,centering=(.5,.22))
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),17,fill=255)
    im.paste(pic,pos,mask)

def bubble(xy,tail,s):
    d.polygon(tail,fill='white',outline=ink,width=3)
    box(xy,'white')
    x,y,w,h=xy
    text((x+w)//2,(y+h)//2,s,29,ink,'mm')

text(54,22,'버크셔 100배, 그 전에 장부가 반 토막 났다',66)
box((55,120,712,165),lemon,lemon,13)
text(73,130,'같은 첫 구간 · 원금 1,000달러씩',28)
text(740,132,'연차보고서 표시 수익률을 연결한 결과',27)

box((54,185,1864,365),'#f1dfc6')
mascot('천억이_시그니처표정.png',(45,0,234,241),(78,202),(140,141))
bubble((202,198,712,257),[(236,248),(204,273),(255,250)],'백 배라면 계속 오른 거야?')
mascot('수건_캐릭터_사용자원본.png',(16,34,182,185),(1665,200),(164,145))
bubble((1001,272,1689,330),[(1624,277),(1694,252),(1664,278)],'1974년 장부부터 봐. 거의 반으로 줄었어!')
text(299,290,'1972년 말 약 6,466달러 → 1974년 말 약 3,234달러',28,red)

box((54,382,1864,871),'#fffdf6')
text(88,406,'보고서 관측점에서 처음 100배를 넘긴 해',36)
x0=486
def x(year):return x0+round((year-1964)*21.2)
d.line((x0,484,x0,788),fill='#789194',width=3)
for year in (1964,1974,1984,1994,2004,2014):
    xx=x(year)
    d.line((xx,774,xx,791),fill='#789194',width=3)
    text(xx,803,str(year),21,ink,'mt')
text(1830,803,'연도 눈금',20,ink,'rt')

def rail(year,y,top,bottom,side):
    end=x(year)
    shadow=Image.new('RGBA',im.size)
    ImageDraw.Draw(shadow).rounded_rectangle((x0+8,y+22,end+22,y+45),10,fill=(28,48,49,85))
    shadow=shadow.filter(ImageFilter.GaussianBlur(10))
    im.paste(shadow,(0,0),shadow)
    d.polygon([(x0,y-26),(x0+17,y-43),(end+17,y-43),(end,y-26)],fill=top,outline=side)
    d.polygon([(end,y-26),(end+17,y-43),(end+17,y+8),(end,y+25)],fill=side)
    a,b=ImageColor.getrgb(top),ImageColor.getrgb(bottom)
    for i in range(52):
        f=i/51
        d.line((x0,y-26+i,end,y-26+i),fill=tuple(round(v*(1-f)+w*f) for v,w in zip(a,b)))
    d.line((x0+5,y-23,end-6,y-23),fill='#e5f4ee',width=3)

for name,tick,y,colors in [
 ('Berkshire','버크셔 주당 시장가치',554,('#4c94b1','#a9d9e3','#396275')),
 ('SP500','배당 포함 S&P 500',694,('#b97834','#f6cf8f','#7b572d')),
]:
    result=audit['1965'][name]
    year=result['첫도달']['100']
    val=Decimal(result['연도별배수'][str(year)])
    text(90,y,tick,30,ink,'lm')
    rail(year,y,*colors)
    box((1576,y-46,1828,y+47),'#f9f3e7','#cfc2b1',12)
    text(1702,y-18,f'{year}년 말',29,red,'mm')
    text(1702,y+19,f'약 {val:.2f}배',25,ink,'mm')

box((54,890,1864,969),lemon,lemon,14)
text(80,910,'2000년부터 2024년 말까지 다시 계산하면 버크셔 약 12.12배, S&P 500 약 6.39배.',31)
text(57,988,'가상 미국달러 장부 · 연도별 평가점 · 개인 세금·거래비·환율 제외',22)
text(57,1029,'출처  Berkshire Hathaway · Annual Report, Berkshire’s Performance vs. the S&P 500',21)
im.save(root/'영상/EP125/백배_두장부.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep125-preview.png')
