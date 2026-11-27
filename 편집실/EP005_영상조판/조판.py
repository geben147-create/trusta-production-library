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


label(55,45,'퇴직금 첫 ETF 주문, 200원을 더 낸 걸까?',59)
panel((54,145,580,913),'#e8dcca')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(80,174),(146,152))
panel((248,181,554,319),'#fffdf8')
label(270,208,'“같은 시각의',29)
label(270,258,'가격부터 봐!”',29)
d.polygon([(248,255),(221,238),(248,230)],fill='#fffdf8')
panel((94,375,531,550),lemon)
label(117,405,'한 좌당 비교',30)
label(117,465,'10,200원 vs 10,000원',31)
portrait('천억이_시그니처표정.png',(39,8,251,249),(85,590),(177,198))
panel((282,619,550,757),'#fffdf8')
label(301,650,'“100좌면',32)
label(301,701,'2만 원 차이?”',31,red)
d.polygon([(282,684),(258,668),(282,661)],fill='#fffdf8')
label(92,835,'주문 전 호가와 iNAV 시각 확인',24)

panel((610,145,1866,913),'#fffdf8')
label(663,184,'100좌 주문 영수증',47)
label(663,258,'가상 사례  ·  100좌 전량 매수 후 매도',27)
x0=875
scale=6.35
for value in (0,25,50,75,100):
    x=x0+round(value*scale)
    d.line((x,343,x,691),fill='#cfcac3',width=2)
    label(x,709,str(value),25,anchor='mt')
label(1562,709,'만 원',24)
for y,name,value,top,low,side in [(410,'매수',102,(16,66,130),(86,164,223),'#163e75'),(570,'매도',100,(144,75,22),(232,163,68),'#834316')]:
    label(663,y+41,name,34)
    x=x0+round(value*scale)
    d.rounded_rectangle((x0+2,y+95,x+21,y+110),7,fill='#ddd8cf')
    d.polygon([(x0,y),(x,y),(x+19,y-19),(x0+19,y-19)],fill=low)
    d.polygon([(x,y),(x+19,y-19),(x+19,y+77),(x,y+96)],fill=side)
    for row in range(96):
        progress=row/95
        for step in range(12):
            left=x0+round((x-x0)*step/12)
            right=x0+round((x-x0)*(step+1)/12)
            factor=1-0.14*(step/11)
            color=tuple(round((a+(b-a)*progress)*factor) for a,b in zip(top,low))
            d.line((left,y+row,right,y+row),fill=color)
    d.line((x0+5,y+7,x-4,y+7),fill=low,width=3)
    panel((1585,y+9,1824,y+87),'#f5efe2')
    label(1704,y+49,f'{value}만 원',39,anchor='mm')
panel((660,789,1819,873),lemon)
label(691,815,'괴리 해소 전후',29)
label(1077,814,'기준 가치가 그대로면  −2만 원 (−1.96%)',35,red)
label(55,952,'가상 원화 예시  ·  세금·비용·분배금 0원  ·  재투자 없음',26)
label(55,1006,'출처  미국 SEC ETF 투자자 안내  ·  삼성액티브자산운용 투자설명서',24)
im.save(root/'시각자료/EP005_퇴직금_첫ETF주문.png')
im.resize((960,540)).save('/tmp/trusta-ep005-preview.png')
