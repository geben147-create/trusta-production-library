"""Reconstruct Berkshire's reported observation-period returns and milestones."""
import hashlib
import json
import re
import subprocess
from decimal import Decimal
from pathlib import Path

folder = Path(__file__).resolve().parent
pdf = folder / 'Berkshire_2024_Annual_Report.pdf'
text = subprocess.check_output(
    ['pdftotext', '-f', '17', '-l', '21', '-layout', str(pdf), '-'],
    text=True,
)
pattern = r'^((?:19|20)\d{2})(?:\s+\.)+\s+([()0-9.]+)%?\s+([()0-9.]+)%?\s*$'
series = {}
for year, first, second in re.findall(pattern, text, re.M):
    year = int(year)
    if year in series:
        raise ValueError(f'중복 관측 행: {year}')
    series[year] = [Decimal(s.replace('(', '-').replace(')', '')) for s in (first, second)]
if sorted(series) != list(range(1965, 2025)):
    raise ValueError('1965~2024 관측 행이 완전하지 않습니다.')


def ledger(start, column):
    value = maximum = Decimal(1)
    milestones, history = {}, {}
    drawdown, low = Decimal(0), None
    for year in range(start, 2025):
        value *= 1 + series[year][column]/100
        maximum = max(maximum, value)
        if value/maximum-1 < drawdown:
            drawdown, low = value/maximum-1, year
        for goal in (2, 3, 100):
            if value >= goal:
                milestones.setdefault(goal, year)
        history[year] = str(value)
    return {'최종': str(value), '첫도달': milestones, '최대관측낙폭': str(drawdown),
            '낙폭연도': low, '연도별배수': history}


audit = {str(y): {n: ledger(y, i) for i, n in enumerate(('Berkshire', 'SP500'))}
         for y in (1965, 1985, 2000)}
assert [audit['1965'][n]['첫도달'][100] for n in ('Berkshire', 'SP500')] == [1983, 2014]
assert audit['1965']['Berkshire']['낙폭연도'] == 1974
assert round(Decimal(audit['1965']['Berkshire']['최대관측낙폭']) * 100, 2) == Decimal('-49.98')
assert all(100 not in audit['2000'][n]['첫도달'] for n in ('Berkshire', 'SP500'))
audit['재현정보'] = {
    '원문': 'https://www.berkshirehathaway.com/2024ar/2024ar.pdf',
    'PDF_SHA256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
    '자료조건': '1965·1966년 9월 결산, 1967년 15개월, 이후 달력연도. 일별 관측 미적용.',
}
target = folder / '복리_검산.json'
temp = target.with_suffix('.tmp')
temp.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
temp.replace(target)
print('60개 공시 관측 구간, 3개 출발점 검산 완료')
