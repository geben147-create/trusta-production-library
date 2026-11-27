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

txt(60,53,'예금은 만기인데, 병원비는 왜 중도해지?',63)
rounded((60,144,1860,203),'#fff0aa')
txt(82,160,'원금 3,000만 원 + 세전 이자 90만 원  ·  다음 달 병원비 500만 원  ·  가상 사례',31)

rounded((60,234,605,918),'#eee1d0','#ac9178')
portrait('천억이_시그니처표정.png',(39,8,251,252),(90,288),(215,232))
rounded((276,315,575,459),'#fffdf7',ink)
d.polygon([(276,370),(248,390),(276,404)],fill='#fffdf7',outline=ink,width=2)
txt(425,338,'만기 문자 왔는데',30,anchor='mt')
txt(425,391,'왜 또 묶였지?',34,red,'mt')
d.line((82,550,583,550),fill='#ad9477',width=3)
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(352,583),(222,204))
rounded((87,641,366,774),'#fffdf7',ink)
d.polygon([(366,679),(390,701),(366,716)],fill='#fffdf7',outline=ink,width=2)
txt(228,663,'만기 처리를',31,anchor='mt')
txt(228,716,'먼저 열어 봐.',32,red,'mt')

rounded((630,234,1860,918),'#fffdf8','#bda78f')
txt(666,270,'같은 만기 뒤, 결제할 통장에 있는 돈',39)
txt(1400,350,'즉시 쓸 수 있는 돈',28,anchor='mt')
txt(1707,350,'500만 원까지 부족액',26,anchor='mt')
d.line((675,403,1817,403),fill='#beaa93',width=3)
paths=[
    ('자동해지','원금과 이자 입금','3,090만 원','0원'),
    ('원금 재예치','이자만 입금','90만 원','410만 원'),
    ('원금+이자 재예치','두 금액을 다시 예치','0원','500만 원'),
]
for index,(title,detail,available,gap) in enumerate(paths):
    y=427+index*142
    rounded((664,y,1840,y+121),'#f0eadf' if index%2==0 else '#f7f3ec')
    txt(693,y+17,title,35)
    txt(693,y+68,detail,26)
    rounded((1281,y+22,1519,y+94),'#fffdfa')
    txt(1400,y+39,available,37,anchor='mt')
    rounded((1580,y+22,1833,y+94),'#fffdfa')
    txt(1707,y+39,gap,37,red if index else ink,'mt')
txt(68,969,'자동 처리가 정상 완료되고 다른 현금은 없다고 가정. 실제 입금액·새 만기일·일부 인출 조건은 내 계약에서 확인.',28)
output=root/'시각자료/EP159_만기문자와_병원비.png'
im.save(output)
