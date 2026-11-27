from csv import DictReader
from decimal import Decimal as D
from pathlib import Path
import re
from subprocess import check_output

root = Path(__file__).resolve().parent

def observations(series):
    with (root / f"{series}.csv").open() as stream:
        return {row["observation_date"]: D(row[series]) for row in DictReader(stream) if row[series]}

def nav_returns(ticker):
    text = check_output(["pdftotext", "-layout", str(root / f"{ticker}.pdf"), "-"], text=True)
    dates = re.search(r"2021\s+2022\s+2023\s+2024\s+2025", text)
    numbers = r"\s+".join([r"(-?\d+\.\d{2})"] * 5)
    match = re.search(r"(?m)^\s*NAV\s+" + numbers, text[dates.end():])
    return dict(zip(range(2021, 2026), map(D, match.groups()), strict=True))

def balances(returns, start):
    balance = peak = D(10000)
    drawdown = D(0)
    for year, rate in returns.items():
        if year >= start:
            balance *= 1 + rate / 100
            peak = max(peak, balance)
            drawdown = min(drawdown, balance / peak - 1)
    return balance, drawdown * 100

rates = observations("DGS30")
fx = observations("DEXKOUS")
print("30-year yields", rates["2021-12-31"], rates["2022-12-30"])
start_fx = fx["2021-12-30"]
end_fx = fx["2022-12-30"]
for ticker in ("IAU", "TLT"):
    returns = nav_returns(ticker)
    for start in (2021, 2023):
        print(ticker, start, *(round(value, 2) for value in balances(returns, start)))
    final_usd = 10000 * (1 + returns[2022] / 100)
    print(ticker, final_usd, final_usd * end_fx, round((final_usd * end_fx / (10000 * start_fx) - 1) * 100, 2))
