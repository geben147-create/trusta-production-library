"""Match long corporate equities by security identifier in the two public N-PORT filings."""
import hashlib
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parent


def holdings(path):
    doc = ET.parse(path)
    for node in doc.iter():
        node.tag = node.tag.rsplit('}', 1)[-1]
    assert doc.findtext('.//repPdDate') == '2025-12-31'
    asset_sum = defaultdict(Decimal)
    members = defaultdict(list)
    net_assets = Decimal(doc.findtext('.//netAssets'))
    for pos in doc.findall('.//invstOrSec'):
        if (pos.findtext('assetCat'), pos.findtext('issuerCat'), pos.findtext('payoffProfile')) != ('EC', 'CORP', 'Long'):
            continue
        isin = pos.find('identifiers/isin').attrib['value']
        assert len(isin) == 12, pos.findtext('name')
        percent = Decimal(pos.findtext('valUSD'))*100/net_assets
        assert abs(percent - Decimal(pos.findtext('pctVal'))) < Decimal('0.00001')
        asset_sum[isin] += percent
        members[isin].append({'name': pos.findtext('name'), 'cusip': pos.findtext('cusip')})
    return asset_sum, members


weights = {}
issuers = {}
for ticker in ('SOXX', 'SMH'):
    weights[ticker], issuers[ticker] = holdings(root / f'{ticker}.xml')
a,b = weights['SOXX'],weights['SMH']
shared = sorted(a.keys() & b.keys())
union = a.keys() | b.keys()
nvda = next(isin for isin, rows in issuers['SOXX'].items() if any(x['cusip'] == '67066G104' for x in rows))
audit = {
    '관측일': '2025-12-31',
    '비교키': 'ISIN',
    '분모': 'ETF의 N-PORT 순자산 총액. 보통주 계열 EC·CORP·Long만 취합하고 재정규화하지 않음.',
    '종목수': {'SOXX': len(a), 'SMH': len(b), '공통': len(shared), '합집합': len(union)},
    '종목수_합집합기준_겹침_pct': str(Decimal(len(shared))*100/len(union)),
    '작은쪽_합계_pct': str(sum(min(a[isin],b[isin]) for isin in shared)),
    '엔비디아_pct': {n:str(w[nvda]) for n,w in weights.items()},
    '공통종목': {
        isin:{n:{'비중_pct': str(weights[n][isin]), '공시행': issuers[n][isin]} for n in weights}
        for isin in shared
    },
    'XML_SHA256': {n:hashlib.sha256((root/f'{n}.xml').read_bytes()).hexdigest() for n in weights},
}
(root/'중복_검산.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print({k:audit[k] for k in ('종목수','종목수_합집합기준_겹침_pct','작은쪽_합계_pct','엔비디아_pct')})
