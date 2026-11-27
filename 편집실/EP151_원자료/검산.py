from csv import DictReader
from decimal import Decimal as D
from pathlib import Path

with Path(__file__).with_name('SEC_총수익_전사.csv').open() as source:
    observations = list(DictReader(source))
assert observations[5]['date'] == observations[6]['date']
for key in ('NVIDIA', 'SP500', 'Nasdaq100'):
    levels = []
    base = D(observations[5][key]) / 100
    for i, row in enumerate(observations):
        if i != 6:
            levels.append((row['date'], D(row[key]) * (base if i > 6 else 1)))
    print(key)
    for multiple in (2, 3, 100):
        hit = next(((day, round(amount / 100, 2)) for day, amount in levels if amount >= 100 * multiple), ('없음', None))
        print(multiple, hit)
    peak = D(0)
    worst = D(0)
    for day, amount in levels:
        peak = max(peak, amount)
        drop = (amount / peak - 1) * 100
        if drop < worst:
            worst, bottom = drop, day
    print('연간 표본 낙폭', bottom, round(worst,2))
    print('10년 연율', round(((levels[-1][1] / 100) ** (D(1)/10) - 1) * 100, 2))
print('NVDA 회복 필요율', round((D('1174.93')/D('773.30')-1)*100,2))
print('10년 100배에 필요한 가상 연율', round((D(100)**(D(1)/10)-1)*100,2))

for weight, expected in [(D('.05'), D('453.92')), (D('.5'), D('4706.84'))]:
    balance = D(100)
    for previous, current in zip(observations, observations[1:]):
        if previous['date'] == current['date']:
            continue
        stock = D(current['NVIDIA']) / D(previous['NVIDIA'])
        index = D(current['SP500']) / D(previous['SP500'])
        balance *= weight * stock + (1-weight) * index
    assert round(balance, 2) == expected
    print('재조정', weight, round(balance, 2))
