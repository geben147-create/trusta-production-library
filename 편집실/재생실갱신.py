"""현재 완성된 로컬 Qwen 음성을 읽어 재생 페이지를 갱신한다."""
from csv import DictReader
from html import escape
import json
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from urllib.parse import quote
import wave

ROOT = Path(__file__).resolve().parents[1]
EDITOR = ROOT / '편집실'

def clock(seconds):
    minutes, remainder = divmod(round(seconds), 60)
    return f'{minutes}분 {remainder:02d}초'

def audio_tag(path, rate):
    href = quote(path.relative_to(ROOT).as_posix())
    return f'<audio controls preload="none" data-rate="{rate}" src="{href}"></audio>'

def audio_rows():
    candidates = {}
    for folder in (ROOT / '음성').glob('*_Qwen_v2*'):
        match = re.fullmatch(r'((?:EP|FAQ)\d+)_Qwen_v2(_보강)?', folder.name)
        if not match:
            continue
        ident, supplement = match.groups()
        full = folder / 'full.wav'
        report = folder / 'report.csv'
        if not full.is_file() or not report.is_file():
            continue
        narration = ROOT / '낭독본문' / f'{folder.name}.jsonl'
        if not narration.exists():
            narration = ROOT / '낭독본문' / f'{ident}_Qwen_v2.jsonl'
        try:
            with report.open() as stream:
                lines = list(DictReader(stream))
            with narration.open() as stream:
                ids = [json.loads(line)['line_id'] for line in stream if line.strip()]
            if not ids or ids != [row['line_id'] for row in lines]:
                continue
            with wave.open(str(full)) as original:
                seconds = original.getnframes() / original.getframerate() / 1.2
            speech = sum(float(row['seconds']) for row in lines) / 1.2
            markdown = (ROOT / f'{ident}.md').read_text().splitlines()
            title = markdown[0].removeprefix('# ')
        except (OSError, ValueError, KeyError, EOFError, wave.Error):
            continue
        row = (bool(supplement), full.stat().st_mtime, title, full, seconds, speech)
        if ident not in candidates or row[:2] > candidates[ident][:2]:
            candidates[ident] = row
    return candidates

def main():
    summary = json.loads((EDITOR / '현황.json').read_text())
    sounds = audio_rows()
    heading = f"""<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>TRUSTA 완성 음성</title>
<style>
body{{margin:2rem auto;max-width:780px;padding:0 1rem;font:17px/1.58 system-ui,sans-serif;color:#172c39;background:#fbf9f3}}
a{{color:#155675}}article{{border-block-start:1px solid #c6d3d8;padding:1rem 0}}audio{{width:min(100%,36rem)}}img{{max-width:100%}}h2{{font-size:1.15rem}}
</style>
<h1>TRUSTA 완성 음성</h1>
<p>고유 본문 <strong>{summary['고유본문']:,}편</strong> / 목표 {summary['고유배정']:,}편 · 지정 Qwen 전체 음성 <strong>{len(sounds)}편</strong></p>
<p>지정 Qwen 1.2배속 낭독만 17분 초과 <strong>{sum(min(row[4:6]) > 1020 for row in sounds.values())}편</strong></p>
<p>1.2배속 17분 검산 통과 <strong>{len(summary['재생시간통과'])}편</strong> (다른 검산 음성 포함) · 이미지 연결 {summary['이미지연결원고수']}편</p>
<p><a href="원고_미리보기.html">전체 원고</a> · <a href="#retirement">은퇴 생활비</a> · <a href="#audio">전체 재생 목록</a></p>
<section id="retirement">
<h2>은퇴 후 한 달에 얼마가 부족할까?</h2>
<p><a href="원고_미리보기.html#EP034">연금을 뺀 은퇴 생활비</a> · <a href="원고_미리보기.html#EP157">퇴직금 1억에서 생활비를 꺼낸다면</a> · <a href="원고_미리보기.html#EP141">집을 유지하며 받는 주택연금</a> · <a href="원고_미리보기.html#EP149">비과세 예금 이자</a></p>
<img loading="lazy" src="시각자료/EP034_은퇴부족액_3D.png" alt="월 생활비와 연금 입금액의 차이를 보여 주는 차트">
</section>
<section id="audio"><h2>지정 Qwen 음성 재생</h2>
"""
    sections = [heading]
    teaser = ROOT / '음성/미리듣기/EP117_1.2x.mp3'
    if teaser.is_file():
        sections.append(f'<p>ISA 만기자금 편 · 1.2배속 30초 미리듣기</p>{audio_tag(teaser, 1)}')
    for ident, row in sorted(sounds.items(), key=lambda item: item[1][1], reverse=True):
        supplement, _, title, full, seconds, speech = row
        record = json.loads((EDITOR / '원고기록' / f'{ident}.json').read_text())
        video = record.get('영상')
        if not isinstance(video, str) or not (ROOT / video).is_file():
            video = ''
        links = f'<a href="원고_미리보기.html#{ident}">원고 보기</a>'
        if video:
            links += f' · <a href="{quote(video)}">가로 영상 보기</a>'
        sections.append(f'<article id="{ident}"><h2>{escape(title)}</h2><p>{"보강판 · " if supplement else ""}1.2배속 전체 {clock(seconds)} · 행간 제외 {clock(speech)}</p>{audio_tag(full, 1.2)}<p>{links}</p></article>')
    sections.append("""</section><script>
const players = Array.from(document.querySelectorAll('audio'));
for (const player of players) {
  player.defaultPlaybackRate = Number(player.dataset.rate);
  player.playbackRate = player.defaultPlaybackRate;
  player.addEventListener('play', () => players.forEach(other => {if (other !== player) other.pause();}));
}
</script></html>""")
    target = ROOT / '완성음성_재생실.html'
    with NamedTemporaryFile(mode='w', encoding='utf-8', dir=ROOT, delete=False) as output:
        output.write('\n'.join(sections))
    os.replace(output.name, target)
    print(f'재생실 지정 Qwen {len(sounds)}편')

if __name__ == '__main__':
    main()
