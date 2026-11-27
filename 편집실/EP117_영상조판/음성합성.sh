#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
studio=편집실/EP117_영상조판
input=낭독본문/EP117_Qwen_v2.jsonl
out=음성/EP117_Qwen_v2
exec 9>"$studio/EP117.lock"
flock -n 9 || exit 0
exec 8>편집실/.천억뷰_음성.lock
flock 8
if [[ ! -s "$out/full.wav" || ! -s "$out/report.csv" ]]; then
    mkdir -p "$out"
    VOICE=voiceB LANG_TTS=Korean bash /home/yh/ai-work/tts_cosy_prod/qwen_natural.sh "$input" "$out" -12
fi
flock -u 8
python3 편집실/낭독자막.py EP117
