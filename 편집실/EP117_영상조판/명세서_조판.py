from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

root=Path(__file__).resolve().parents[2]
sheet=root/'편집실/EP117_원자료/공제명세서_6쪽.png'
im=Image.new('RGB',(1920,1080),'#faf3e5')
d=ImageDraw.Draw(im)
font='/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf'
ink,red='#243638','#89232c'

def text(x,y,s,n,color=ink,anchor='la'):
    d.text((x,y),s,font=ImageFont.truetype(font,n),fill=color,anchor=anchor)

def box(xy,fill,stroke=ink):
    d.rounded_rectangle(xy,22,fill=fill,outline=stroke,width=3)

text(54,29,'연말정산 서류에서 ISA 전환은 어디에 적힐까?',63)
text(59,120,'공식 빈 서식 확대 · 연금·저축 등 소득·세액 공제명세서',29)
box((52,178,1867,731),'#fffdf6')
with Image.open(sheet) as page:
    width,height=page.size
    heading=page.crop(tuple(round(v) for v in (width*.045,height*.061,width*.907,height*.083)))
    row=page.crop(tuple(round(v) for v in (width*.045,height*.308,width*.907,height*.393)))
    for source,xy in [(heading,(81,227)),(row,(81,390))]:
        source=ImageOps.contain(source,(1758,272),Image.Resampling.LANCZOS)
        im.paste(source,xy)

# 표시선은 원문의 인쇄 글자와 빈 칸 밖에 둔다.
d.line((101,377,1817,377),fill=red,width=8)
d.line((1435,667,1435,631),fill=red,width=8)
d.polygon([(1420,637),(1450,637),(1435,620)],fill=red)
text(115,670,'만기 전환 납입액을 별도 행에서 확인',32,red)
box((55,760,1865,968),'#f2e0c7')
mascot=Image.open(root/'집필인계/천억이_시그니처표정.png').crop((45,0,237,240))
mascot.thumbnail((155,169))
im.paste(mascot,(84,778))
d.polygon([(277,838),(232,861),(285,863)],fill='white',outline=ink,width=3)
box((269,799,961,881),'white')
text(610,841,'납입금액과 세액공제금액, 칸이 따로 있네!',30,ink,'mm')
text(1024,818,'금융사의 전환 처리 기록과',35,ink)
text(1024,876,'연말정산 자료의 구분을 대조해요.',34,red)
text(59,1016,'출처  국가법령정보센터 · 소득세법 시행규칙 별지 제24호서식(1)',23)
im.save(root/'영상/EP117/만기전환_공제명세서.png')
im.resize((960,540),Image.Resampling.LANCZOS).save('/tmp/trusta-ep117-form-preview.png')
