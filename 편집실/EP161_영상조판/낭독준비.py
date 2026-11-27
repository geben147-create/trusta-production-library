import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
episode = 'EP161'
source = root / f'{episode}.md'
draft = source.read_text()
digits = '영일이삼사오육칠팔구'

def spoken_number(number):
    groups = []
    for separator in ('', '만', '억', '조'):
        number, group = divmod(number, 10000)
        if group:
            syllables = []
            for index, unit in enumerate(('', '십', '백', '천')):
                group, digit = divmod(group, 10)
                if digit:
                    syllables.append(('' if digit == 1 and unit else digits[digit]) + unit)
            groups.append(''.join(reversed(syllables)) + separator)
        if number == 0:
            return ' '.join(reversed(groups)) or '영'
    raise ValueError('낭독 숫자 범위 초과')

sections = []
for paragraph in draft.splitlines():
    if paragraph == '## 출처':
        break
    if paragraph.startswith('## '):
        sections.append((re.sub(r'^## (?:\d+\. )?', '', paragraph), []))
        continue
    if not sections or not paragraph or paragraph.startswith(('#', '|', '!', '*SEC')):
        continue
    text = re.sub(r'\s*\[[^]]+\]\(https?://[^)]+\)(?:\s*·)?', '', paragraph)
    text = text.replace('**', '').replace('`', '')
    for label, spoken in [('Vanguard','뱅가드'),('−','마이너스 '),('+','플러스 '),('%',' 퍼센트'),('~','부터 ')]:
        text = text.replace(label, spoken)
    def convert(match):
        integer, point, decimal = match[0].replace(',', '').partition('.')
        return spoken_number(int(integer)) + (' 점 ' + ''.join(digits[int(i)] for i in decimal) if point else '')
    text = re.sub(r'\d+(?:,\d{3})*(?:\.\d+)?', convert, text)
    if text.strip():
        sections[-1][1].append(text.strip())

rows = []
chapters = []
for stage, paragraphs in sections:
    chapters.append({'장': stage, '첫행': len(rows) + 1})
    for paragraph in paragraphs:
        current = ''
        for sentence in re.split(r'(?<=[.!?])\s+', paragraph):
            candidate = (current + ' ' + sentence).strip()
            if len(candidate) > 108 and current:
                rows.append({'text': current, 'stage': stage})
                current = sentence
            else:
                current = candidate
        if current:
            rows.append({'text': current, 'stage': stage})

for index, row in enumerate(rows, 1):
    row['line_id'] = f'L{index:04d}'
    assert not re.search(r'https?://|\.png\)|\|', row['text']), row
    assert len(row['text']) <= 160, row

audio = root / '낭독본문' / f'{episode}_Qwen_v2.jsonl'
audio.write_text(''.join(json.dumps({'line_id': row['line_id'], 'text': row['text']}, ensure_ascii=False) + '\n' for row in rows))
Path(__file__).with_name('장면과낭독행.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n')
count = sum(len(row['text']) for row in rows)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
manifest = {'상태':'지정 Qwen 합성 전. 실제 재생시간 미확인.','원고해시':sha(source),'낭독해시':sha(audio),'행수':len(rows),'글자수':count,'구간':chapters}
(root / '편집실' / f'{episode}_낭독준비.json').write_text(json.dumps(manifest, ensure_ascii=False,indent=2)+'\n')
print(f'{len(rows)}행, {count}자')
