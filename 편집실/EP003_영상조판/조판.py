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


label(49,34,'ETF인 줄 알았는데 ETN이었다. 뭐가 다를까?',60)
panel((54,143,1868,905),'#fffdf8')
portrait('천억이_시그니처표정.png',(39,8,251,249),(95,186),(167,189))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1644,186),(180,187))
panel((284,199,959,276),'#f0e0cc')
panel((1003,286,1621,360),'#f0e0cc')
label(619,223,'“같은 지수니까 같은 상품?”',34,anchor='mt')
label(1312,308,'“누가 뭘 약속하는지 보자.”',34,anchor='mt')
d.polygon([(284,224),(255,242),(284,247)],fill='#f0e0cc')
d.polygon([(1620,309),(1648,293),(1620,332)],fill='#f0e0cc')

for x,heading,first,second in [(91,'주식','기업의 지분','그 회사의 주주'),(674,'ETF','펀드의 지분','운용 방식과 자산 확인'),(1257,'ETN','발행사의 채무증권','발행사 신용과 만기 확인')]:
    panel((x,416,x+544,642),'#f3ecdf')
    panel((x+25,440,x+160,501),lemon)
    label(x+92,468,heading,31,anchor='mm')
    label(x+27,524,first,36,red if heading=='ETN' else ink)
    label(x+27,587,second,26)
panel((90,686,1819,865),'#f4e5d2')
label(119,716,'가상 ETN의 지표가치가 105만 원이어도',36)
label(121,782,'그 94%에 거래소에서 팔면',29)
panel((1194,753,1785,829),'#fff2b5')
label(1490,791,'가상 매도액 98만 7,000원',36,red,'mm')
label(54,944,'가상 원금 100만 원 · 1년 지표 +5% · 투자자 세금·비용 제외 · 발행사 지급 불능 시 회수액은 별도',24)
label(54,995,'출처  한국거래소 · ETN 투자위험  |  미국 SEC · ETF 구조 안내',23)
with (root/'시각자료/EP003_같은지수와_다른권리.png').open('wb') as stream:im.save(stream,format='PNG')
im.resize((960,540)).save('/tmp/trusta-ep003-preview.png')
