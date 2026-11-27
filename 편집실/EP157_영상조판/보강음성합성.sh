#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
studio=편집실/EP157_영상조판
input=낭독본문/EP157_Qwen_v2_보강.jsonl
out=음성/EP157_Qwen_v2_보강
exec 9>"$studio/EP157.lock"
flock -n 9 || exit 0
python3 - <<'PY'
import os,json,hashlib
from pathlib import Path
old=Path('낭독본문/EP157_Qwen_v2.jsonl')
new=Path('낭독본문/EP157_Qwen_v2_보강.jsonl')
m=Path('편집실/EP157_영상조판/보강낭독준비.json')
j=json.loads(m.read_text())
assert all(hashlib.sha256(x.read_bytes()).hexdigest()==j[key] for x,key in [(old,'초판낭독해시'),(new,'보강낭독해시'),(Path('EP157.md'),'원고해시')])
a={r['line_id']:r['text'] for r in map(json.loads,old.read_text().splitlines())}
b=list(map(json.loads,new.read_text().splitlines()))
assert len(b)==len({r['line_id'] for r in b})
assert {r['line_id']:r['text'] for r in b if r['line_id'] in a}==a
out=Path('음성/EP157_Qwen_v2_보강/raw')
out.mkdir(parents=True,exist_ok=True)
for ident in a:
    source=Path('음성/EP157_Qwen_v2/raw')/f'{ident}.wav'
    target=out/source.name
    if not target.exists():
        os.link(source,target)
    assert os.path.samefile(source,target)
j['상태']='지정 음성 보강 대기열'
m.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
PY
exec 8>편집실/.천억뷰_음성.lock
flock 8
if [[ ! -s "$out/full.wav" || ! -s "$out/report.csv" ]]; then
    VOICE=voiceB LANG_TTS=Korean bash /home/yh/ai-work/tts_cosy_prod/qwen_natural.sh "$input" "$out" -12 > "$studio/보강음성합성.log" 2>&1
fi
flock -u 8
