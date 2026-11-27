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

from decimal import Decimal as D
txt(57,45,'월분배 두 ETF, 그해 말 병원비를 낼 수 있었을까?',59)
rounded((59,127,1470,177),'#fff0aa')
txt(82,139,'2022년 시작 1만 달러씩 · 공시 NAV 총수익 · 분배금 재투자 반영',29)
rounded((60,216,515,922),'#e8d1b5','#b59e81')
portrait('천억이_시그니처표정.png',(40,4,250,253),(83,239),(151,177))
rounded((219,271,492,367),'#fffdfa',ink)
txt(354,302,'매달 입금되니까',26,ink,'mt')
txt(354,332,'괜찮겠지?',27,ink,'mt')
portrait('수건_캐릭터_사용자원본.png',(9,52,180,180),(279,423),(198,168))
rounded((81,454,288,550),'#fffdfa',ink)
txt(183,478,'연말 잔액도',25,ink,'mt')
txt(183,512,'보자고!',27,red,'mt')
rounded((83,652,488,859),'#fffdfa')
txt(109,676,'가상 병원비 고지서',27)
d.line((109,736,466,736),fill='#c9b9a9',width=2)
txt(109,757,'연말 납부',25)
txt(461,800,'9,000달러',41,red,'rt')
rounded((550,216,1857,922),'#fffdfa','#b59e81')
txt(585,242,'연말에 남은 달러',35)
x0,x1,y0=682,1793,747
scale=400/10000
def yy(n):
    return y0-round(n*scale)
for tick in (0,2500,5000,7500,10000):
    d.line((x0,yy(tick),x1,yy(tick)),fill='#aebcbc',width=3 if tick==0 else 1)
    txt(x0-12,yy(tick),f'{tick:,}',23,ink,'rm')
threshold=yy(9000)
d.line((x0,threshold,x1,threshold),fill=red,width=3)
rounded((1448,threshold-55,1785,threshold-9),'#fff0aa')
txt(1470,threshold-44,'병원비 9,000달러',25,red)
for center,ticker,returns,colors in [
    (985,'PFF',D('-.1837'),((119,58,15),(255,204,130))),
    (1440,'LQD',D('-.1801'),((19,78,118),(127,212,234))),
]:
    value=int(D(10000)*(1+returns))
    assert value in (8163,8199)
    left=center-110
    top=yy(value)
    height=y0-top
    shadow=Image.new('RGBA',im.size)
    sh=ImageDraw.Draw(shadow)
    sh.rounded_rectangle((left+15,y0-20,left+252,y0+29),15,fill=(20,34,48,99))
    shadow=shadow.filter(ImageFilter.GaussianBlur(12))
    im.paste(shadow,(0,0),shadow)
    d.polygon([(left,top),(left+29,top-23),(left+249,top-23),(left+220,top)],fill=colors[1],outline=colors[0])
    d.polygon([(left+220,top),(left+249,top-23),(left+249,y0-23),(left+220,y0)],fill=colors[0])
    front=Image.new('RGB',(220,height))
    for row in range(height):
        for col in range(220):
            w=.49+.35*row/height-.21*col/220+(.13 if col<9 else 0)
            front.putpixel((col,row),tuple(round(a+(b-a)*w) for a,b in zip(colors[0],colors[1])))
    im.paste(front,(left,top))
    d.line((left+3,top+3,left+215,top+3),fill='#fff5e4',width=3)
    txt(center,787,ticker,30,ink,'mt')
    rounded((center-153,836,center+153,882),'#fcebe4')
    txt(center,859,f'{value:,}달러 · {9000-value:,}달러 부족',24,red,'mm')
txt(65,970,'두 계좌에 월분배를 재투자한 공시 성과를 적용해도, 이 가상 지출은 부족했어요.',32,red)
txt(65,1020,'개인 세금·매매·환전비 제외  |  출처  iShares · PFF 및 LQD 팩트시트',24)
out=root/'영상/EP153/월분배와_병원비.png'
im.save(out)
im.resize((960,540),Image.Resampling.LANCZOS).save(Path(__file__).with_name('축소검수.png'))
