"""UTF-8 낭독 전용 Markdown 파일을 eSpeak NG의 한국어 보통 속도로 실제 합성해 측정한다."""
import ctypes as c
import hashlib
import json
import re
import sys
from pathlib import Path

def measure(path):
    data=path.read_bytes()
    text=data.decode("utf-8")
    paras=[p.strip() for p in re.split(r"\n\s*\n",text) if p.strip() and not p.strip().startswith(("#","<!--","|","!["))]
    assert paras and all("http" not in p for p in paras)
    lib=c.CDLL("libespeak-ng.so.1")
    sr=lib.espeak_Initialize(2,60,None,0)
    assert sr>1000 and lib.espeak_SetVoiceByName(b"ko")==0
    samples=0
    @c.CFUNCTYPE(c.c_int,c.c_void_p,c.c_int,c.c_void_p)
    def count(wav,n,events):
        nonlocal samples
        samples+=n
        return 0
    lib.espeak_SetSynthCallback(count)
    assert lib.espeak_SetParameter(1,175,0)==0
    for p in paras:
        buf=p.encode('utf-8')
        assert lib.espeak_Synth(buf,len(buf)+1,0,1,0,1,None,None)==0
        lib.espeak_Synchronize()
    lib.espeak_Terminate()
    secs=samples/sr
    return dict(원고=path.name,sha256=hashlib.sha256(data).hexdigest(),한국어음성='eSpeak NG ko',기본속도=175,샘플레이트=sr,합성표본수=samples,일배속초=round(secs,3),배속=1.2,재생초=round(secs/1.2,3),요건초=1020,판정='PASS' if secs/1.2>=1020 else '미달')
if __name__=='__main__':
    print(json.dumps(measure(Path(sys.argv[1])),ensure_ascii=False,indent=2))
