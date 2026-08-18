# -*- coding: utf-8 -*-
"""补充 P1 缺口题目：徐行、追越禁止、高速、ながら/あおり、灾害。"""
from __future__ import annotations

import json
import re
from pathlib import Path

Q_PATH = Path("src/assets/data/all_questions.json")

# ============ I. 徐行定义与适用场所（5题，P1） ============
SLOW_DOWN = [
    ("“徐行”的法律定义是：以能够立即停止的速度行驶（通常认为约 1 米内能停稳的速度），法律没有规定具体时速。",
     "「徐行」とは、直ちに停止することができるような速度（通常、約1メートル以内で停止できる速度と考えられている）で進行することをいい、具体的な時速は法律で定められていない。",
     True,
     "徐行的法律定义是外免切替高频考点。",
     ["traffic_rules", "chapter_4_to_6", "source_page_16", "slow_down"]),
    ("在没有信号灯且视线不良的交叉路口，即使没有“一时停止”标志，也必须徐行，确认左右安全后通过。",
     "信号機がなく見通しの悪い交差点では、「止まれ」の標識がなくても徐行し、左右の安全を確認してから通過しなければならない。",
     True,
     "视线不良交叉路口必须徐行。",
     ["traffic_rules", "chapter_4_to_6", "source_page_16", "slow_down", "intersection"]),
    ("在坡道顶部附近视线受阻时，应徐行通过。",
     "坂の頂上付近で見通しがきかないときは、徐行して通過しなければならない。",
     True,
     "坡道顶部须徐行。",
     ["traffic_rules", "chapter_4_to_6", "source_page_16", "slow_down", "uphill"]),
    ("在视线不良的弯道处，应徐行通过。",
     "見通しの悪いカーブでは、徐行して通過しなければならない。",
     True,
     "视线不良弯道须徐行。",
     ["traffic_rules", "chapter_4_to_6", "source_page_16", "slow_down", "cornering"]),
    ("在应徐行的场所，徐行与“一时停止”的含义相同，都需要把车完全停下来。",
     "徐行すべき場所では、徐行と「一時停止」は同じ意味で、車を完全に停止させる必要がある。",
     False,
     "徐行≠停车。徐行是缓慢行进能随时停车，一時停止是完全停稳。",
     ["traffic_rules", "chapter_4_to_6", "source_page_16", "slow_down", "stop"]),
]

# ============ J. 追越禁止场所（8题，P1） ============
NO_OVERTAKING = [
    ("在隧道内，除有中央线虚线的路段等特殊情形外，原则上禁止追越。",
     "トンネル内では、中央線が破線で引かれている区間などの特別な場合を除き、原則として追い越しをしてはならない。",
     True,
     "隧道内原则上禁止追越。",
     ["traffic_rules", "chapter_7_to_8", "source_page_18", "no_overtaking"]),
    ("在交叉路口及其 30 米以内的区域，禁止追越。",
     "交差点とその端から30メートル以内の区域では、追い越しをしてはならない。",
     True,
     "交差点30m以内禁止追越。",
     ["traffic_rules", "chapter_7_to_8", "source_page_18", "no_overtaking"]),
    ("在人行横道（横断歩道）和自行车横道及其 30 米以内的区域，禁止追越。",
     "横断歩道・自転車横断帯とその端から30メートル以内の区域では、追い越しをしてはならない。",
     True,
     "横道30m以内禁止追越。",
     ["traffic_rules", "chapter_7_to_8", "source_page_18", "no_overtaking"]),
    ("在坡道顶部附近视线受阻的地方，禁止追越。",
     "坂の頂上付近で見通しがきかない場所では、追い越しをしてはならない。",
     True,
     "坡道顶禁止追越。",
     ["traffic_rules", "chapter_7_to_8", "source_page_18", "no_overtaking", "uphill"]),
    ("在弯道等视线不良的地方，禁止追越。",
     "カーブなど見通しの悪い場所では、追い越しをしてはならない。",
     True,
     "弯道禁止追越。",
     ["traffic_rules", "chapter_7_to_8", "source_page_18", "no_overtaking", "cornering"]),
    ("追越时，应从被追越车辆的右侧通过（在单向 3 车道以上的道路等例外场合，左侧也可追越）。",
     "追い越しは、追い越される車両の右側から行う（片側3車線以上の道路など例外がある）。",
     True,
     "追越原则上右侧。",
     ["traffic_rules", "chapter_7_to_8", "source_page_18", "overtaking"]),
    ("追越完成后，应在不影响被追越车辆的前提下，尽快回到原来的车道。",
     "追い越しが終わったら、追い越された車両の走行を妨げないように、速やかに元の車線に戻る。",
     True,
     "追越完成后尽快回原车道。",
     ["traffic_rules", "chapter_7_to_8", "source_page_18", "overtaking"]),
    ("当前方车辆正在右转或准备右转时，禁止从该车辆右侧追越。",
     "前方の車両が右折しているとき又は右折しようとしているときは、その車両の右側から追い越してはならない。",
     True,
     "前方车右转时禁止从其右侧追越。",
     ["traffic_rules", "chapter_7_to_8", "source_page_18", "no_overtaking"]),
]

# ============ K. 高速道路（8题，P1） ============
EXPRESSWAY = [
    ("在高速汽车国道上，除标志另有规定外，普通汽车的最高速度为时速 100km。",
     "高速自動車国道では、標識で別に定められている場合を除き、普通自動車の最高速度は時速100キロメートルである。",
     True,
     "高速100km/h法定最高速度。",
     ["traffic_rules", "chapter_7_to_8", "source_page_27", "expressway", "speed"]),
    ("在高速汽车国道上，最低速度为时速 50km；以低于最低速度行驶将受到处罚。",
     "高速自動車国道では、最低速度は時速50キロメートルで、これより遅い速度で走行すると処罰される。",
     True,
     "高速最低50km/h。",
     ["traffic_rules", "chapter_7_to_8", "source_page_27", "expressway", "speed"]),
    ("在高速公路上，汇入主车道前应在加速车道上加速，并观察主车道来车情况，找准时机汇入。",
     "高速道路では、本線に合流する前に加速車線で加速し、本線の車両の状況を見てタイミングを計って合流する。",
     True,
     "加速车道合流要领。",
     ["traffic_rules", "chapter_7_to_8", "source_page_27", "expressway", "merge"]),
    ("在高速公路上，即使走错了出口，也禁止倒车、逆行或穿过中央分隔带掉头。",
     "高速道路で出口を間違えても、バック・逆走・中央分離帯の切れ目を通っての転回は禁止されている。",
     True,
     "高速禁止倒车逆行。",
     ["traffic_rules", "chapter_7_to_8", "source_page_27", "expressway", "prohibited_acts"]),
    ("在高速公路上，除故障等不得已的情况外，禁止停车和临时停车，也禁止在行车道和路肩上停车。",
     "高速道路では、故障などのやむを得ない場合を除き、駐停車は禁止されており、走行車線や路肩に停めることもできない。",
     True,
     "高速原则上禁止驻停。",
     ["traffic_rules", "chapter_7_to_8", "source_page_27", "expressway", "parking"]),
    ("在高速公路上车辆发生故障时，应驶入紧急停车带（路肩）停车，开启危险警告灯，并在车辆后方放置故障警示器材。",
     "高速道路で車両が故障したときは、非常停車帯（路肩）に停車し、非常点滅表示灯をつけ、車の後方に故障表示器材を置く。",
     True,
     "高速故障应急处置。",
     ["traffic_rules", "chapter_7_to_8", "source_page_27", "expressway", "breakdown"]),
    ("在高速公路上行驶时，应尽量在右侧车道（快车道）连续行驶，而不是在左侧车道行驶。",
     "高速道路を走行するときは、左側の車線ではなく、できるだけ右側の車線（追越車線）を連続して走行するのがよい。",
     False,
     "高速应靠左侧车道行驶，右侧是追越车道。",
     ["traffic_rules", "chapter_7_to_8", "source_page_27", "expressway"]),
    ("在高速公路上遇到暴雨、浓雾等恶劣天气导致视线严重不良时，应降低车速并开启危险警告灯等，确保安全行驶。",
     "高速道路で大雨・濃霧などにより視界が著しく悪くなったときは、速度を落とし、非常点滅表示灯をつけるなどして安全に走行する。",
     True,
     "恶劣天气高速减速。",
     ["traffic_rules", "chapter_7_to_8", "source_page_27", "expressway", "rain"]),
]

# ============ L. ながら運転・あおり運転（8题，P1） ============
DISTRACTED = [
    ("驾驶中手持手机通话，即使通话时间很短，也属于禁止行为（ながら運転）。",
     "運転中に携帯電話を手で持って通話することは、たとえ短時間でも禁止行為（ながら運転）にあたる。",
     True,
     "手持手机通话即违规。",
     ["prohibited_acts", "traffic_rules", "smartphone"]),
    ("驾驶中操作手机查看地图、发送信息等行为，即使车辆处于停止状态（如红灯等待时），原则上也属于违规。",
     "運転中に携帯電話を操作して地図を見る・メッセージを送るなどの行為は、車両が停止しているとき（赤信号待ちなど）でも原則として違反となる。",
     True,
     "红灯等待时操作手机同样违规。",
     ["prohibited_acts", "traffic_rules", "smartphone"]),
    ("在驾驶中，为了确认导航信息，可以短时间单手操作智能手机。",
     "運転中、ナビゲーションの情報を確認するためなら、短時間であれば片手でスマートフォンを操作してもよい。",
     False,
     "驾驶中操作手机一律禁止。",
     ["prohibited_acts", "traffic_rules", "smartphone"]),
    ("“妨碍驾驶”（あおり運転）指为了妨碍前方车辆行驶而进行的急速逼近、急刹车、蛇行等危险行为。",
     "「妨害運転」（あおり運転）とは、前方車両の走行を妨害する目的で、急に接近する・急ブレーキをかける・蛇行するなどの危険な行為をいう。",
     True,
     "妨害驾驶罪定义。",
     ["prohibited_acts", "traffic_rules", "dangerous_driving"]),
    ("因不满前方车辆速度慢，从后方强烈逼近并用远光灯闪照对方，属于被处罚的危险驾驶行为。",
     "前方車両の速度が遅いことに腹を立て、後方から強く接近してハイビームで照らすことは、処罰の対象となる危険な運転行為である。",
     True,
     "逼近+闪灯属于妨害驾驶。",
     ["prohibited_acts", "traffic_rules", "dangerous_driving"]),
    ("为了“教训”前方车辆，故意在其面前急刹车，属于妨害驾驶（あおり運転），会被处罚。",
     "前方車両を「懲らしめる」ために、わざとその直前で急ブレーキをかけることは、妨害運転（あおり運転）にあたり処罰される。",
     True,
     "故意急刹属妨害驾驶。",
     ["prohibited_acts", "traffic_rules", "dangerous_driving"]),
    ("在道路上故意蛇行、左右摇摆行驶，会妨碍其他交通参与者，属于禁止的危险驾驶行为。",
     "道路でわざと蛇行・ふらつき運転をすることは、他の交通を妨げ、禁止されている危険な運転行為である。",
     True,
     "蛇行属危险驾驶。",
     ["prohibited_acts", "traffic_rules", "dangerous_driving"]),
    ("在高速公路上长时间占用超车道行驶，只要速度没有超速，就不算违规。",
     "高速道路で追越車線を長時間走行していても、速度が制限を超えていなければ違反にはならない。",
     False,
     "高速长时间占用追越车道是违规行为（通行区分違反）。",
     ["prohibited_acts", "traffic_rules", "expressway"]),
]

# ============ M. 灾害时对应（5题，P1） ============
DISASTER = [
    ("在地震发生时，驾驶员应将车辆靠道路左侧停下，并在注意周围情况的同时通过广播等获取信息。",
     "地震が発生したとき、運転者は車を道路の左側に寄せて止め、周囲の状況に注意しながらラジオなどで情報を得る。",
     True,
     "地震时靠左停车。",
     ["traffic_rules", "chapter_7_to_8", "source_page_33", "disaster"]),
    ("听到紧急地震速报（J-Alert）时，即使正在高速公路上，也应在确保安全的前提下逐渐减速并靠边停车。",
     "緊急地震速報（Jアラート）が発表されたとき、高速道路を走行中でも、安全を確保した上で徐々に減速し路肩に停車する。",
     True,
     "紧急地震速报时减速停车。",
     ["traffic_rules", "chapter_7_to_8", "source_page_33", "disaster"]),
    ("看到消防车、救护车等紧急车辆靠近时，应尽快避让，必要时在交叉路口停车或让行。",
     "消防車・救急車などの緊急自動車が近づいてきたときは、速やかに避け、必要に応じて交差点で停止又は譲る。",
     True,
     "紧急车辆避让。",
     ["traffic_rules", "chapter_7_to_8", "source_page_33", "emergency_vehicle"]),
    ("灾害发生时，警察等实施交通管制时，必须服从管制人员的指挥。",
     "災害発生時、警察などが交通規制を行っているときは、規制に従わなければならない。",
     True,
     "服从交通管制。",
     ["traffic_rules", "chapter_7_to_8", "source_page_33", "disaster"]),
    ("看到前方有落石、塌方等危险的标志或现场时，应停车等待障碍清除后再通过。",
     "前方に落石・土砂崩れなどの危険を示す標識や現場を見つけたときは、停止して障害物が取り除かれるのを待ってから通過する。",
     True,
     "落石危险路段应停车确认。",
     ["traffic_rules", "chapter_7_to_8", "source_page_33", "disaster", "falling_rocks"]),
]

if __name__ == "__main__":
    with Q_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    max_no = max(
        int(q["id"].split("_")[-1])
        for q in data
        if re.fullmatch(r"q_\d+", q["id"])
    )
    start = max_no + 1

    new_questions = []
    for group in (SLOW_DOWN, NO_OVERTAKING, EXPRESSWAY, DISTRACTED, DISASTER):
        for q, jp, ans, expl, tags in group:
            new_questions.append({
                "id": f"q_{start:04d}",
                "type": "true_false",
                "question": q,
                "question_jp": jp,
                "answer": ans,
                "explanation": expl,
                "tags": tags,
            })
            start += 1

    ref_start = next(i for i, q in enumerate(data) if q["id"].startswith("q_ref_"))
    data[ref_start:ref_start] = new_questions

    with Q_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"新增 {len(new_questions)} 题（q_{max_no+1:04d} ~ q_{start-1:04d}），题库总数 {len(data)}")
