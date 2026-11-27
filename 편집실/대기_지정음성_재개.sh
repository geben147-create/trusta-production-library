#!/usr/bin/env bash
set -uo pipefail
cd -- "$(dirname -- "$0")/.."
result=0
for id in FAQ01 FAQ03 EP129; do
    (
        exec 9>"편집실/${id}_영상조판/${id}.lock"
        flock -n 9 || exit 0
        python3 - "$id" <<'PY' || exit 1
import hashlib
import json
from pathlib import Path
import sys

episode = sys.argv[1]
manifest = json.loads(Path(f"편집실/{episode}_낭독준비.json").read_text())
for file, key in ((f"{episode}.md", "원고해시"), (f"낭독본문/{episode}_Qwen_v2.jsonl", "낭독해시")):
    actual = hashlib.sha256(Path(file).read_bytes()).hexdigest()
    if actual != manifest[key]:
        raise SystemExit(f"현재 판본의 해시를 확인하세요: {file}")
PY
        exec 8>편집실/.천억뷰_음성.lock
        flock 8 || exit 1
        output="음성/${id}_Qwen_v2"
        if [[ ! -s "$output/full.wav" || ! -s "$output/report.csv" ]]; then
            mkdir -p "$output"
            VOICE=voiceB LANG_TTS=Korean bash /home/yh/ai-work/tts_cosy_prod/qwen_natural.sh "낭독본문/${id}_Qwen_v2.jsonl" "$output" -12 || exit 1
        fi
        ffprobe -v error -show_entries format=duration -of csv=p=0 "$output/full.wav" || exit 1
    ) || result=1
done
exit "$result"
