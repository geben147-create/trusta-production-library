from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

root=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#fbf3e4')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#25363a','#8a242c','#fff0a6'

def text(x,y,s,n,color=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=color,anchor=anchor)

def box(xy,color,edge=ink,r=21):
    d.rounded_rectangle(xy,r,fill=color,outline=edge,width=3)

def art(name,crop,where,size):
    pic=ImageOps.fit(Image.open(root/'집필인계'/name).crop(crop),size,centering=(.5,.28))
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),17,fill=255)
    im.paste(pic,where,mask)

def speak(xy,lines):
    box(xy,'white')
    x1,y1,x2,y2=xy
    for i,line in enumerate(lines):
        text((x1+x2)//2,y1+14+i*34,line,26,ink,'mt')

text(55,24,'분배락 날짜와 입금 예정일은 언제일까?',66)
box((57,123,661,169),lemon,lemon,13)
text(75,132,'KODEX 미국배당다우존스 · 489250',28)
text(695,132,'실제 2026년 10월 운용사 공지 일부',28)

box((56,190,1114,913),'#fffdf7')
text(82,215,'운용사 분배 일정 원문',34)
raw=Image.open(root/'편집실/FAQ03_원자료/삼성운용_지급일정.png').convert('RGB')
ratio=1000/raw.width
calendar=raw.crop((0,0,raw.width,2850)).resize((1000,round(2850*ratio)),Image.Resampling.LANCZOS)
im.paste(calendar,(85,268))
# Frame the three whole cells so their original dates and labels remain readable.
for a,b,c,e in [(493,399,676,616),(690,399,881,616),(91,659,279,876)]:
    d.rounded_rectangle((a,b,c,e),18,outline=red,width=5)

box((1137,190,1864,913),'#f2dfc7')
art('천억이_시그니처표정.png',(45,0,237,242),(1164,219),(137,148))
speak((1300,224,1835,302),['14일에 평가액이 움직였는데','왜 아직 현금이 없지?'])
art('수건_캐릭터_사용자원본.png',(16,35,182,183),(1657,348),(167,148))
speak((1162,380,1663,456),['입금은 지급 예정일을 봐.','이 회차는 19일이야.'])
d.polygon([(1310,266),(1286,278),(1307,285)],fill='white',outline=ink,width=3)
d.polygon([(1656,409),(1678,398),(1656,429)],fill='white',outline=ink,width=3)

box((1162,533,1834,634),'#fff9ec','#d1b99c')
text(1186,555,'공시 37원 × 가상 100좌',26)
text(1802,586,'세전 3,700원',37,red,'rm')
box((1162,665,1834,853),lemon,'#d8bf7c')
text(1186,686,'16일에 3,000원이 필요하다면?',29)
text(1186,745,'이번 예정일은 19일.',34,red)
text(1186,801,'16일에 쓸 현금은 따로 확인해요.',25)
text(58,947,'10월 19일은 운용사 공지의 지급 예정일 · 개인 계좌 입금 및 순액은 증권사에서 확인',24)
text(58,1002,'출처  삼성자산운용 · Kodex ETF 분배금 공지 및 지급 일정',23)
im.save(root/'영상/FAQ03/분배락_지급예정_원문달력.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-faq03-calendar.png')
