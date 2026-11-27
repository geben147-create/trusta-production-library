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


label(55,40,'주식만 올랐다면, 꼭 팔아야 60 대 40으로 돌아갈까?',53)
panel((56,136,1865,354),'#eadcca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(84,157),(151,173))
panel((256,168,913,259),'#fffaf0')
label(280,197,'“오른 주식을 48만 원 팔까?”',32)
d.polygon([(256,209),(227,224),(256,241)],fill='#fffaf0')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1675,169),(140,151))
panel((959,228,1649,319),'#fffaf0')
label(981,257,'“채권에 새 돈 80만 원을 넣어도 돼.”',31,red)
d.polygon([(1649,262),(1678,248),(1649,283)],fill='#fffaf0')
panel((56,380,1865,916),'#fffaf0')
label(97,408,'같은 목표 비중, 다른 총액',39)
panel((1098,399,1816,466),lemon)
label(1457,433,'파랑 주식  ·  주황 채권  ·  막대는 비중',27,anchor='mm')
x0,width=475,1035
for percent in (0,20,40,60,80,100):
    x=x0+round(width*percent/100)
    d.line((x,499,x,808),fill='#c9c0b4',width=2)
    label(x,823,f'{percent}%',22,anchor='mt')
for y,name,stock,bond in [(522,'1년 뒤 점검',720,400),(630,'주식 48만 원 이동',672,448),(738,'채권 80만 원 납입',720,480)]:
    label(93,y+18,name,29)
    total=stock+bond
    split=x0+round(width*stock/total)
    for left,right,amount,top,light,side in [
        (x0,split,stock,(25,63,111),(84,151,213),'#253f6a'),
        (split,x0+width,bond,(133,70,24),(230,155,77),'#80461e')]:
        d.polygon([(left,y),(right,y),(right+15,y-12),(left+15,y-12)],fill=light)
        if right==x0+width:
            d.polygon([(right,y),(right+15,y-12),(right+15,y+45),(right,y+57)],fill=side)
        for row in range(57):
            for col in range(9):
                color=tuple(round((a+(b-a)*row/56)*(1-.017*col)) for a,b in zip(top,light))
                d.line((left+(right-left)*col//9,y+row,left+(right-left)*(col+1)//9-1,y+row),fill=color)
        middle=(left+right)//2
        d.rounded_rectangle((middle-96,y+8,middle+96,y+48),9,fill=side)
        label(middle,y+28,f'{amount}만 원',25,'#fffaf0','mm')
    panel((1545,y+2,1815,y+52),'#eee3d6')
    label(1681,y+27,f'합계 {total:,}만 원',25,red if total==1200 else ink,'mm')
label(97,877,'처음 주식 600만 원·채권 400만 원에서 주식만 20% 오른 가상 1년',24)
label(55,947,'가상 원화 · 점검 전 입출금 없음 · 세금·비용·분배금 0 · 재투자 없음',24)
label(55,991,'출처  FINRA 자산배분과 분산투자  ·  미국 SEC 자산배분과 리밸런싱',23)
im.save(root/'시각자료/EP039_목표비중_다른총액.png')
im.resize((960,540)).save('/tmp/trusta-ep039-preview.png')
