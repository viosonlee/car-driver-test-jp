# -*- coding: utf-8 -*-
"""执行去重：删除7组重复中较弱的一方，并将优点融合进保留题"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = 'src/assets/data/all_questions.json'
with open(path, encoding='utf-8') as f:
    data = json.load(f)

by_id = {q['id']: q for q in data}
removed = []

# (保留, 删除, 保留题解析增强文本或None)
merges = [
    ('q_0216', 'q_0636', '左转弯须预先尽量靠向道路左侧、沿路口侧端减速缓行——这样可避免卷入同向直行的两轮车。'),
    ('q_0077', 'q_0427', None),
    ('q_0413', 'q_0601', None),
    ('q_0265', 'q_0639', '铁路道口的本体、侧方及其前后各10米以内的地方，长时停车和临时停车均被禁止。'),
    ('q_0403', 'q_0600', None),
    ('q_0010', 'q_0623', None),
    ('q_0720', 'q_ref_27', None),
]
for keep_id, drop_id, new_expl in merges:
    assert by_id[drop_id]['answer'] == by_id[keep_id]['answer'], f'答案不一致! {keep_id} vs {drop_id}'
    if new_expl:
        by_id[keep_id]['explanation'] = new_expl
    removed.append(drop_id)

data = [q for q in data if q['id'] not in set(removed)]
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已删除 {len(removed)} 道重复题: {removed}')
print(f'剩余 {len(data)} 题')
