"""Generate chapter timings and SRT from the finished Qwen line WAVs."""
import argparse
import csv
import json
import hashlib
import subprocess
import sys
import random
import wave
from pathlib import Path


def wav_info(path):
    with wave.open(str(path)) as wav:
        return wav.getnframes(), wav.getframerate()


def timestamp(seconds):
    n = round(seconds * 1000)
    return f"{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}"


def subtitle_blocks(text, width=32):
    lines = []
    current = ""
    for word in text.split():
        combined = (current + " " + word).strip()
        if current and len(combined) > width:
            lines.append(current)
            current = word
        else:
            current = combined
    if current:
        lines.append(current)
    return ["\n".join(lines[i:i+2]) for i in range(0, len(lines), 2)]


def build(rows, reports, audio):
    if len(rows) != len(reports):
        raise ValueError("낭독 행과 음성 보고서의 행 수가 다릅니다.")
    frames, rate = wav_info(audio / "full.wav")
    cursor = 0
    voice_frames = 0
    chapters = {}
    entries = []
    rng = random.Random(7)
    for row, report in zip(rows, reports):
        name = row["line_id"]
        count, line_rate = wav_info(audio / (name + ".wav"))
        if report["line_id"] != name or line_rate != rate or abs(float(report["seconds"]) - count / rate) >= .006:
            raise ValueError(f"{name} 음성 보고서가 일치하지 않습니다.")
        chapters.setdefault(row["stage"], cursor)
        gap = rng.uniform(.35, .65)
        if row["text"].rstrip().endswith(("?", "？")):
            gap = .7
        if abs(float(report["gap_after"]) - gap) >= .006:
            raise ValueError(f"{name}의 줄 간격을 확인해야 합니다.")
        blocks = subtitle_blocks(row["text"])
        weights = [len(block.replace("\n", "")) for block in blocks]
        denominator = sum(weights)
        elapsed = 0
        for block, weight in zip(blocks, weights):
            start = (cursor + count * elapsed / denominator) / rate
            elapsed += weight
            end = (cursor + count * elapsed / denominator) / rate
            entries.append(f"{len(entries)+1}\n{timestamp(start)} --> {timestamp(end)}\n{block}")
        voice_frames += count
        cursor += count + int(gap * rate)
    if cursor != frames:
        raise ValueError("개별 음성과 전체 음성의 표본 수가 일치하지 않습니다.")
    timings = [
        {"장": stage, "기본시작초": start / rate, "기본끝초": end / rate}
        for (stage, start), end in zip(chapters.items(), [*list(chapters.values())[1:], frames])
    ]
    return "\n\n".join(entries) + "\n", timings, voice_frames / rate / 1.2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("episode", choices=["EP051", "EP053", "EP117", "EP157", "EP163"])
    parser.add_argument("--audio-dir", type=Path)
    options = parser.parse_args()
    ep = options.episode
    root = Path(__file__).resolve().parents[1]
    studio = root / "편집실" / (ep + "_영상조판")
    audio = options.audio_dir or root / "음성" / (ep + "_Qwen_v2")
    supplemented = ep in {"EP157", "EP163"} and audio.name == ep + "_Qwen_v2_보강"
    scene_file = "보강장면과낭독행.json" if supplemented else "장면과낭독행.json"
    rows = json.loads((studio / scene_file).read_text())
    with (audio / "report.csv").open() as f:
        reports = list(csv.DictReader(f))
    srt, timing, voice_seconds = build(rows, reports, audio)
    frames, sample_rate = wav_info(audio / "full.wav")
    playback_seconds = frames / sample_rate / 1.2
    seconds = playback_seconds if ep == "EP117" else voice_seconds
    video = root / "영상" / ep
    video.mkdir(parents=True, exist_ok=True)
    (video / "한국어자막.srt").write_text(srt)
    (studio / "장면시간.json").write_text(json.dumps(
        {"장면": timing, "행간제외_1.2배속초": voice_seconds, "전체_1.2배속초": playback_seconds, "판정": "PASS" if seconds > 1020 else "미달"},
        ensure_ascii=False, indent=2,
    ) + "\n")

    def digest(path):
        with path.open("rb") as f:
            return hashlib.file_digest(f, "sha256").hexdigest()

    narration_markdown = root / "낭독본문" / (ep + ".md")
    if ep in {"EP157", "EP163"}:
        narration_markdown = root / (ep + ".md")
    verification = {
        "sha256": digest(narration_markdown),
        "JSONLsha256": digest(root / "낭독본문" / (ep + ("_Qwen_v2_보강.jsonl" if supplemented else "_Qwen_v2.jsonl"))),
        "전체WAVsha256": digest(audio / "full.wav"),
        "한국어음성": "Qwen3-TTS-Base 자연스러운 v2 / voiceB",
        "재생초": seconds,
        "행간제외_1.2배속초": voice_seconds,
        "전체_1.2배속초": playback_seconds,
        "판정": "PASS" if seconds > 1020 else "미달",
    }
    final = root / "편집실" / (ep + "_낭독검산.json")
    tmp = final.with_suffix(".tmp")
    tmp.write_text(json.dumps(verification, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(final)
    subprocess.run([sys.executable, str(root / "편집실/목차갱신.py")], check=True)


if __name__ == "__main__":
    main()
