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


label(55,43,'일본 ETF 거래대금 30만 엔, 새로 들어온 돈은?',54)
panel((54,138,1864,346),'#e9dcca')
portrait('천억이_시그니처표정.png',(39,8,251,249),(86,155),(147,169))
panel((255,168,895,257),'#fffaf0')
label(278,196,'“30만 엔이 펀드로 들어왔겠네?”',32)
d.polygon([(255,213),(228,232),(255,239)],fill='#fffaf0')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1679,170),(137,146))
panel((940,227,1652,316),'#fffaf0')
label(965,255,'“같은 100좌가 세 번 팔린 걸 수도 있어.”',29,red)
d.polygon([(1652,266),(1684,248),(1652,286)],fill='#fffaf0')

panel((54,369,1864,913),'#fffaf0')
label(96,402,'가상 하루 · 1좌 1,000엔',39)
x0=498
for value in (0,10,20,30):
    x=x0+31*value
    d.line((x,506,x,767),fill='#cfc5b8',width=2)
    label(x,793,str(value),24,anchor='mt')
label(1473,793,'만 엔',24)
label(96,558,'거래소 체결대금',33)
label(96,702,'펀드 순설정액',33)
x=x0+930
d.polygon([(x0,542),(x,542),(x+17,527),(x0+17,527)],fill='#85c8ec')
d.polygon([(x,542),(x+17,527),(x+17,608),(x,623)],fill='#24486e')
for row in range(81):
    for col in range(12):
        rgb=tuple(round((a+(b-a)*row/80)*(1-.012*col)) for a,b in zip((27,63,113),(74,155,209)))
        d.line((x0+930*col//12,542+row,x0+930*(col+1)//12,542+row),fill=rgb)
panel((1520,546,1795,614),'#efe5d6')
label(1657,580,'30만 엔',32,anchor='mm')
panel((1520,687,1795,755),'#efe5d6')
label(1657,721,'0엔',32,red,'mm')
d.line((x0,685,x0,750),fill='#263c50',width=5)
label(96,857,'NISA 적격은 계좌에 담을 수 있는지 확인하는 별도의 항목',25)
label(55,947,'가상 엔화 하루 · 같은 100좌 묶음 각각 10만 엔 · 신규 설정과 환매 없음',24)
label(55,991,'출처  일본거래소 ETF 매매 통계  ·  일본 금융청 NISA 안내  ·  미국 투자회사협회 ETF 안내',22)
im.save(root/'시각자료/EP065_거래대금과_순설정.png')
im.resize((960,540)).save('/tmp/trusta-ep065-preview.png')
