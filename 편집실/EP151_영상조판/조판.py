from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

root=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#f8f2e7')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink='#172b36'
red='#91212d'

def txt(x,y,s,n,fill=ink,anchor='lt'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=fill,anchor=anchor)

def rounded(bounds,fill,outline=None):
    d.rounded_rectangle(bounds, radius=20,fill=fill,outline=outline,width=3)

def portrait(file,crop,at,size):
    art=ImageOps.fit(Image.open(root/'집필인계'/file).crop(crop),size)
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),radius=20,fill=255)
    im.paste(art,at,mask)

import csv
from datetime import date
from decimal import Decimal as D

rows=list(csv.DictReader((root/'편집실/EP151_원자료/SEC_총수익_전사.csv').open()))
names=['NVIDIA','SP500','Nasdaq100']
base={key:D(rows[5][key])/100 for key in names}
series={}
for key in names:
    series[key]=[(date.fromisoformat(row['date']),D(row[key]) if i<6 else D(row[key])*base[key]) for i,row in enumerate(rows) if i!=6]
assert round(series['NVIDIA'][-2][1]/100,2)==D('118.34')
txt(59,42,'엔비디아 100달러, 100배가 확인된 해는?',61)
rounded((60,126,1170,178),'#fff0aa')
txt(81,139,'2015년 같은 100달러 · 배당 재투자 · 개인 세금과 거래·환전비 제외',27)
rounded((54,208,1290,880),'#fffdfa','#baad96')
txt(79,234,'공시 연간 관측점의 가상 달러 잔액',29)
x0,x1,y0,y1=196,1241,779,345
start=series['NVIDIA'][0][0]
end=series['NVIDIA'][-1][0]
def x(day):
    return x0+round((day-start).days/(end-start).days*(x1-x0))
def y(value):
    return y0-round(float(value)/30000*(y0-y1))
for val in (0,10000,20000,30000):
    d.line((x0,y(val),x1,y(val)),fill='#abbab9',width=3 if val==0 else 1)
    txt(x0-15,y(val),f'{val:,}',22,ink,'rm')
for year,idx in [(2015,0),(2018,3),(2020,5),(2023,8),(2025,10)]:
    txt(x(series['NVIDIA'][idx][0]),809,str(year),25,ink,'mt')

def raise_line(values,palette):
    pts=[(x(day),y(value)) for day,value in values]
    shadow=Image.new('RGBA',im.size)
    sh=ImageDraw.Draw(shadow)
    sh.line([(a+5,b+8) for a,b in pts],fill=(24,44,59,105),width=12,joint='curve')
    shadow=shadow.filter(ImageFilter.GaussianBlur(6))
    im.paste(shadow,(0,0),shadow)
    for offset,color,width in [(2,palette[0],10),(0,palette[1],6),(-2,palette[2],2)]:
        d.line([(a,b+offset) for a,b in pts],fill=color,width=width,joint='curve')
    return pts

nv=raise_line(series['NVIDIA'],('#843310','#c8742a','#ffe4ad'))
raise_line(series['Nasdaq100'],('#10536d','#3285a0','#b0dae3'))
raise_line(series['SP500'],('#4a3b6b','#74639d','#d6c9ed'))
x_cross,y_cross=nv[-2]
d.ellipse((x_cross-8,y_cross-8,x_cross+8,y_cross+8),fill='#ffdb99',outline='#843310',width=3)
rounded((x_cross-265,y_cross-64,x_cross+13,y_cross-18),'#fff0aa')
txt(x_cross-253,y_cross-53,'2024년 약 118.34배',23,red)
txt(218,849,'연간 관측점 연결 · 정확한 최초 도달일은 별도 자료 필요',19)
rounded((1320,208,1864,880),'#f0e2cc','#baad96')
portrait('천억이_시그니처표정.png',(40,4,249,253),(1343,230),(124,145))
portrait('수건_캐릭터_사용자원본.png',(9,52,180,180),(1636,239),(184,125))
rounded((1456,273,1652,338),'#fffdfa',ink)
txt(1554,303,'중간도 봤어?',23,ink,'mm')
txt(1350,413,'2025년 1월 공시 관측값',25)
for i,(name,label,color) in enumerate(zip(names,('엔비디아','S&P 500','나스닥 100'),('#843310','#74639d','#3285a0'),strict=True)):
    yy=479+i*91
    rounded((1344,yy,1838,yy+67),'#fffdfa')
    d.ellipse((1361,yy+25,1379,yy+43),fill=color)
    txt(1394,yy+21,label,25)
    txt(1818,yy+33,f'{series[name][-1][1]:,.2f}달러',31,red if i==0 else ink,'rm')
txt(1350,776,'2018→2019 관측점 사이',26)
txt(1350,821,'엔비디아 약 34.18% 하락',31,red)
rounded((54,907,1864,975),'#fff0aa')
txt(80,927,'2020년부터 새로 시작했다면, 같은 2025년에도 엔비디아 약 22.87배',32,red)
txt(55,1015,'공시 관측 기간 2015년 1월 25일~2025년 1월 26일   |   출처  미국 SEC · 엔비디아 Form 10-K 주주 총수익 표',21)
out=root/'영상/EP151/백배의_달력.png'
im.save(out)
im.resize((960,540),Image.Resampling.LANCZOS).save(Path(__file__).with_name('축소검수.png'))
