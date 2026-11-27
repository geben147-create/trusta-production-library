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

def mix(a,b,t):
    return tuple(round(x+(y-x)*t) for x,y in zip(a,b))

def glass(x,y,w,h,palette):
    depth=22
    shadow=Image.new('RGBA',im.size)
    sh=ImageDraw.Draw(shadow)
    sh.rounded_rectangle((x+11,y+18,x+w+45,y+h+19),radius=16,fill=(28,43,52,84))
    shadow=shadow.filter(ImageFilter.GaussianBlur(11))
    im.paste(shadow,(0,0),shadow)
    d.polygon([(x,y),(x+depth,y-depth),(x+w+depth,y-depth),(x+w,y)],fill=palette[1],outline=palette[0],width=2)
    d.polygon([(x+w,y),(x+w+depth,y-depth),(x+w+depth,y+h-depth),(x+w,y+h)],fill=palette[0])
    colors=Image.new('RGB',(w,h))
    px=colors.load()
    for yi in range(h):
        for xi in range(w):
            v=yi/(h-1)
            u=xi/(w-1)
            shade=.65+.26*v-.22*u
            if .17<v<.24:
                shade+=.12
            px[xi,yi]=mix(palette[0],palette[1],min(1,shade))
    im.paste(colors,(x,y))
    d.line((x+2,y+2,x+w-2,y+2),fill='#fff7ec',width=3)
    d.line((x+w-1,y+1,x+w-1,y+h),fill=palette[0],width=3)

txt(60,49,'같은 병원비 500만 원, 왜 환급은 다를까?',63)
rounded((60,140,1860,200),'#fff0aa')
txt(84,154,'같은 환자 납부액 500만 원  ·  같은 개인별 상한 200만 원  ·  가상 사례',31)
rounded((62,230,1858,444),'#eadcc9','#aa9077')
portrait('천억이_시그니처표정.png',(40,7,250,246),(82,245),(161,181))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1668,248),(165,171))
rounded((258,272,836,399),'#fffdf7',ink)
d.polygon([(258,306),(235,326),(258,347)],fill='#fffdf7',outline=ink,width=2)
txt(547,304,'나도 500만 원 냈는데?',39,anchor='mt')
rounded((866,272,1648,399),'#fffdf7',ink)
d.polygon([(1648,309),(1675,330),(1648,347)],fill='#fffdf7',outline=ink,width=2)
txt(1257,300,'영수증에서 상한에 들어가는 돈부터 봐.',36,red,'mt')
rounded((62,465,1858,958),'#fffdfa','#bfa88b')
txt(97,491,'상한제에 들어가는 금액을 비교해요',40)
x0, width = 360, 900
for val in range(0,501,100):
    x=x0+round(width*val/500)
    if val!=200:
        d.line((x,578,x,867),fill='#c3cdcf',width=3 if val==0 else 1)
    txt(x,884,str(val),25,anchor='mt')
for label,amount,exclude,y,color,refund in [
    ('영수증 A',350,150,626,((23,73,132),(132,214,248)),150),
    ('영수증 B',150,350,760,((146,71,16),(255,187,87)),0),
]:
    txt(102,y+9,label,34)
    glass(x0,y,round(width*amount/500),51,color)
    rounded((1308,y-12,1818,y+82),'#f2eee4')
    txt(1328,y+4,f'산입 {amount}만 원 · 제외 {exclude}만 원',26)
    txt(1328,y+42,f'상한 초과액 {refund}만 원' if refund else '상한 초과액 0원',29,red)
limit=x0+round(width*200/500)
d.line((limit,576,limit,856),fill=red,width=4)
txt(limit,547,'가상 상한 200',26,red,'mt')
txt(1790,894,'단위  만 원',24,anchor='rt')
txt(80,1005,'진료연도 개인별 비교 · 다른 지출 및 사전 지급 없음 · 실제 산입 내역과 상한액은 공단에서 확인',27)
im.save(root/'시각자료/EP161_두_퇴원영수증.png')
