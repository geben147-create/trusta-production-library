from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps

root=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1920,1080),'#faf3e6')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red,lemon='#25363b','#8a242c','#fff0a7'

def text(x,y,s,n,color=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=color,anchor=anchor)

def box(xy,color,edge=ink,r=20):
    d.rounded_rectangle(xy,r,fill=color,outline=edge,width=3)

def excerpt(name,xy,at):
    source=Image.open(root/'편집실/EP075_원자료'/name)
    factor=source.width/595
    crop=source.crop(tuple(round(v*factor) for v in xy))
    crop=crop.resize((1450,round(crop.height*1450/crop.width)),Image.Resampling.LANCZOS)
    im.paste(crop,at)
    return crop.height

text(56,25,'엔비디아, 매출은 전망 상단을 넘었는데',64)
box((57,122,793,170),lemon,lemon,14)
text(77,131,'회사 전망과 실제 실적 · 2025 회계연도 4분기',26)
text(837,131,'달러 매출 · GAAP 매출총이익률',26)

box((56,188,1593,402),'#fffdf7')
text(82,210,'이전 발표에서 제시한 4분기 전망',33)
height=excerpt('공식_Q3_2쪽.png',(45,24,570,52.8),(84,270))
d.line((87,270+height+9,1530,270+height+9),fill=red,width=5)

box((56,427,1593,686),'#fffdf7')
text(82,447,'실제 4분기 발표에서 읽은 매출과 이익률',32)
height=excerpt('공식_Q4_1쪽.png',(48,452,570,516),(84,494))
d.line((87,494+height+6,1530,494+height+6),fill=red,width=5)

box((1610,188,1868,686),'#ecd8bd')
refs=root/'집필인계'
for name,crop,y in [('천억이_시그니처표정.png',(45,0,236,241),260),('수건_캐릭터_사용자원본.png',(16,35,182,185),490)]:
    portrait=ImageOps.fit(Image.open(refs/name).crop(crop),(192,147),centering=(.5,.20))
    im.paste(portrait,(1645,y))
text(1740,217,'어느 전망?',23,ink,'mm')
text(1740,446,'회사 발표 범위!',22,red,'mm')

box((56,709,1868,938),lemon,'#ddc481')
text(85,731,'매출 비교',28)
text(84,778,'전망 상단 382.50억 달러 → 실제 393.31억 달러',42)
text(1789,797,'+2.83%',41,red,'rm')
text(84,859,'다음 분기 GAAP 매출총이익률 전망은 70.6% · 이번 실제 73.0%보다 2.4%p 낮음',27)
text(55,964,'회사 전망 기준 · 증권사 컨센서스와 실제 주가 변동은 별도 확인',23)
text(55,1019,'출처  NVIDIA · 회계연도 3분기 및 4분기 실적 발표',22)
im.save(root/'영상/EP075/엔비디아_전망과실제_원문.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep075-preview.png')
