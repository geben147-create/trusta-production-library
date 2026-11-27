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


label(57,39,'QYLD 11.87%, 내 통장에 들어올 금액은?',57)
panel((56,138,1214,926),'#fffaf0')
label(92,172,'운용사 표의 세 줄',38)
label(92,230,'미국 기준 2026년 11월 25일',26)
for y,when,title,value,detail in [
    (287,'최근 1회','최근 분배 연환산율','11.87%','가장 최근 지급액으로 연간 규모 계산'),
    (462,'지난 12개월','후행 12개월 분배율','13.89%','지난 12개월 지급 내역을 반영'),
    (637,'지난 30일','30일 SEC 수익률','−0.02%','펀드 소득을 표준 방식으로 계산')]:
    panel((95,y,1170,y+153),'#eee2d3')
    panel((115,y+17,357,y+69),lemon)
    label(235,y+43,when,26,anchor='mm')
    label(385,y+23,title,33)
    label(385,y+88,detail,25)
    panel((924,y+30,1140,y+116),'#fffaf0')
    label(1033,y+71,value,40,red if value=='11.87%' else ink,'mm')
label(95,840,'세 수치는 각각 기간과 계산식이 다릅니다.',28)

panel((1241,138,1865,926),'#ebddc9')
portrait('천억이_시그니처표정.png',(39,8,251,249),(1266,170),(130,149))
panel((1410,177,1834,298),'#fffaf0')
d.polygon([(1410,222),(1389,241),(1410,254)],fill='#fffaf0')
label(1431,204,'“이번 달에',26)
label(1431,247,'얼마가 들어와?”',27)
panel((1279,360,1826,594),'#fffaf0')
panel((1305,384,1798,433),lemon)
label(1552,407,'공시 지급일 2026년 11월 27일',25,anchor='mm')
label(1308,466,'1주당 0.16달러',36)
label(1308,524,'가상 100주 → 세전 16달러',34,red)
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1687,666),(134,143))
panel((1280,671,1669,804),'#fffaf0')
d.polygon([(1669,730),(1692,712),(1669,751)],fill='#fffaf0')
label(1302,697,'“분배 이력에서',26)
label(1302,741,'주당 금액을 찾아.”',26,red)
label(1279,856,'환전·원천징수는 별도 확인',25)
label(56,947,'운용사 원문 표시값  ·  100주는 가상 보유 수량, 해당 지급 분배 자격 가정',23)
label(56,991,'출처  Global X QYLD 상품 안내 및 분배 이력',23)
im.save(root/'시각자료/EP043_QYLD_세줄과통장.png')
im.resize((960,540)).save('/tmp/trusta-ep043-preview.png')
