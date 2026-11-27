from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent
project = root.parent.parent
chart = root / 'glass'
geometry = json.loads((chart / 'geometry.json').read_text())['year2022']
assert geometry['values'] == [8787, 8477]
font = '/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
im = Image.new('RGB', (1920, 1080), '#f3eee6')
d = ImageDraw.Draw(im)

def draw(x, y, label, size, color='#182522'):
    for offset, line in enumerate(label.splitlines()):
        d.text((x, y + offset * (size + 8)), line, font=ImageFont.truetype(font, size), anchor='lt', fill=color)

def box(bounds, color, outline=None, radius=15):
    d.rounded_rectangle(bounds, radius=radius, fill=color, outline=outline, width=2)

draw(69, 51, '물가가 올랐는데, 1만 달러는 얼마가 됐을까?', 60)
box((69, 139, 1235, 197), '#fff1ab')
draw(92, 153, '2022년 초 → 연말  |  두 ETF에 각각 10,000달러', 33)
base = Image.open(chart / 'year2022.png').convert('RGB')
origin = (91, 214)
size = (1170, 731)
im.paste(base.resize(size, Image.Resampling.LANCZOS), origin)
for x, y, amount in geometry['ticks']:
    px, py = origin[0]+x*size[0], origin[1]+y*size[1]
    label = f'{int(amount):,}'
    f = ImageFont.truetype(font, 23)
    w = d.textlength(label, font=f)
    box((int(px-w-27),int(py-15),int(px-5),int(py+16)), '#fcfaf3')
    d.text((px-12,py),label,font=f,anchor='rm',fill='#263437')
for x,y,name,amount in zip((355,727),(846,846),('TIP','IEF'),geometry['values'],strict=True):
    box((x,y,x+275,y+65),'#fffdf6','#aca892')
    draw(x+14,y+18,f'{name}  {amount:,}달러',31)
box((1300,193,1850,934),'#faf7ef','#c6b8a8',20)
mascot = Image.open(project/'집필인계'/'천억이_시그니처표정.png').convert('RGB').crop((30,4,260,246))
mascot.thumbnail((225,225))
im.paste(mascot,(1325,233))
box((1558,252,1825,392),'white','#746a60')
draw(1575,272,'물가는 6.5%\n올랐는데?',32)
friend = Image.open(project/'집필인계'/'수건_캐릭터_사용자원본.png').convert('RGB').crop((16,45,182,198))
friend.thumbnail((225,194))
im.paste(friend,(1587,521))
box((1325,514,1585,683),'white','#746a60')
draw(1341,535,'채권값은\n금리에도\n반응해.',30)
box((1325,738,1825,883),'#fff2b8')
draw(1352,758,'310달러 더 남았지만',33)
draw(1352,814,'두 계좌 모두 손실',41,'#93202b')
draw(75,965,'가상 잔액 · 달러 NAV 총수익 · 분배금 재투자 · 개인 세금·거래비 제외',27)
draw(75,1011,'출처  iShares TIP·IEF 팩트시트 · 미국 노동통계국 CPI',24,'#5f6561')
out = project/'영상'/'EP129'/'물가와_채권_2022.png'
im.save(out)
im.resize((960,540),Image.Resampling.LANCZOS).save(root/'비교_축소검수.png')
