# -*- coding: utf-8 -*-
"""去重分析：完全重复 + 高相似题对检测"""
import json, re, difflib, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open('src/assets/data/all_questions.json', encoding='utf-8') as f:
    data = json.load(f)
print('总数:', len(data))

def norm(t):
    return re.sub(r'[\s，。、,.!！?？「」『』（）()【】\[\]""\u2018\u2019·…\-—~～的了是很]', '', t)

# 1) 完全重复（归一化题干相同）
exact = defaultdict(list)
for i, q in enumerate(data):
    exact[norm(q['question'])].append(i)
dup_exact = {k: v for k, v in exact.items() if len(v) > 1}
print('\n=== 归一化后题干完全相同的组 ===')
for k, idxs in dup_exact.items():
    print(f'{len(idxs)}题: {[data[i]["id"] for i in idxs]}')
    for i in idxs:
        print(f'   {data[i]["id"]}: {data[i]["question"][:60]}')

# 2) 高相似题干
texts = [(i, norm(q['question'])) for i, q in enumerate(data) if not q.get('image_url')]
pairs = []
n = len(texts)
for a in range(n):
    ia, ta = texts[a]
    for b in range(a + 1, n):
        ib, tb = texts[b]
        if abs(len(ta) - len(tb)) > max(len(ta), len(tb)) * 0.25:
            continue
        r = difflib.SequenceMatcher(None, ta, tb).ratio()
        if r >= 0.82:
            pairs.append((r, ia, ib))
pairs.sort(reverse=True)
print(f'\n=== 相似度>=0.82 的题对（去重后 {len(set((ia, ib) for _, ia, ib in pairs))} 组）===')
seen = set()
count = 0
for r, ia, ib in pairs:
    key = tuple(sorted([ia, ib]))
    if key in seen:
        continue
    seen.add(key)
    count += 1
    same_ans = data[ia]['answer'] == data[ib]['answer']
    print(f'[{r:.2f}] ans{"同" if same_ans else "异"} | {data[ia]["id"]} vs {data[ib]["id"]}')
    print(f'   A: {data[ia]["question"][:58]}')
    print(f'   B: {data[ib]["question"][:58]}')
print(f'\n共 {count} 组高相似')
