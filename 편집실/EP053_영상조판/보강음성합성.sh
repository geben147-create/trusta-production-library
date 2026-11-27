#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
studio=편집실/EP053_영상조판
input=낭독본문/EP053_Qwen_v2.jsonl
out=음성/EP053_Qwen_v2_보강
exec 9>"$studio/EP053.lock"
flock -n 9 || exit 0
exec 8>편집실/.천억뷰_음성.lock
flock 8
if [[ ! -s "$out/full.wav" || ! -s "$out/report.csv" ]]; then
    VOICE=voiceB LANG_TTS=Korean bash /home/yh/ai-work/tts_cosy_prod/qwen_natural.sh "$input" "$out" -12
fi
flock -u 8
python3 "$studio/영상편집.py" --audio-dir "$out" --output-name 반토막_회복_보강.mp4
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height:format=duration -of json 영상/EP053/반토막_회복_보강.mp4 > "$studio/가로영상편집/보강_출력검증.json"
