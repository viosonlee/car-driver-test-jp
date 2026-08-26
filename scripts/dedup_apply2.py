# -*- coding: utf-8 -*-
"""第二轮去重执行：移除 15 题同事实重复，合并最优解析"""
import json, shutil

SRC = 'src/assets/data/all_questions.json'
shutil.copy(SRC, SRC + '.bak')

qs = json.load(open(SRC, encoding='utf-8'))

REMOVE = {
    'q_0692',  # 交叉路口5m 禁停（与 q_0263 重复，保留原版）
    'q_0693',  # 踏切10m 禁停（与 q_0265 重复，对比表并入 q_0265）
    'q_0694',  # 横断步道5m 禁停（与 q_0264 重复）
    'q_0513',  # 疲劳驾驶（与 q_0099 重复）
    'q_0503',  # 准中型初学者标志（与 q_0608 同规则，解析并入 q_0608）
    'q_0613',  # 上车前确认（与 q_0000 重复，解析并入 q_0000）
    'q_0047',  # 左转弯靠左（与 q_0216 重复）
    'q_0634',  # 超车右侧通过（与 q_0208 重复）
    'q_0602',  # 黄灯必须停（与 q_0417 重复，保留含"车辆和有轨电车"版本）
    'q_0632',  # 变道前3秒信号（与 q_0035 重复）
    'q_ref_26',  # 导流带文字版（保留图片版 q_img_pdf_marking_guide_zone_t）
    'q_0361',  # 挡位矩阵精简：保留 上坡1挡(q_0362) + 下坡1挡错误(q_0384)
    'q_0385',  # 挡位矩阵精简
    'q_0359',  # "夜间8小时"无明确法源且与 q_0358(12小时) 重复
    'q_sign_img_auto_one_way_up_t',  # 单行道上向箭头（与 one_way_t 同考点）
}

by_id = {q['id']: q for q in qs}

# 合并解析（保留信息更全版本）
by_id['q_0000']['explanation'] = (
    '上车前的安全确认是基本义务：确认车身周围有无行人、特别是车底有无小孩'
    '（车底是起步时的典型盲区），同时检查轮胎、灯光等状态，防止起步碾压事故。'
)
by_id['q_0265']['explanation'] = (
    '铁路道口的本体、侧方及其前后各10米以内，禁止长时停车和临时停车。'
    '对比记忆：交叉路口为5米、人行横道前后为5米、公交车站为10米、消防栓为5米。'
)
by_id['q_0608']['explanation'] = (
    '取得普通或准中型驾照未满1年的初学驾驶者，驾驶相应车辆时必须在车辆前后'
    '规定位置张贴初学者标志（若标志脱落也须义务补贴）。'
)

before = len(qs)
qs = [q for q in qs if q['id'] not in REMOVE]
json.dump(qs, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'{before} -> {len(qs)} (removed {before - len(qs)})')
missing = sum(1 for q in qs if not q.get('question_jp'))
print('missing question_jp now:', missing)
