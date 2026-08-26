# -*- coding: utf-8 -*-
"""第二轮去重分析：更激进的相似度检测"""
import json, re, difflib
from collections import defaultdict

qs = json.load(open('src/assets/data/all_questions.json', encoding='utf-8'))

def norm(t):
    t = re.sub(r'[\s，。、；：？！,.;:?!()（）""\'"「」·\-—~～]', '', t or '')
    return t

def strip_nums(t):
    return re.sub(r'[0-9０-９一二两三四五六七八九十百千]+', '#', norm(t))

pairs = []
for i in range(len(qs)):
    for j in range(i+1, len(qs)):
        a, b = qs[i], qs[j]
        s = difflib.SequenceMatcher(None, norm(a['question']), norm(b['question'])).ratio()
        if s >= 0.72:
            same_ans = a['answer'] == b['answer']
            img = bool(a.get('image_url') or b.get('image_url'))
            pairs.append((round(s,3), a['id'], b['id'], 'SAME' if same_ans else 'DIFF', 'IMG' if img else '', a['question'][:38], b['question'][:38]))

pairs.sort(reverse=True)
print(f'pairs >= 0.72: {len(pairs)}')
for p in pairs:
    print(p)
