from decimal import Decimal as D
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

root = Path(__file__).resolve().parents[2]
im = Image.new('RGB', (1920, 1080), '#fbf5e6')
draw = ImageDraw.Draw(im)
font = '/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink, red, lemon = '#222f34', '#881e24', '#fff1ab'

def label(x, y, value, size, color=ink, anchor='la'):
    draw.text((x,y), value, font=ImageFont.truetype(font,size), fill=color, anchor=anchor)

def panel(box, color):
    draw.rounded_rectangle(box, 27, fill=color, outline=ink, width=3)

def bubble(box, tail, value, size, color=ink):
    draw.polygon(tail, fill='white', outline=ink, width=3)
    draw.rounded_rectangle(box, 25, fill='white', outline=ink, width=3)
    label((box[0]+box[2])//2, (box[1]+box[3])//2, value, size, color, 'mm')

label(58, 22, '연 0.4%p 아끼는 ETF, 지금 갈아탈까?', 72)
draw.rounded_rectangle((62,121,460,165), 13, fill=lemon)
label(77, 129, '같은 원금 · 같은 시장 노출', 28)
label(492, 129, '오늘 2,000만 원 · 교체 비용 18만 원', 28)

panel((54,185,1333,868), '#fffdf6')
label(96, 210, '교체 후 잔액 − 보유 유지 잔액', 43)
label(96, 266, '마이너스면 유지가, 플러스면 교체가 앞서요.', 29)
baseline, scale = 761, 0.00375
draw.line((baseline,329,baseline,804), fill='#607478',width=4)
label(baseline,815,'0원',22,ink,'mt')

def lerp(a,b,t):
    return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))

for n, y in [(1,398),(2,559),(3,720)]:
    today = D(20000000)
    delta = round((today-180000)*D('1.059')**n - today*D('1.055')**n)
    end = baseline+round(delta*scale)
    lo, hi = sorted((baseline,end))
    top = y-34
    shadow = Image.new('RGBA', im.size)
    ImageDraw.Draw(shadow).rounded_rectangle((lo+9, y+24, hi+21,y+54), 10,fill=(14,38,44,75))
    im.paste(shadow.filter(ImageFilter.GaussianBlur(11)),(0,0),shadow.filter(ImageFilter.GaussianBlur(11)))
    light, dark = ((255,205,125),(141,67,16)) if delta<0 else ((98,213,239),(13,76,119))
    draw.polygon([(lo,top),(lo+15,top-16),(hi+15,top-16),(hi,top)], fill=lerp(light,dark,.26), outline=dark)
    draw.polygon([(hi,top),(hi+15,top-16),(hi+15,top+53),(hi,top+69)],fill=dark)
    for k in range(70):
        draw.line((lo,top+k,hi,top+k),fill=lerp(light,dark,.22+.56*(k/69)**.8))
    draw.line((lo+3,top+4,hi-3,top+4),fill=lerp(light,(255,255,255),.65),width=3)
    label(99,y,str(n)+'년 말',32,ink,'lm')
    draw.rounded_rectangle((1011,y-41,1289,y+41),15,fill='#f7f2e8',outline='#ddd6ca',width=2)
    sign = '+' if delta>0 else '−'
    label(1150,y,f'{sign}{abs(delta):,}원',41,red if delta>0 else ink,'mm')

panel((1355,185,1865,868), '#ead7bd')
refs = root/'집필인계'
towel = Image.open(refs/'수건_캐릭터_사용자원본.png').crop((12,34,186,187))
towel = ImageOps.fit(towel,(282,219))
mask = Image.new('L',towel.size)
ImageDraw.Draw(mask).rounded_rectangle((0,0,281,218),25,fill=255)
im.paste(towel,(1395,234),mask)
bubble((1452,196,1842,258),[(1510,252),(1502,279),(1547,251)],'오늘 18만 원이 빠져.',31)

shock = Image.open(refs/'천억이_시그니처표정.png').crop((46,0,237,244))
shock.thumbnail((205,252))
im.paste(shock,(1607,516))
bubble((1381,477,1816,541),[(1681,532),(1704,560),(1744,532)],'앗, 3년째에야 앞서네!',33,red)
label(1610,790,'돈 쓸 날짜부터 확인!',35,ink,'mm')

draw.rounded_rectangle((56,895,1864,973),22,fill=lemon)
label(82,922,'반례',30,red)
label(190,918,'교체 비용이 3만 원이면 첫해부터 교체 잔액이 48,230원 더 커요.',37)
label(62,989,'가상 계산 · 원화 · 비용 전 연 6% · 분배금 재투자 · 세금과 종료 시 거래비 제외',23)
label(62,1028,'출처  미국 SEC · 투자 비용 및 ETF 비용 안내',22)
im.save(root/'영상/EP111/교체비_달력.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep111-preview.png')
