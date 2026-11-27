import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
episode = 'EP151'
source = root / f'{episode}.md'
draft = source.read_text()
spoken_tables = {
    '2015년의 원금 대비': (
        '세 가상 계좌를 달러로 읽어 봅니다. 엔비디아는 이만 칠천육백육십일 달러 팔 센트. '
        '에스앤피 오백 총수익 비교값은 삼백이십삼 달러 팔십팔 센트입니다. '
        '나스닥 백 총수익 비교값은 오백삼십칠 달러 칠십팔 센트예요. '
        '모두 같은 날의 백 달러를 출발값으로 썼습니다.'
    ),
    '천억이는 첫 번째 달력의': (
        '엔비디아는 이천십칠년 관측점에서 두 배와 세 배를 모두 넘어 오 점 사 배를 보였습니다. '
        '에스앤피 오백은 이천이십이년에 두 배와 이천이십오년에 세 배를 넘긴 표본이 처음 보입니다. '
        '나스닥 백은 이천이십년에 두 배를 넘고 이천이십일년에 세 배를 넘긴 표본이 처음 보입니다. '
        '셋 중 백 배 이상이 관측된 것은 엔비디아이며, 이천이십사년 표본에서는 백십팔 점 삼사 배입니다. '
        '여기서 말하는 해는 각 문턱을 넘은 실제 거래일이 아니라, 한 해에 한 번 찍은 관측 시점이에요.'
    ),
}
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
    if paragraph.startswith('## '):
        sections.append((re.sub(r'^## (?:\d+\. )?', '', paragraph), []))
        continue
    if not sections or not paragraph or paragraph.startswith(('#', '|', '!', '*SEC')):
        continue
    text = re.sub(r'\s*\[[^]]+\]\(https?://[^)]+\)(?:\s*·)?', '', paragraph)
    for prefix, narration in spoken_tables.items():
        if text.startswith(prefix):
            sections[-1][1].append(narration)
    text = text.replace('**', '').replace('`', '')
    for label, spoken in [('S&P 500','에스앤피 오백'),('나스닥 100','나스닥 백'),('SEC','에스이씨'),
                          ('Stock Performance Graphs','주주 총수익 비교'),('%','퍼센트'),('~','부터 ')]:
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
