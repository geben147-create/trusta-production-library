#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
exec 9>편집실/EP051_영상조판/EP051.lock
flock -n 9 || exit 0
exec 8>편집실/.천억뷰_음성.lock
flock 8
input=낭독본문/EP051_Qwen_v2.jsonl
out=음성/EP051_Qwen_v2
mkdir -p "$out"
VOICE=voiceB LANG_TTS=Korean bash /home/yh/ai-work/tts_cosy_prod/qwen_natural.sh "$input" "$out" -12
python3 - <<'PY'
import json,wave,hashlib
from pathlib import Path
p=Path('음성/EP051_Qwen_v2/full.wav')
with wave.open(str(p)) as w:sec=w.getnframes()/w.getframerate()
d={'음성':'Qwen3-TTS-Base 자연스러운 v2 voiceB','기본초':sec,'1.2배속초':sec/1.2,'판정':'PASS' if sec/1.2>1020 else '미달','입력해시':hashlib.sha256(Path('낭독본문/EP051_Qwen_v2.jsonl').read_bytes()).hexdigest()}
Path('편집실/EP051_영상조판/음성실측.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
PY
