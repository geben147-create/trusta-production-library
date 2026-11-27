#!/usr/bin/env bash
set -euo pipefail
here="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$here/../.."
exec 9>"$here/EP001.lock"
flock -n 9 || exit 0
infile="낭독본문/EP001_Qwen_v2.jsonl"
out="음성/EP001_Qwen_v2"
mkdir -p "$out"
sha256sum "$infile" > "$here/합성입력.sha256"
if ! test -s "$out/full.wav" || ! test -s "$out/report.csv"; then
  VOICE=voiceB LANG_TTS=Korean bash /home/yh/ai-work/tts_cosy_prod/qwen_natural.sh "$infile" "$out" -12
fi
sha256sum -c "$here/합성입력.sha256"
python3 "$here/영상완성.py"
