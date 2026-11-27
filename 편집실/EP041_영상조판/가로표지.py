from 페이지 import P,R,page
import subprocess,tempfile
from pathlib import Path
from PIL import Image
def capture(dest,markup):
 with tempfile.TemporaryDirectory(prefix='ep041-img-') as d:
  d=Path(d);p=d/'capture.html';p.write_text(markup)
  snap=d/'shot.png'
  subprocess.run(['google-chrome','--headless','--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files','--user-data-dir='+str(d/'chrome'),'--window-size=1280,720','--force-device-scale-factor=1.5','--virtual-time-budget=1200','--screenshot='+str(snap),p.as_uri()],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  im=Image.open(snap).convert('RGB');assert im.size==(1920,1080);im.save(dest)
if __name__=='__main__':
 D=R/'영상/EP041';capture(D/'열두봉투_장부.png',page(1,4,0,'poster'));capture(D/'QYLD_분배율과성과.png',page(6,3,0,'docposter'))
