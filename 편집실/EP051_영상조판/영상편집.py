"""Compose the EP051 widescreen cut list from the verified narration WAVs."""
from __future__ import annotations

import csv
import fcntl
import json
import random
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

STUDIO = Path(__file__).resolve().parent
ROOT = STUDIO.parents[1]
OUTPUT = ROOT / "영상/EP051"
AUDIO = ROOT / "음성/EP051_Qwen_v2"
FONT = Path("/home/yh/.local/share/fonts/JalnanGothic/JalnanGothic.ttf")
SIZE = (1920, 1080)


def wav_frames(path: Path) -> tuple[int, int]:
    with wave.open(str(path)) as source:
        return source.getnframes(), source.getframerate()


def shot_images(cuts: list[dict], directory: Path) -> list[Path]:
    mascot_source = ROOT / "집필인계/천억이_시그니처표정.png"
    with Image.open(mascot_source) as mascot_image:
        mascot = mascot_image.crop((31, 2, 242, 254))
        mascot.thumbnail((176, 185))

    font = ImageFont.truetype(str(FONT), 42)
    shots = []
    for number, cut in enumerate(cuts):
        source = ROOT / cut["자산"]
        with Image.open(source) as picture:
            if picture.size == SIZE:
                canvas = picture.convert("RGB")
            else:
                canvas = Image.new("RGB", SIZE, "#f6ecdb")
                draw = ImageDraw.Draw(canvas)
                draw.rectangle((0, 0, 1920, 120), fill="#263e49")
                draw.text((66, 32), cut["문구"], font=font, fill="#fff5d8")
                body = ImageOps.contain(picture.convert("RGB"), (1320, 860), Image.Resampling.LANCZOS)
                canvas.paste(body, (720 - body.width // 2, 145 + (860 - body.height) // 2))
                canvas.paste(mascot, (1620, 730))
        if cut["행"] in (107, 117):
            canvas = Image.new("RGB", SIZE, "#eadec9")
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle((90, 125, 1827, 973), radius=27, fill="#f7eedf")
            draw.text((132, 164), cut["문구"], font=font, fill="#243c43")
            values = {
                107: ("가상 달러 평가액 100달러 → 98달러", "최초 원화 120,000원",
                      "마지막 환율 1,300원 → 127,400원", "마지막 환율 1,100원 → 107,800원"),
                117: ("첫날 마감 잔고 120만 원", "그대로 두면 둘째 날 약 981,818원",
                      "40만 원 추가 납입 → 약 1,309,091원", "총 납입 140만 원 → 약 90,909원 부족"),
            }
            small_font = ImageFont.truetype(str(FONT), 35)
            for index, line in enumerate(values[cut["행"]]):
                y = 274 + index * 127
                draw.rounded_rectangle((129, y, 1475, y + 94), radius=16,
                                       fill="#fff0a4" if index == 3 else "#fffbf1")
                draw.text((162, y + 23), line, font=small_font,
                          fill="#982b23" if index == 3 else "#263d43")
            canvas.paste(mascot, (1559, 596))
        target = directory / f"shot_{number:02d}.png"
        canvas.save(target)
        shots.append(target)
    return shots


def timeline(rows: list[dict], reports: list[dict]) -> tuple[list[float], float]:
    total, sample_rate = wav_frames(AUDIO / "full.wav")
    starts = []
    cursor = 0
    rng = random.Random(7)
    for row, report in zip(rows, reports, strict=True):
        name = row["line_id"]
        frames, rate = wav_frames(AUDIO / (name + ".wav"))
        if report["line_id"] != name or rate != sample_rate:
            raise ValueError(f"{name} does not match the synthesis report")
        gap = rng.uniform(.35, .65)
        if row["text"].rstrip().endswith(("?", "？")):
            gap = .7
        if abs(float(report["seconds"]) - frames / rate) >= .006 or abs(float(report["gap_after"]) - gap) >= .006:
            raise ValueError(f"{name} duration does not match the synthesis report")
        starts.append(cursor / sample_rate)
        cursor += frames + int(gap * sample_rate)
    if cursor != total:
        raise ValueError("Full WAV frame count does not match the line WAVs")
    return starts, total / sample_rate


def main() -> None:
    build = STUDIO / "가로영상편집"
    build.mkdir(exist_ok=True)
    with (build / "render.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        cuts = json.loads((STUDIO / "화면배치.json").read_text())
        shots = shot_images(cuts, build)
        if "--frames-only" in sys.argv:
            return

        rows = json.loads((STUDIO / "장면과낭독행.json").read_text())
        with (AUDIO / "report.csv").open() as report:
            starts, total = timeline(rows, list(csv.DictReader(report)))
        start_times = [starts[cut["행"] - 1] for cut in cuts]
        ends = start_times[1:] + [total]
        concat = "\n".join(
            f"file '{shot.name}'\nduration {end - start:.9f}"
            for shot, start, end in zip(shots, start_times, ends, strict=True)
        )
        concat += f"\nfile '{shots[-1].name}'\n"
        (build / "cuts.ffconcat").write_text(concat)
        subtitle = OUTPUT / "한국어자막.srt"
        target = OUTPUT / "두자전거_일일복리.mp4"
        temporary = build / "render.partial.mp4"
        subprocess.run(
            [
                "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "concat", "-safe", "0", "-i", "cuts.ffconcat",
                "-i", str(AUDIO / "full.wav"), "-i", str(subtitle),
                "-map", "0:v", "-map", "1:a", "-map", "2:s", "-t", f"{total:.9f}",
                "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
                "-threads", "4", "-crf", "21", "-c:a", "aac", "-b:a", "128k",
                "-c:s", "mov_text", "-metadata:s:s:0", "language=kor", "-movflags", "+faststart",
                str(temporary),
            ],
            cwd=build,
            check=True,
        )
        temporary.replace(target)
        results = [
            {**cut, "시작초": round(start, 3), "종료초": round(end, 3)}
            for cut, start, end in zip(cuts, start_times, ends, strict=True)
        ]
        (build / "실제화면시간.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
