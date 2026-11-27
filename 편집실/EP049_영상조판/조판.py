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


label(52,42,'분배금은 받을 예정인데, ETF값은 왜 떨어졌을까?',61)
panel((54,147,1869,405),'#eedecb')
portrait('천억이_시그니처표정.png',(39,8,251,249),(82,168),(182,211))
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1627,171),(195,204))
panel((279,172,956,266),'#fffdfa')
panel((955,277,1611,371),'#fffdfa')
d.polygon([(278,199),(253,221),(278,232)],fill='#fffdfa')
d.polygon([(1611,299),(1640,280),(1611,323)],fill='#fffdfa')
label(617,200,'“1만 원이 9,800원으로 줄었어!”',34,anchor='mt')
label(1286,307,'“받을 분배금도 장부에 적어.”',34,anchor='mt')
panel((54,430,1869,932),'#fffdfa')
label(89,463,'받을 돈을 포함한 1주 장부',43)
for x,y,title,value,color in [
    (120,554,'전날 주당 NAV','10,000원',ink),
    (700,554,'오늘 주당 NAV','9,800원',ink),
    (1290,554,'받을 분배금','150원',red),
]:
    panel((x,y,x+514,y+157),lemon if color==red else '#f2ebdf')
    label(x+257,y+28,title,32,anchor='mt')
    label(x+257,y+82,value,46,color,'mt')
label(648,622,'→',42)
label(1230,622,'+',42)
panel((92,761,1827,887),'#f1e4d2')
label(125,791,'9,800원 + 150원 = 9,950원',40)
label(1775,791,'분배 포함 가치 50원 감소',37,red,'rt')
label(56,962,'원화 가상 1주 · 받을 권리 가정 · 세금·비용·재투자 없음 · 실제 입금일은 별도',25)
label(56,1012,'출처  미국 SEC · 펀드 분배금 안내 및 ETF 구조 안내',22)
with (root/'시각자료/EP049_분배금과_한주장부.png').open('wb') as stream:im.save(stream,format='PNG')
im.resize((960,540)).save('/tmp/trusta-ep049-preview.png')
