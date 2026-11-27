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


label(55,42,'연금저축 600만 원, 세금 90만 원은 어디서 줄까?',55)
panel((55,139,1866,339),'#eadbc9')
portrait('천억이_시그니처표정.png',(39,8,251,249),(83,155),(143,163))
panel((250,163,870,258),'#fffaf0')
label(273,192,'“연금 통장에 90만 원이 더 붙나?”',32)
d.polygon([(250,202),(221,222),(250,224)],fill='#fffaf0')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1677,168),(134,142))
panel((938,228,1654,310),'#fffaf0')
label(963,253,'“납입 확인서와 세금 명세서를 나눠 봐.”',31,red)
d.polygon([(1654,258),(1685,241),(1654,277)],fill='#fffaf0')

panel((55,362,1185,925),'#fffaf0')
label(96,389,'세금 명세서',42)
panel((647,386,1129,443),lemon)
label(887,415,'국세 · 적격 납입 600만 원',26,anchor='mm')
x0=337
for value in (0,30,60,90):
    x=x0+value*7
    d.line((x,475,x,760),fill='#ccc3b6',width=2)
    label(x,780,str(value),22,anchor='mt')
label(1021,780,'만 원',22)
for y,rate,value,top,light,side in [(517,'15%',90,(29,68,123),(82,165,218),'#264979'),(649,'12%',72,(138,71,19),(232,157,74),'#854718')]:
    label(102,y+28,rate,35)
    x=x0+value*7
    d.polygon([(x0,y),(x,y),(x+16,y-13),(x0+16,y-13)],fill=light)
    d.polygon([(x,y),(x+16,y-13),(x+16,y+51),(x,y+64)],fill=side)
    for row in range(64):
        for col in range(10):
            color=tuple(round((a+(b-a)*row/63)*(1-.015*col)) for a,b in zip(top,light))
            d.line((x0+(x-x0)*col//10,y+row,x0+(x-x0)*(col+1)//10,y+row),fill=color)
    panel((996,y+8,1148,y+57),'#f3eadc')
    label(1071,y+32,f'{value}만 원',26,red if value==90 else ink,'mm')
label(96,854,'적용 가능한 산출세액이 있다고 가정',27)

panel((1212,362,1866,925),'#f0e5d6')
label(1254,390,'투자계좌 명세서',40)
panel((1254,487,1824,635),'#fffaf0')
label(1281,516,'별도 ETF 가상 예시',29)
label(1281,566,'600만 원 × (1 − 10%)',33)
panel((1254,677,1824,804),'#fffaf0')
label(1280,706,'투자 평가액',29)
label(1783,753,'540만 원',46,red,'rt')
label(1254,853,'분배·비용·세금 0원 · 재투자 없음',25)
label(55,949,'법 적용 기준  2026년 7월 1일 시행  ·  지방소득세 제외  ·  실제 환급액은 기납부세액 등 대조',24)
label(55,999,'출처  국가법령정보센터 소득세법 연금계좌세액공제  ·  국세청 연금계좌 안내',23)
im.save(root/'시각자료/EP027_연금저축_두명세서.png')
im.resize((960,540)).save('/tmp/trusta-ep027-preview.png')
