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

txt(55,47,'금리는 같은데, 이자는 왜 23만 1천 원 차이?',64)
rounded((55,132,1374,183),'#fff0aa')
txt(79,145,'가상 원금 5천만 원 · 연 3.00% 단리 · 1년 만기 · 원화 · 비용 0원',29)
d.rounded_rectangle((49,211,1867,797),28,fill='#e8d1b5')
for y in (290,516,738):
    d.line((51,y,1865,y),fill='#dbc1a2',width=2)
portrait('천억이_시그니처표정.png',(40,3,252,252),(78,288),(241,283))
portrait('수건_캐릭터_사용자원본.png',(9,52,180,180),(1541,395),(285,250))
rounded((74,595,349,719),'#fffdf7',ink)
d.polygon([(167,595),(194,568),(213,595)],fill='#fffdf7',outline=ink,width=2)
txt(211,622,'둘 다 3%인데',31,ink,'mt')
txt(211,666,'왜 달라?',33,ink,'mt')
rounded((1499,243,1837,363),'#fffdf7',ink)
d.polygon([(1635,363),(1660,386),(1687,363)],fill='#fffdf7',outline=ink,width=2)
txt(1670,270,'입금된 이자를',31,ink,'mt')
txt(1670,313,'옆에 놓아 봐!',31,ink,'mt')

def receipt(x,title,tax,net):
    y=253
    width=529
    height=470
    shadow=Image.new('RGBA',im.size)
    layer=ImageDraw.Draw(shadow)
    layer.rounded_rectangle((x+8,y+17,x+width+15,y+height+22),radius=16,fill=(58,39,19,105))
    shadow=shadow.filter(ImageFilter.GaussianBlur(13))
    im.paste(shadow,(0,0),shadow)
    d.rectangle((x,y,x+width,y+height),fill='#fffdfa')
    start=x
    for tooth in range(13):
        a=start+tooth*40
        d.polygon([(a,y+height),(a+20,y+height+14),(a+40,y+height)],fill='#fffdfa')
    txt(x+31,y+30,title,39)
    d.line((x+30,y+97,x+width-30,y+97),fill='#c3b6a6',width=3)
    txt(x+31,y+140,'세전 이자',29)
    txt(x+width-34,y+135,'150만 원',35,ink,'rt')
    txt(x+31,y+217,'지급 시 세액',29)
    txt(x+width-34,y+212,tax,35,ink,'rt')
    rounded((x+28,y+298,x+width-28,y+424),'#fff0aa')
    txt(x+49,y+318,'손에 들어오는 이자',28)
    txt(x+width-45,y+364,net,42,red,'rt')

receipt(375,'일반과세','23만 1천 원','126만 9천 원')
receipt(939,'비과세 적용','0원','150만 원')
rounded((55,833,1865,949),'#fffdf7','#c4af94')
txt(81,855,'65세 이상 거주자 경로는',30)
rounded((529,846,1015,889),'#fff0aa')
txt(545,854,'기초연금 수급도 확인',30,red)
txt(81,902,'일반과세 금리가 연 3.60%라면 세후 152만 2,800원으로 순서가 바뀌어요.',31)
txt(55,1003,'출처  국가법령정보센터 · 조세특례제한법  /  국세청 · 원천징수 세율 및 지방소득세 특별징수',24)
out=root/'영상/EP149/이자_영수증.png'
im.save(out)
im.resize((960,540),Image.Resampling.LANCZOS).save(Path(__file__).with_name('축소검수.png'))
