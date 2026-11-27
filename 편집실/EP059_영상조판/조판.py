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


label(55,34,'생활비 때문에 ETF를 팔았다면?',65)
panel((54,140,1871,423),'#f2e0ca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(83,166),(179,212))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1647,161),(195,218))
panel((277,172,946,265),'#fffdfa')
panel((925,288,1628,380),'#fffdfa')
d.polygon([(277,202),(247,229),(277,229)],fill='#fffdfa')
d.polygon([(1627,315),(1657,292),(1627,346)],fill='#fffdfa')
label(612,199,'“팔고 나니까 바로 올랐어.”',36,anchor='mt')
label(1276,315,'“그전에 납부 날짜부터 봤어?”',35,anchor='mt')
panel((54,446,1199,954),'#fffdfa')
label(85,479,'매도한 뒤보다, 매도하기 전',41)
items=['언제 필요한 생활비인가','수익률을 같은 기간에 비교했나','ETF 속 같은 기업이 얼마나 겹치나','2배 목표가 적용되는 기간은','왕복 거래에 드는 비용은']
for i,item in enumerate(items,1):
    y=553+(i-1)*72
    panel((85,y-3,144,y+51),lemon)
    label(115,y+24,str(i),28,anchor='mm')
    label(164,y+8,item,30,red if i==1 else ink)

panel((1222,446,1872,954),'#fffdfa')
label(1254,482,'가격이 그대로여도',35)
label(1254,540,'100만 원 · 왕복 비용 0.2%',28)
label(1254,586,'10회 뒤 남는 돈',27)
panel((1255,637,1836,733),'#fff8d7')
label(1545,685,'980,179원',51,anchor='mm')
label(1254,777,'비용으로 약 19,821원 감소',30,red)
label(1254,852,'원화 가상 계산 · 세금·분배 제외',23)
label(55,994,'출처  FINRA · 분산투자 안내  |  미국 SEC · 레버리지 ETF 안내  |  Barber·Odean · 가계 거래 연구',22)
with (root/'시각자료/EP059_보일러영수증과_매도점검.png').open('xb') as stream:im.save(stream,format='PNG')
im.resize((960,540)).save('/tmp/trusta-ep059-preview.png')
