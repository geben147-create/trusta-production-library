#!/usr/bin/env bash
set -euo pipefail
here="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$here/../.."
exec 9>"$here/EP041.lock"
flock -n 9 || exit 0
# The preceding episode already holds a private GPU slot. Wait on that actual
# lock; reserve the series slot so simultaneous later pickups cannot duplicate work.
exec 8>"편집실/.천억뷰_음성.lock"
flock 8
flock "편집실/EP001_영상조판/EP001.lock" true
input="낭독본문/EP041_Qwen_v2.jsonl"
output="음성/EP041_Qwen_v2"
mkdir -p "$output"
sha256sum -c "$here/합성입력.sha256"
if ! test -s "$output/full.wav" || ! test -s "$output/report.csv"; then
  python3 "$here/검토화면.py" --합성중
  VOICE=voiceB LANG_TTS=Korean bash /home/yh/ai-work/tts_cosy_prod/qwen_natural.sh "$input" "$output" -12
fi
sha256sum -c "$here/합성입력.sha256"
python3 "$here/영상완성.py"
