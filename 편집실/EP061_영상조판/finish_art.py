from pathlib import Path
import shutil, subprocess, tempfile, os, json, hashlib,tomllib,re
from PIL import Image
t=Path(__file__).resolve().parent;r=Path.cwd();pr=r/'편집실/EP061_영상조판';d=r/'영상/EP061'
def snap(slug,html,dest,local):
 h=t/('final-'+slug+'.html');h.write_text(html);out=t/('public-'+slug+'.png')
 with tempfile.TemporaryDirectory() as profile:
  subprocess.run(['google-chrome','--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--disable-dev-shm-usage','--allow-file-access-from-files','--user-data-dir='+profile,'--window-size=1920,1080','--virtual-time-budget=1200','--screenshot='+str(out),h.as_uri()],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 assert Image.open(out).size==(1920,1080);a=r/'시각자료'/dest;new=a.with_suffix('.new');shutil.copy2(out,new);os.replace(new,a)
 holder=d/(local+'.new');holder.unlink(missing_ok=True);os.link(a,holder);os.replace(holder,d/(local+'.png'));shutil.copy2(h,pr/h.name);shutil.copy2(out,pr/out.name)
snap('main',(t/'hero.html').read_text(),'EP061_월간순매수_생활그래프.png','천억이_순매수_생활그래프')
for slug,file,local,word1,word2,img1,img2 in [('ksd','EP061_세이브로_조회화면.png','세이브로_조회조건','달력을 얼마나 접을까?','빨간 곳부터 고르자!','story-glass-3.jpg','tutor.jpg'),('issuer','EP061_운용사_투자목표.png','운용사_하루목표','한 장에 이름이 둘이네.','하루 목표, 여기!','comic-0.jpg','tutor.jpg')]:
 s=(t/('public-'+slug+'.html')).read_text()
 css="""<style>.docbody{grid-template-columns:490px 1fr;gap:9px;border-radius:7px;padding:10px;background:#f8f0df}.docbody aside{display:grid;grid-template-rows:.78fr 1.22fr;gap:7px;border:0;border-radius:0}.docbody aside section{position:relative;min-height:0;overflow:hidden;border:3px solid #382f28;border-radius:6px}.docbody aside img{object-position:center 37%}.docbody aside b{font-size:29px;border-radius:16px 20px 11px 3px;left:8px;bottom:7px;right:auto}.docbody .paper{background:linear-gradient(120deg,#f5f1e7,#fff 25%,#fff 83%,#efeae4);border-radius:4px;box-shadow:2px 5px 5px #917e5b41}.docline .tip{background:#464039}.docline{font-size:33px}</style>"""
 if slug=='issuer':css+='<style>.docbody{grid-template-columns:1fr 525px}.docbody aside{order:2;grid-template-rows:1.04fr .96fr}.docbody aside img{object-position:center 40%}</style>'
 s=s.replace('</style>', '</style>'+css,1);s=re.sub(r'<aside>.*?</aside>','<aside><section><img src="'+img1+'"><b>'+word1+'</b></section><section><img src="'+img2+'"><b>'+word2+'</b></section></aside>',s)
 vb=re.search(r'<svg viewBox="([0-9 ]+)"',s).group(1).split()
 s=s.replace('<image href=', '<clipPath id="evidence-window"><rect x="'+vb[0]+'" y="'+vb[1]+'" width="'+vb[2]+'" height="'+vb[3]+'"/></clipPath><image clip-path="url(#evidence-window)" href=',1)
 snap(slug,s,file,local)
shutil.copytree(t/'glass',pr/'glass',dirs_exist_ok=True)
for f in [*t.glob('story-glass-*.jpg'),*[t/n for n in ['glass_scene.py','frame.html','shots.py','finish_video.py','gallery.py','hero.html','finish_art.py','qa.py']]]:shutil.copy2(f,pr/f.name)
shutil.copy2(next((Path.home()/'.codex/generated_images/01a21866-0d58-7370-831b-ebe56708540b').glob('exec-bec7a1a4*')),pr/'유리원판_두인물_사건연속컷.png')
mfile=r/'편집실/원고기록/EP061.json';m=json.loads(mfile.read_text());article=r/'EP061.md';s=article.read_text()
for i in m['이미지']:
 if '월간순매수_생활그래프' in i['파일']:
  old=i['대체텍스트'];new='천억이와 수건 친구가 굴러가는 유리 원판을 붙잡고 마지막 닷새로 달력을 접는다. 10월 ETF 상위 열 종목의 달러 순매수 중 SOXL은 주황 유리 67.51%, 나머지 아홉 종목은 투명 유리 32.49%다.';s=s.replace(old,new);i['대체텍스트']=new
m['시각연출']='사건·소품이 이어지는 연재 만화와 실측 통계 기반 Blender Cycles 유리 원판·기둥. 자료에 따라 전체 컷 구성을 바꾸고 공식 원문은 캡처한 화면에만 안내선을 얹었다.'
article.write_text(s);m['원고해시']=hashlib.sha256(article.read_bytes()).hexdigest();mfile.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
