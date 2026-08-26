# -*- coding: utf-8 -*-
"""合并 6 批日文翻译回 all_questions.json，并校验覆盖完整性"""
import json, glob

SRC = 'src/assets/data/all_questions.json'
qs = json.load(open(SRC, encoding='utf-8'))
by_id = {q['id']: q for q in qs}

# 收集所有翻译
translations = {}
for f in sorted(glob.glob('scripts/jp_translate_b*.json')):
    data = json.load(open(f, encoding='utf-8'))
    translations.update(data)

# 校验：翻译文件内部是否有重复 id
assert len(translations) == sum(
    len(json.load(open(f, encoding='utf-8'))) for f in sorted(glob.glob('scripts/jp_translate_b*.json'))
), "translation id duplicates across batches"

missing_ids = [q['id'] for q in qs if not q.get('question_jp')]
assert set(missing_ids) == set(translations.keys()), (
    f"MISMATCH! bank-missing={len(missing_ids)} translations={len(translations)}\n"
    f"in translations but bank not missing: {set(translations) - set(missing_ids)}\n"
    f"bank missing but no translation: {set(missing_ids) - set(translations)}"
)

for qid, jp in translations.items():
    by_id[qid]['question_jp'] = jp

json.dump(qs, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"merged {len(translations)} translations; total questions: {len(qs)}")
print("still missing question_jp:", sum(1 for q in qs if not q.get('question_jp')))
