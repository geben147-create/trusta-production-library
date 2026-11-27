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

label(52,36,'퇴직한 회사 배당이 반으로 줄면, 생활비는?',62)
panel((51,138,667,933),'#f2e0c7')
panel((690,138,1871,689),'#fffefa')
panel((690,708,1871,933),'#fffefa')
portrait('천억이_시그니처표정.png',(39,8,251,249),(85,284),(239,270))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(403,552),(218,235))
panel((101,176,616,258),'#fffefa')
d.polygon([(195,257),(222,257),(204,281)],fill='#fffefa')
label(358,202,'“배당으로 빈 생활비를 채웠는데!”',29,anchor='mt')
panel((85,799,620,886),'#fffefa')
d.polygon([(458,800),(476,800),(467,777)],fill='#fffefa')
label(353,826,'“입금액부터 다시 적어 봐.”',34,anchor='mt')

label(725,172,'배당이 줄자 장부에 빈칸이 생겼다',44)
panel((728,226,1809,277),lemon)
label(751,241,'월 필수지출 220만 원 · 다른 고정수입 180만 원',29)
label(741,326,'줄기 전',32)
label(741,458,'줄어든 뒤',32)
x0,scale=968,13
for value in range(0,41,10):
    x=x0+value*scale
    d.line((x,305,x,536),fill='#a09483' if not value else '#ded5ca',width=2)
    label(x,552,str(value),24,anchor='mt')
label(1521,550,'만 원',23)

shadow=Image.new('L',im.size)
sd=ImageDraw.Draw(shadow)
for y,value in [(348,40),(480,20)]:
    sd.ellipse((x0,y+16,x0+value*scale+32,y+51),fill=135)
im.paste('#8a7866',(0,0,*im.size),shadow.filter(ImageFilter.GaussianBlur(11)))

for y,value,light,dark in [(348,40,(143,206,240),(28,79,134)),(480,20,(251,203,132),(158,70,26))]:
    end=x0+value*scale
    d.polygon([(x0,y-27),(x0+18,y-40),(end+18,y-40),(end,y-27)],fill=light)
    d.polygon([(end,y-27),(end+18,y-40),(end+18,y+14),(end,y+27)],fill=dark)
    for dx in range(end-x0):
        for dy in range(54):
            mix=.10+.34*dx/(end-x0)+.35*(1-dy/54)
            im.putpixel((x0+dx,y-27+dy),tuple(round(a+(b-a)*mix) for a,b in zip(light,dark)))
    d.line((x0+6,y-24,end-4,y-24),fill='#fff9e9',width=2)
    panel((1583,y-33,1810,y+36),'#f6ede0')
    label(1696,y,f'{value}만 원',38,red if value==20 else ink,'mm')

label(746,609,'직접 보유 주식에서 받는 월평균 배당',25)
label(732,744,'한 달 생활비의 빈칸',35)
label(732,802,'220만 원 − (180만 원 + 배당 20만 원)',32)
panel((1492,765,1812,874),lemon)
label(1652,803,'20만 원 부족',37,red,'mt')
label(53,973,'원화 가상 사례 · 연간 배당 480만 원 → 240만 원 · 투자자 세금·비용 및 ETF 분배금 제외',25)
label(53,1019,'출처  FINRA · 회사 주식과 ETF 보유 종목의 집중 위험',23)
target=root/'시각자료/EP171_사원증과_배당통장.png'
with target.open('xb') as stream:im.save(stream,format='PNG')
im.resize((960,540)).save('/tmp/trusta-ep171-preview.png')
