from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from decimal import Decimal as D

root = Path(__file__).resolve().parents[2]
image = Image.new('RGB',(1920,1080),'#f4ede0')
draw = ImageDraw.Draw(image)
font = '/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink, red, lemon = '#172b36','#8d222b','#fff1b2'

def text(x,y,label,size,color=ink,anchor='lt'):
    draw.text((x,y),label,fill=color,font=ImageFont.truetype(font,size),anchor=anchor)

def panel(box,fill='#fffdf8'):
    draw.rounded_rectangle(box,18,fill=fill,outline='#bda88c',width=2)

def portrait(name,crop,xy,size):
    art=ImageOps.fit(Image.open(root/'집필인계'/name).crop(crop),size)
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),20,fill=255)
    image.paste(art,xy,mask)

text(48,42,'은퇴 생활비 1만 달러, 같은 미국 국채인데?',65)
panel((48,143,453,959))
panel((470,143,1448,959))
panel((1465,143,1872,959))
portrait('천억이_시그니처표정.png',(39,8,251,249),(76,344),(347,400))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1499,349),(338,380))
for box, x, lines in [
    ((74,198,427,309),250,['치과 잔금을','여기서 낼 수 있겠지?']),
    ((1490,197,1847,311),1668,['두 상품의','만기 범위부터 봐.'])
]:
    panel(box,'#f4e7d6')
    draw.polygon([(x-19,box[3]-1),(x+20,box[3]-1),(x+4,box[3]+23)],fill='#f4e7d6')
    for j,line in enumerate(lines):text(x,box[1]+18+j*43,line,30,anchor='mt')
panel((76,783,425,908),lemon)
text(250,807,'납부일 · 금액 · 통화',29,anchor='mt')
text(250,853,'고지서에서 먼저 확인',25,anchor='mt')
panel((1492,783,1844,908),'#fbe5db')
text(1668,805,'2022년 한 해 예시',28,anchor='mt')
text(1668,851,'IEF는 523달러 부족',28,red,'mt')

text(505,182,'2021년 초 1만 달러씩 → 2025년 말',38)
text(505,241,'공시 총수익률로 재계산한 가상 잔액 · USD',25)
base, scale = 800, D('0.036')
shadow=Image.new('RGBA', image.size)
sd=ImageDraw.Draw(shadow)
for x in (837,1180):sd.ellipse((x-112,base-7,x+122,base+31),fill=(40,27,17,72))
image.paste(shadow.filter(ImageFilter.GaussianBlur(12)), (0,0), shadow.filter(ImageFilter.GaussianBlur(12)))
for val in (0,4000,8000,12000):
    y=base-int(D(val)*scale)
    draw.line((626,y,1387,y),fill='#9d9386' if not val else '#e1d8cb',width=3 if not val else 2)
    text(614,y,f'{val:,}',23,anchor='rm')

def crystal(x,value,label,period,low,high):
    top=base-round(D(value)*scale)
    width, depth=149,31
    draw.polygon([(x+width,top),(x+width+depth,top-17),(x+width+depth,base-17),(x+width,base)],fill=high)
    for dy in range(base-top):
        for dx in range(width):
            mix=min(.91,.12+.48*(1-dy/(base-top))+.27*(dx/width))
            light=.19*max(0,1-abs(dx-25)/24)
            color=tuple(round((a*(1-mix)+b*mix)*(1-light)+255*light) for a,b in zip(low,high))
            image.putpixel((x+dx,top+dy),color)
    draw.polygon([(x,top),(x+depth,top-17),(x+width+depth,top-17),(x+width,top)],fill=low,outline=high)
    draw.line((x+3,top+4,x+width-3,top+4),fill='#fff8ec',width=2)
    center=x+width//2
    panel((center-147,293,center+147,351))
    text(center,305,f'{D(value):,.2f} 달러',32,anchor='mt')
    draw.line((center,353,center,top-6),fill='#827768',width=2)
    text(center,831,label,41,anchor='mt')
    panel((center-120,886,center+120,932),lemon)
    text(center,893,period,26,anchor='mt')

crystal(754,'11722.01','SGOV','0~3개월',(131,202,233),(23,76,136))
crystal(1098,'9121.93','IEF','7~10년',(252,205,126),(169,78,22))
text(49,980,'미화 · 분배금 재투자 · 투자자 세금·거래비용·환전 제외  |  9,000달러 인출 부족분은 2022년 별도 예시',25)
text(49,1026,'출처  iShares · SGOV 및 IEF 상품 설명과 달력연도별 총수익률',21)
target=root/'시각자료/EP167_치과잔금과_국채유리차트.png'
with target.open('xb') as f:image.save(f,format='PNG')
