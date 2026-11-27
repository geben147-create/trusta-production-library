import hashlib
import json
from pathlib import Path

studio = Path(__file__).resolve().parent
root = studio.parents[1]
base_script = studio / '낭독준비.py'
code = base_script.read_text().split('audio = root', 1)[0]
namespace = {'__file__': str(base_script)}
exec(compile(code, str(base_script), 'exec'), namespace)

old_path = root / '낭독본문/EP157_Qwen_v2.jsonl'
new_path = root / '낭독본문/EP157_Qwen_v2_보강.jsonl'
old = [json.loads(line) for line in old_path.read_text().splitlines()]
unused = {}
for line in reversed(old):
    unused.setdefault(line['text'], []).append(line['line_id'])
rows = namespace['rows']
fresh = 0
for row in rows:
    matching = unused.get(row['text'])
    if matching:
        row['line_id'] = matching.pop()
    else:
        fresh += 1
        row['line_id'] = f'B{fresh:04d}'
assert not any(unused.values()), '기존 낭독 중 보강판에서 누락된 행이 있습니다.'
assert len({row['line_id'] for row in rows}) == len(rows)
new_path.write_text(''.join(json.dumps({k: row[k] for k in ('line_id', 'text')}, ensure_ascii=False) + '\n' for row in rows))
(studio / '보강장면과낭독행.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

record = {
    '상태': '보강 낭독 준비, 실제 재생시간 미확인',
    '초판낭독해시': digest(old_path),
    '보강낭독해시': digest(new_path),
    '원고해시': digest(root / 'EP157.md'),
    '기존행': len(old),
    '신규행': fresh,
    '전체글자': sum(len(r['text']) for r in rows),
    '신규글자': sum(len(r['text']) for r in rows if r['line_id'].startswith('B')),
}
(studio / '보강낭독준비.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(record['기존행'], record['신규행'], record['신규글자'])
