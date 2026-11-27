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


label(55,41,'ETF 청산 알림, 팔 수 있는 날과 돈 받는 날',57)
panel((55,140,1865,349),'#eadcca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(86,155),(149,169))
panel((258,164,884,259),'#fffaf0')
label(281,198,'“거래가 끝나면 내 돈도 없어져?”',32)
d.polygon([(258,214),(231,232),(258,238)],fill='#fffaf0')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1674,174),(141,150))
panel((941,228,1653,318),'#fffaf0')
label(966,256,'“마지막 거래일과 청산 예정일을 봐.”',31,red)
d.polygon([(1653,265),(1685,249),(1653,286)],fill='#fffaf0')

panel((55,374,1865,678),'#fffaf0')
label(96,403,'실제 공지  ·  Global X Metaverse ETF',37)
for x,date,purpose in [(463,'2024년 2월 16일','미국 정규장 거래 마감'),(1405,'2024년 2월 23일 전후','자산 정리·현금 분배 예정')]:
    d.rounded_rectangle((x-301,496,x+311,641),20,fill='#c6b39c')
    panel((x-310,482,x+302,630),lemon)
    label(x,520,date,33,anchor='mm')
    label(x,578,purpose,29,anchor='mm')
d.line((811,557,1036,557),fill='#936a49',width=7)
d.polygon([(1036,543),(1060,557),(1036,571)],fill='#936a49')

panel((55,702,1865,923),'#efe3d4')
label(96,730,'가상 10주 영수증',35)
label(96,793,'즉시 매도',26)
label(355,789,'188달러',37)
label(692,793,'청산 시',26)
label(859,789,'190달러 또는 185달러',37,red)
label(96,864,'지급 예정일과 실제 계좌 입금일은 각각 확인',25)
label(55,948,'가상 달러 원금 200달러 · 개인 세금·거래·환전 비용 및 분배·재투자 제외',24)
label(55,991,'출처  Global X 투자설명서 청산 보충문서',23)
im.save(root/'시각자료/EP057_청산_두날짜.png')
im.resize((960,540)).save('/tmp/trusta-ep057-preview.png')
