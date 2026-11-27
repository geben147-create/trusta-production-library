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


label(58,40,'퇴직 후 대출금리 1%p 내리면 무조건 아낄까?',59)
panel((56,140,1864,352),'#f0e0cd')
portrait('천억이_시그니처표정.png',(39,8,251,249),(82,157),(158,176))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1654,155),(172,177))
panel((255,168,948,286),'#fffcf6')
panel((971,197,1640,313),'#fffcf6')
label(602,200,'“금리가 연 5%에서 4%로!”',36,anchor='mt')
label(1305,228,'“집 팔 때까지 몇 달 쓸 건데?”',36,anchor='mt')
panel((56,377,1864,902),'#fffdf8')
label(88,408,'원화 대출 잔액 1억 원 · 갈아타는 비용 60만 원',38)
label(90,464,'기간 이자 절감액 − 최초 전환비용 = 순절감액',28)
zero,scale=1180,15
for tick in (-20,-10,0,10,20):
    x=zero+tick*scale
    d.line((x,521,x,790),fill='#a79887' if not tick else '#e3dbce',width=3 if not tick else 2)
    label(x,805,f'{tick:+d}' if tick else '0',26,anchor='mt')
label(1520,805,'만 원',24)
for y,months,value,low,high in [(585,6,-10,(250,193,125),(154,74,36)),(725,9,15,(149,211,243),(35,85,143))]:
    left,right=sorted((zero,zero+value*scale))
    shade=Image.new('L',im.size)
    ImageDraw.Draw(shade).ellipse((left,y+20,right+28,y+49),fill=123)
    im.paste('#78604c',(0,0,*im.size),shade.filter(ImageFilter.GaussianBlur(10)))
    d.polygon([(left,y-27),(left+18,y-42),(right+18,y-42),(right,y-27)],fill=low)
    d.polygon([(right,y-27),(right+18,y-42),(right+18,y+12),(right,y+27)],fill=high)
    for dx in range(right-left):
        for dy in range(54):
            f=.1+.3*dx/(right-left)+.4*(1-dy/54)
            im.putpixel((left+dx,y-27+dy),tuple(round(a+(b-a)*f) for a,b in zip(low,high)))
    d.line((left+4,y-23,right-4,y-23),fill='#fff4d9',width=2)
    panel((92,y-33,589,y+33),lemon)
    label(340,y,f'{months}개월 뒤 전액 상환',33,anchor='mm')
    panel((1550,y-33,1817,y+33),'#f6ede0')
    label(1683,y,f'{value:+d}만 원',36,red if value<0 else ink,'mm')
panel((56,925,1864,993),lemon)
label(960,943,'비용이 같아지는 시점은 약 7.2개월 · 같은 날까지의 이자를 비교',32,red,'mt')
label(59,1010,'가상 고정 잔액의 단순 계산 · 종료일 양쪽 추가 비용 없음 | 출처 금융위원회 · 대환대출 비용 비교 안내',23)
with (root/'시각자료/EP173_이사와_대출갈아타기.png').open('xb') as stream:im.save(stream,format='PNG')
im.resize((960,540)).save('/tmp/trusta-ep173-preview.png')
