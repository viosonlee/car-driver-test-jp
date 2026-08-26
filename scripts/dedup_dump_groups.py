# -*- coding: utf-8 -*-
"""导出疑似重复组的完整信息供人工裁决"""
import json

qs = {q['id']: q for q in json.load(open('src/assets/data/all_questions.json', encoding='utf-8'))}

groups = [
    # 多代生成重复（SAME 文本事实）
    ['q_0263', 'q_0692'],
    ['q_0265', 'q_0693'],
    ['q_0264'],
    ['q_0694'], ['q_0740'],
    ['q_0695'], ['q_0696'],
    ['q_0099', 'q_0513'],
    ['q_0503', 'q_0608'],
    ['q_0000', 'q_0613'],
    ['q_0047', 'q_0216'],
    ['q_0208', 'q_0634'],
    ['q_0417', 'q_0602'],
    ['q_0035', 'q_0632'],
    ['q_0358', 'q_0359'],
    # 挡位矩阵
    ['q_0361', 'q_0362', 'q_0384', 'q_0385'],
    # 数字干扰对（DIFF，需确认是否保留）
    ['q_0266', 'q_0288'],
    ['q_0356', 'q_0379'],
    ['q_0269', 'q_0290'],
    ['q_0274', 'q_0297'],
    # 图片题疑似重复
    ['q_sign_img_auto_one_way_t', 'q_sign_img_auto_one_way_up_t'],
    ['q_sign_img_auto_closed_to_bicycles_f', 'q_sign_img_auto_bicycle_crossing_f'],
    ['q_img_pdf_marking_guide_zone_t', 'q_ref_26'],
]

seen = set()
for g in groups:
    print('=' * 80)
    for qid in g:
        q = qs[qid]
        seen.add(qid)
        print(f"[{qid}] ans={q['answer']} img={q.get('image_url','-')}")
        print(f"  Q: {q['question']}")
        print(f"  E: {q['explanation'][:150]}")
print('\nNOT IN BANK:', [q for g in groups for q in g if q not in qs])
