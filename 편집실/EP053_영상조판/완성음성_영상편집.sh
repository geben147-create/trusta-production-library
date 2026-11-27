#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
studio=편집실/EP053_영상조판
audio=음성/EP053_Qwen_v2
exec 8>"$studio/영상편집대기.lock"
flock -n 8 || exit 0
exec 9>"$studio/EP053.lock"
flock 9
test -s "$audio/full.wav"
test -s "$audio/report.csv"
test -s "$studio/음성실측.json"
target=영상/EP053/반토막_회복.mp4
if [[ -s "$target" ]]; then
    ffprobe -v error -show_entries format=duration -of csv=p=0 "$target"
    exit 0
fi
python3 "$studio/영상편집.py"
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height:format=duration -of json "$target" > "$studio/가로영상편집/출력검증.json"
