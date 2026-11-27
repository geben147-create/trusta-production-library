#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
base=편집실/EP159_영상조판
input=낭독본문/EP159_Qwen_v2.jsonl
output=음성/EP159_Qwen_v2
exec 9>"$base/EP159.lock"
flock -n 9 || exit 0
python3 - <<'PY'
import hashlib, json
from pathlib import Path
m=json.loads(Path('편집실/EP159_낭독준비.json').read_text())
for path,key in [('EP159.md','원고해시'),('낭독본문/EP159_Qwen_v2.jsonl','낭독해시')]:
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==m[key],path
PY
exec 8>편집실/.천억뷰_음성.lock
flock 8
if [[ ! -s "$output/full.wav" || ! -s "$output/report.csv" ]]; then
    mkdir -p "$output"
    VOICE=voiceB LANG_TTS=Korean bash /home/yh/ai-work/tts_cosy_prod/qwen_natural.sh "$input" "$output" -12
fi
ffprobe -v error -show_entries format=duration -of csv=p=0 "$output/full.wav"
