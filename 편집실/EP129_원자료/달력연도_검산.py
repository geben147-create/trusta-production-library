"""Reproduce hypothetical USD balances from fact-sheet NAV calendar returns."""
from decimal import Decimal
from pathlib import Path
import json
import re
import subprocess

root = Path(__file__).resolve().parent
results = {}
for ticker in ('tip', 'ief', 'stip'):
    text = subprocess.check_output(
        ['pdftotext', '-layout', str(root / f'{ticker}.pdf'), '-'], text=True
    )
    calendar = text.split('CALENDAR YEAR PERFORMANCE (%)', 1)[1]
    years = re.search(r'\b2021\s+2022\s+2023\s+2024\s+2025\b', calendar)
    values = re.search(r'^\s*NAV\s+((?:-?\d+\.\d+\s+){4}-?\d+\.\d+)', calendar, re.M)
    rates = dict(zip(map(int, years[0].split()), map(Decimal, values[1].split()), strict=True))
    outcomes = {}
    for start, end in [(2022, 2022), (2025, 2025), (2021, 2025), (2022, 2025)]:
        balance = Decimal(10000)
        for year in range(start, end + 1):
            balance *= 1 + rates[year] / 100
        outcomes[f'{start}~{end}'] = str(balance)
    results[ticker.upper()] = {'NAV_%': {k: str(v) for k, v in rates.items()}, '잔액_USD': outcomes}
(root / '달력연도_검산.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(results, ensure_ascii=False, indent=2))
