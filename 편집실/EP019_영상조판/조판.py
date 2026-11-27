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


label(55,39,'월세가 10% 줄었는데, 남는 돈은 왜 20% 줄었지?',54)
panel((55,138,1865,366),'#e9dcc9')
portrait('천억이_시그니처표정.png',(39,8,251,249),(87,158),(153,177))
panel((266,175,876,265),'#fffaf0')
d.polygon([(266,221),(231,232),(266,244)],fill='#fffaf0')
label(287,202,'“리츠 ETF도 월세처럼 들어올까?”',31)
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1672,183),(140,151))
panel((939,243,1640,330),'#fffaf0')
d.polygon([(1640,268),(1681,259),(1640,289)],fill='#fffaf0')
label(961,268,'“건물에서 돈이 어디로 가는지 보자.”',31,red)
panel((55,390,1865,919),'#fffaf0')
label(96,416,'가상 부동산의 두 회계연도 장부',40)
for x,color,caption in [(99,'#274d73','운영비'),(313,'#5c4976','이자'),(501,'#8c461a','남는 돈')]:
    d.rounded_rectangle((x,491,x+39,529),7,fill=color)
    label(x+55,496,caption,25)
panel((1113,483,1818,536),lemon)
label(1465,510,'같은 운영비 3천만 원과 이자 2천만 원',26,anchor='mm')
x0=384
for value in (0,20,40,60,80,100):
    x=x0+value*12
    d.line((x,570,x,792),fill='#cbc5b9',width=2)
    label(x,804,str(value*100) if value else '0',24,anchor='mt')
label(1660,804,'만 원',24)
for y,name,residual in ((588,'첫해',50),(714,'공실이 난 해',40)):
    label(96,y+27,name,32)
    left=x0
    for value,top,light,side in [
        (30,(25,62,105),(71,115,158),'#1d3c60'),
        (20,(57,43,85),(114,93,151),'#3f315a'),
        (residual,(132,67,23),(222,149,66),'#8a461c')]:
        right=left+value*12
        d.polygon([(left,y),(right,y),(right+16,y-14),(left+16,y-14)],fill=light)
        if value==residual:
            d.polygon([(right,y),(right+16,y-14),(right+16,y+58),(right,y+72)],fill=side)
        for row in range(72):
            for col in range(8):
                rgb=tuple(round((a+(b-a)*row/71)*(1-.013*col)) for a,b in zip(top,light))
                d.line((left+(right-left)*col//8,y+row,left+(right-left)*(col+1)//8-1,y+row),fill=rgb)
        mid=(left+right)//2
        d.rounded_rectangle((mid-82,y+13,mid+82,y+61),11,fill=side)
        label(mid,y+37,f'{value*100:,}',29,'#fffaf0','mm')
        left=right
label(95,861,'임대수입 1억 원 → 9천만 원',28)
label(1024,855,'잔액 5천만 원 → 4천만 원  (−20%)',32,red)
label(55,949,'가상 원화 예시  ·  건물 단계 현금  ·  세금·기타 비용·투자자 분배 제외',24)
label(55,994,'출처  미국 SEC 리츠 투자자 안내  ·  Vanguard VNQ 부동산 ETF 팩트시트',23)
im.save(root/'시각자료/EP019_월세에서_남는돈.png')
im.resize((960,540)).save('/tmp/trusta-ep019-preview.png')
