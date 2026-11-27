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

txt(58,46,'퇴직한 해의 병원비, 두 장 다 공제될까?',64)
rounded((60,135,1858,191),'#fff0aa')
txt(81,150,'6월 30일 퇴직 후 재취업 없음  ·  총급여 3,000만 원  ·  의료비 각 120만 원  ·  가상 사례',29)
rounded((60,220,1858,665),'#fffdfa','#b59c80')
portrait('천억이_시그니처표정.png',(39,8,251,249),(92,248),(170,182))
rounded((283,250,817,349),'#f5e7d4')
txt(550,277,'둘 다 올해 낸 병원비인데?',36,anchor='mt')
portrait('수건_캐릭터_사용자원본.png',(23,30,184,187),(1632,246),(192,182))
rounded((1059,250,1609,349),'#f5e7d4')
txt(1334,276,'퇴직일 앞뒤부터 확인해.',35,red,'mt')
d.polygon([(283,279),(263,294),(283,309)],fill='#f5e7d4')
d.polygon([(1609,279),(1631,294),(1609,309)],fill='#f5e7d4')
txt(1700,572,'날짜 순서 도식',22,anchor='rt')
d.line((188,497,1742,497),fill='#6e7c81',width=6)
for x,y,label,detail,c in [
    (469,417,'6월 20일','근로기간 중 120만 원',ink),
    (954,417,'6월 30일','퇴직',red),
    (1420,417,'8월 20일','퇴직 뒤 120만 원',red),
]:
    d.ellipse((x-13,484,x+13,510),fill=c)
    txt(x,y,label,35,c,'mt')
    txt(x,535,detail,28,c,'mt')
rounded((60,695,1858,970),'#f0e8d9','#b59c80')
txt(95,725,'같은 해에도 실제 근로기간을 확인',37)
txt(101,797,'근로기간 중 120만 원 − 총급여의 3%인 90만 원 = 30만 원',31)
rounded((1055,783,1812,902),'#fffdf7')
txt(1434,817,'계산상 소득세 세액공제 4만 5,000원',33,red,'mt')
txt(76,1008,'2026년 귀속 가정 · 본인 의료비 · 다른 공제·보전액·지방소득세 제외 · 실제 정산 환급액은 별도',26)
im.save(root/'시각자료/EP165_퇴직일과_두영수증.png')
