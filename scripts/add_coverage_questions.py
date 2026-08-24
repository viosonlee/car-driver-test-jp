# -*- coding: utf-8 -*-
"""覆盖度补充：路面标线 +7 题，环岛/特殊路口 +6 题（q_0767 起）"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = 'src/assets/data/all_questions.json'
with open(path, encoding='utf-8') as f:
    data = json.load(f)
existing = {q['id'] for q in data}

NEW = [
 # ---- 路面标线 ----
 dict(id='q_0767', answer=False,
      question='路面上施划的黄色实线（中央线）表示可以跨越该线进行超车。',
      question_jp='路面上に白線ではなく黄色の実線が中央線として描かれている場合、その線を越えて追越をしてもよい。',
      explanation='中央线为黄色时表示禁止跨线（车辆不得越过该线或其右侧）。黄色实线的禁令比白色实线更严格，超车、变线均不允许。',
      tags=['road_markings','pages_36_40','source_page_38','no_crossing']),
 dict(id='q_0768', answer=True,
      question='交叉路口前停止线（停止線）前方是必须暂时停车等待的位置，即使没有"一時停止"标志，红灯时也应在停止线前停车。',
      question_jp='交差点手前の停止線は、一時的に停止して待つ位置を示すものである。',
      explanation='停止线表示信号灯或临时停车要求下应停车的位置。有停止线时应在其前方停车，不得压线或越线进入路口。',
      tags=['road_markings','pages_36_40','source_page_39','stop_line']),
 dict(id='q_0769', answer=False,
      question='路面上的"軌道敷内通行可"标示表示任何车辆都可以在路面电车的轨道敷内通行。',
      question_jp='「軌道敷内通行可」の標示があっても、すべての車両が軌道敷内を自由に通行できるわけではない。',
      explanation='"轨道敷内通行可"标示允许普通汽车等在指定时段或条件下借用轨道敷通行，但路面电车始终优先，且标示规定以外的情形仍禁止进入。',
      tags=['road_markings','pages_36_40','source_page_39','tram_lane']),
 dict(id='q_0770', answer=True,
      question='路面标示的横向斑马纹菱形图案（前方减速标示）提示前方有人行横道或停止线，应减速。',
      question_jp='路面に描かれた横縞模様のマークは、前方に横断歩道や停止線があることを知らせるもので、減速が必要である。',
      explanation='这类预告标示设置在人行横道、停止线等之前，提醒驾驶人前方需要减速或停车注意。',
      tags=['road_markings','pages_36_40','source_page_39','advance_warning']),
 dict(id='q_0771', answer=False,
      question='车道之间的白色虚线在任何情况下都可以随意跨越变更车道。',
      question_jp='車線境界の白い破線であれば、どのような場合でも自由に車線変更をしてよい。',
      explanation='白色虚线虽可跨线，但变更车道时必须确认安全、不得妨碍后方车辆正常行驶；在禁止变线区间（如隧道、路口附近）依然不可变线。',
      tags=['road_markings','pages_36_40','source_page_38','lane_change']),
 dict(id='q_0772', answer=True,
      question='路缘石旁的黄色虚线表示该路段禁止长时停车（但允许短时间临时停车上下客）。',
      question_jp='路端に引かれた黄色の破線は、駐車禁止（長時間の停車は禁止だが、乗降などの一時停止は可能）を示す。',
      explanation='黄色虚线=禁止长时停车（驻车禁止），上下客、装卸货物等短暂停留不受限；黄色实线则连临时停车也禁止。',
      tags=['road_markings','pages_36_40','source_page_38','curb_line']),
 dict(id='q_0773', answer=False,
      question='导流带（分流岛纹线区域，斜线加白边围成的区域）可以在交通拥堵时临时停放车辆。',
      question_jp='導流帯（斜線で描かれた区域）は、渋滞時に一時的に車を止めておいてよい。',
      explanation='导流带用于引导车流方向、分离交通流，禁止车辆驶入停留，更不能作为停车位使用。',
      tags=['road_markings','pages_36_40','source_page_39','traffic_island']),

 # ---- 环岛/特殊路口 ----
 dict(id='q_0774', answer=True,
      question='驶入环形交叉路口（环岛）的车辆，必须让已经在环岛内通行的车辆先行。',
      question_jp='環状交差点に入ろうとする車両は、環状交差点内を通行中の車両に優先権を譲らなければならない。',
      explanation='环岛内已在通行的车辆优先。准备进入环岛的车辆须观察左侧来车并让行，防止入口碰撞。',
      tags=['roundabout','intersection','pages_16_18','source_page_17','right_of_way']),
 dict(id='q_0775', answer=False,
      question='驶入环形交叉路口时应打开左转向灯示意。',
      question_jp='環状交差点に入るときは、左の方向指示器（ウィンカー）を出さなければならない。',
      explanation='进入环岛时不打灯（直行进入）；只有在驶出环岛（向左离开）时才打左转向灯。这是环岛规则的易错点。',
      tags=['roundabout','intersection','signal','pages_16_18','source_page_17']),
 dict(id='q_0776', answer=False,
      question='在环形交叉路口内，后进入环岛的车辆因车流量大而享有优先通行权。',
      question_jp='環状交差点内では、後から入った車両の方が優先される。',
      explanation='环岛优先权与进入先后无关：环岛内正在通行者优先于所有准备进入的车辆。',
      tags=['roundabout','intersection','pages_16_18','source_page_17','right_of_way']),
 dict(id='q_0777', answer=True,
      question='丁字形（T字形）路口直行时，若道路被对向侧的路端截断，直行车辆也属于"进入路口"，需注意左右确认。',
      question_jp='丁字路において、行き止まり側に突き当たる直進も交差点への進入であり、左右の確認が必要である。',
      explanation='T形路口的"直行"实际上是转弯进入另一条道路，属于路口进入行为，必须提前靠边、减速并确认左右安全。',
      tags=['intersection','t_junction','pages_16_18','source_page_16']),
 dict(id='q_0778', answer=False,
      question='在没有信号灯和标志的多岔路口（五岔路口等），只要鸣喇叭即可直接通过。',
      question_jp='信号機も標識もない多差路では、クラクションを鳴らせばそのまま通過してよい。',
      explanation='无信号无标志的多岔路口适用一般通行规则：注意其他交通参与者、减速慢行、必要时徐行让行，鸣喇叭不能免除让行义务。',
      tags=['intersection','multi_way','slow_down','pages_16_18','source_page_16']),
 dict(id='q_0779', answer=True,
      question='在视线良好的宽阔路口，即使没有信号和标志，也应注意交叉道路的来车后再通过。',
      question_jp='見通しの良い広い交差点でも、信号や標識がなければ交差道路からの来車に注意して通過しなければならない。',
      explanation='无信号无标志路口的基本原则是注意他车、不盲目抢行；双方同时到达时遵循左侧车辆优先等路权规则。',
      tags=['intersection','right_of_way','pages_16_18','source_page_16']),
]

added = 0
for q in NEW:
    if q['id'] not in existing:
        q['type'] = 'true_false'
        data.append(q); added += 1

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'新增 {added} 题，总计 {len(data)} 题')
