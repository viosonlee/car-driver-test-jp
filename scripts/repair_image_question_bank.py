from __future__ import annotations

from pathlib import Path
import json


QUESTION_PATH = Path("src/assets/data/all_questions.json")


def pair(
    stem: str,
    image: str,
    true_cn: str,
    true_jp: str,
    false_cn: str,
    false_jp: str,
    explanation: str,
    tags: list[str],
) -> list[dict]:
    return [
        {
            "id": f"q_img_pdf_{stem}_t",
            "type": "true_false",
            "question": true_cn,
            "question_jp": true_jp,
            "answer": True,
            "explanation": explanation,
            "image_url": f"/signs/{image}",
            "tags": tags,
        },
        {
            "id": f"q_img_pdf_{stem}_f",
            "type": "true_false",
            "question": false_cn,
            "question_jp": false_jp,
            "answer": False,
            "explanation": explanation,
            "image_url": f"/signs/{image}",
            "tags": tags,
        },
    ]


def add_tag(question: dict, tag: str) -> None:
    tags = question.setdefault("tags", [])
    if tag not in tags:
        tags.append(tag)


def main() -> None:
    questions = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))

    removed_ids = {
        "q_sign_img_auto_warning_pedestrian_crossing_t",
        "q_sign_img_auto_warning_pedestrian_crossing_f",
        "q_sign_img_auto_mark_physical_disability_t",
        "q_sign_img_auto_mark_physical_disability_f",
        "q_sign_img_auto_mark_elderly_t",
        "q_sign_img_auto_mark_elderly_f",
    }
    questions = [question for question in questions if question["id"] not in removed_ids]

    revisions = {
        "q_sign_img_auto_no_entry_t": {
            "question_jp": "この標識は、車両（自転車を含む）がこの方向から進入してはならないことを示している。",
        },
        "q_sign_img_auto_one_way_up_f": {
            "question_jp": "この標識は、この区間では直進しかできず、側道へ進入できないことを示している。",
        },
        "q_sign_img_auto_no_parking_t": {
            "question": "这个标志表示禁止长时停车，但上下客或5分钟以内装卸货物等短暂停车不属于长时停车。",
            "question_jp": "この標識は駐車を禁止しているが、人の乗降や5分以内の荷物の積み卸しなど、駐車に当たらない短時間の停車はできる。",
            "explanation": "蓝底红圈加一条红色斜线是“禁止长时停车”。上下客、5分钟以内装卸货物等法律上不属于长时停车的短暂停车仍可进行。",
        },
        "q_sign_img_auto_no_parking_f": {
            "explanation": "蓝底红圈加一条红色斜线只禁止长时停车；红色交叉斜线才表示长时停车和临时停车均被禁止。",
        },
        "q_sign_img_auto_no_stopping_t": {
            "question": "这个标志表示禁止长时停车和临时停车（驻停均禁止）。",
            "question_jp": "この標識は、駐車と停車の両方を禁止している。",
            "explanation": "蓝底红圈加红色交叉斜线表示“禁止长时及临时停车”。",
        },
        "q_sign_img_auto_no_stopping_f": {
            "explanation": "该标志不区分车辆大小，表示所有车辆原则上都不得长时停车或临时停车。",
        },
        "q_sign_img_auto_no_u_turn_t": {
            "question": "这个标志表示禁止在此路段掉头（回转）。",
            "question_jp": "この標識は、この区間での転回（Uターン）を禁止している。",
        },
        "q_sign_img_auto_road_closed_t": {
            "explanation": "白底红色圆环内有红色交叉斜线，并写有「通行止」，表示行人、车辆和路面电车等均禁止通行。",
        },
        "q_sign_img_auto_road_closed_f": {
            "explanation": "白底红色圆环内有红色交叉斜线，并写有「通行止」，表示行人、车辆和路面电车等均禁止通行。",
        },
        "q_sign_img_auto_closed_to_vehicles_t": {
            "explanation": "红色圆环内有红色斜杠表示“禁止车辆通行”，行人仍可通行。",
        },
        "q_sign_img_auto_closed_to_vehicles_f": {
            "explanation": "红色圆环内有红色斜杠表示“禁止车辆通行”，并不是禁止行人通行。",
        },
        "q_sign_img_auto_exclusive_bus_lane_t": {
            "explanation": "蓝底公交车图案和“专用”字样表示公交车等专用车道。除法律规定的例外或辅助标志允许的车辆外，其他车辆不得持续在该车道行驶。",
        },
        "q_sign_img_auto_exclusive_bus_lane_f": {
            "explanation": "这是公交车等专用车道，而不是所有车辆均可自由使用的公交优先车道。",
        },
        "q_sign_img_auto_roundabout_t": {
            "question": "这个标志表示在环形交叉路口内，车辆必须按照箭头方向顺时针通行。",
            "question_jp": "この標識は、環状交差点内で矢印の方向（右回り）に通行しなければならないことを示している。",
            "explanation": "蓝底白色环形箭头是环形交叉路口内的通行方向指示标志，应按箭头方向顺时针通行。",
        },
        "q_sign_img_auto_roundabout_f": {
            "question": "这个标志是提示前方有环形交叉路口的黄色警告标志。",
            "question_jp": "この標識は、前方に環状交差点があることを予告する黄色の警戒標識である。",
            "explanation": "图片是蓝色指示标志，表示环形交叉路口内的通行方向；预告前方环形交叉路口的是黄色菱形警告标志。",
        },
        "q_sign_img_auto_safe_zone_t": {
            "explanation": "蓝底白色 V 形图案表示“安全地带”。车辆不得驶入安全地带。",
        },
        "q_sign_img_auto_safe_zone_f": {
            "explanation": "蓝底白色 V 形图案表示“安全地带”，并不是车辆临时停车避险区域。",
        },
        "q_sign_img_auto_stopping_permitted_t": {
            "explanation": "蓝底白字「停」表示允许临时停车，但不表示允许长时停车。",
        },
        "q_sign_img_auto_stopping_permitted_f": {
            "explanation": "蓝底白字「停」表示允许临时停车，与掉头指示无关。",
        },
        "q_sign_img_auto_safe_zone_f": {
            "question_jp": "この標識は、車両がこの区域内に一時停止して危険を避けてもよいことを示している。",
        },
        "q_sign_img_auto_warning_t_junction_t": {
            "question": "这个标志提示前方有 T 形交叉路口。",
            "question_jp": "この標識は、前方にT形交差点があることを示している。",
        },
        "q_sign_img_auto_warning_t_junction_f": {
            "question": "这个标志提示前方有环形交叉路口。",
            "question_jp": "この標識は、前方に環状交差点があることを示している。",
        },
        "q_sign_img_auto_warning_right_curve_t": {
            "question": "这个标志提示前方道路向右弯曲。",
            "question_jp": "この標識は、前方の道路が右に曲がっていることを示している。",
            "explanation": "黄色菱形内的右弯箭头表示前方道路向右弯曲。",
        },
        "q_sign_img_auto_warning_right_curve_f": {
            "question": "这个标志提示前方道路向左弯曲。",
            "question_jp": "この標識は、前方の道路が左に曲がっていることを示している。",
            "explanation": "黄色菱形内的箭头向右弯曲，因此不是左弯标志。",
        },
        "q_sign_img_auto_warning_left_curve_t": {
            "question": "这个标志提示前方道路向左弯曲。",
            "question_jp": "この標識は、前方の道路が左に曲がっていることを示している。",
            "explanation": "黄色菱形内的左弯箭头表示前方道路向左弯曲。",
        },
        "q_sign_img_auto_warning_left_curve_f": {
            "question": "这个标志提示前方道路向右弯曲。",
            "question_jp": "この標識は、前方の道路が右に曲がっていることを示している。",
            "explanation": "黄色菱形内的箭头向左弯曲，因此不是右弯标志。",
        },
        "q_sign_img_auto_warning_winding_road_t": {
            "image_url": "/signs/warning_winding_road.png",
        },
        "q_sign_img_auto_warning_winding_road_f": {
            "image_url": "/signs/warning_winding_road.png",
        },
        "q_sign_img_auto_warning_railway_crossing_f": {
            "question": "这个标志提示前方设有交通信号灯。",
            "question_jp": "この標識は、前方に信号機があることを示している。",
        },
        "q_sign_img_auto_warning_traffic_light_t": {
            "image_url": "/signs/warning_traffic_light.png",
        },
        "q_sign_img_auto_warning_traffic_light_f": {
            "image_url": "/signs/warning_traffic_light.png",
            "question": "这个标志提示前方有铁路道口。",
            "question_jp": "この標識は、前方に踏切があることを示している。",
        },
        "q_sign_img_auto_warning_lane_ends_f": {
            "question": "这个标志提示前方道路整体变窄。",
            "question_jp": "この標識は、前方で道路全体の幅が狭くなることを示している。",
        },
        "q_sign_img_auto_warning_road_narrows_f": {
            "question": "这个标志提示前方车线数量减少。",
            "question_jp": "この標識は、前方で車線数が減少することを示している。",
        },
        "q_sign_img_auto_warning_road_work_f": {
            "question": "这个标志提示前方有其他未分类的危险。",
            "question_jp": "この標識は、前方にその他の危険があることを示している。",
        },
        "q_sign_img_auto_warning_other_dangers_f": {
            "question": "这个标志提示前方正在进行道路施工。",
            "question_jp": "この標識は、前方で道路工事が行われていることを示している。",
        },
        "q_sign_img_auto_warning_strong_wind_f": {
            "question": "这个标志提示前方路面容易打滑。",
            "question_jp": "この標識は、前方の路面が滑りやすいことを示している。",
        },
        "q_sign_img_auto_warning_animals_f": {
            "question": "这个标志提示前方有学校、幼儿园或保育所。",
            "question_jp": "この標識は、前方に学校、幼稚園または保育所があることを示している。",
        },
        "q_sign_img_auto_speed_limit_50_f": {
            "question_jp": "この標識は、この区間の最低速度が50km/hであることを示している。",
        },
        "q_sign_img_auto_slow_down_t": {
            "explanation": "写有「徐行」的红色倒三角形是“徐行”标志。驾驶员必须以能够立即停车的速度行驶。",
        },
        "q_sign_img_auto_slow_down_f": {
            "explanation": "写有「徐行」的红色倒三角形是“徐行”标志。驾驶员必须以能够立即停车的速度行驶。",
        },
        "q_sign_img_auto_parking_permitted_t": {
            "question_jp": "この標識は、車両がここで駐車できることを示している。",
        },
        "q_0198": {"type": "true_false"},
        "q_0199": {"type": "true_false"},
        "q_0398": {"type": "true_false"},
        "q_0399": {"type": "true_false"},
    }
    for question in questions:
        if question["id"] in revisions:
            question.update(revisions[question["id"]])

        image_url = question.get("image_url", "")
        if not image_url:
            continue
        if "/warning_" in image_url:
            add_tag(question, "traffic_signs")
            add_tag(question, "source_page_37")
        elif "/marking_" in image_url:
            add_tag(question, "road_markings")
        elif "/mark_" not in image_url:
            add_tag(question, "traffic_signs")
            add_tag(question, "source_page_36")
        else:
            add_tag(question, "traffic_signs")
            add_tag(question, "source_page_15")

    additions: list[dict] = []
    warning_tags = ["traffic_signs", "warning_signs", "image_recognition", "source_page_37"]
    additions += pair("warning_y_junction", "warning_y_junction.png", "这个标志提示前方有 Y 形交叉路口。", "この標識は、前方にY形交差点があることを示している。", "这个标志表示前方道路只能向左或向右分流，禁止直行。", "この標識は、前方で左右方向にしか進めず、直進できないことを示している。", "黄色菱形内的 Y 形图案用于预告前方的 Y 形交叉路口。", warning_tags.copy())
    additions += pair("warning_roundabout_ahead", "warning_roundabout_ahead.png", "这个标志提示前方有环形交叉路口。", "この標識は、前方に環状交差点があることを示している。", "这个标志表示车辆已经进入环形交叉路口，必须立即停车。", "この標識は、すでに環状交差点内に入り、直ちに停止しなければならないことを示している。", "黄色菱形内的环形箭头是环形交叉路口预告标志。", warning_tags.copy())
    additions += pair("warning_slippery", "warning_slippery.png", "这个标志提示前方路面容易打滑。", "この標識は、前方の路面が滑りやすいことを示している。", "这个标志提示前方有连续弯路。", "この標識は、前方に連続したカーブがあることを示している。", "车辆出现侧滑轨迹的图案表示前方路面容易打滑。", warning_tags.copy())
    additions += pair("warning_falling_rocks", "warning_falling_rocks.png", "这个标志提示前方有落石危险。", "この標識は、前方に落石のおそれがあることを示している。", "这个标志提示前方是陡峭上坡。", "この標識は、前方が急な上り坂であることを示している。", "山坡落石图案用于提醒驾驶者注意落石和路面上的石块。", warning_tags.copy())
    additions += pair("warning_uneven_road", "warning_uneven_road.png", "这个标志提示前方路面不平。", "この標識は、前方の路面に凹凸があることを示している。", "这个标志表示前方路面平坦，可以提高速度。", "この標識は、前方の路面が平坦で速度を上げてもよいことを示している。", "凸凹图案表示前方路面不平，应控制速度。", warning_tags.copy())
    additions += pair("warning_merge", "warning_merge.png", "这个标志提示前方有道路汇流。", "この標識は、前方で道路が合流することを示している。", "这个标志提示前方车道数量增加。", "この標識は、前方で車線数が増えることを示している。", "支路并入主路的图案表示前方有道路汇流。", warning_tags.copy())
    additions += pair("warning_two_way", "warning_two_way.png", "这个标志提示前方开始双向通行。", "この標識は、前方から対面通行になることを示している。", "这个标志表示前方道路为单行道。", "この標識は、前方の道路が一方通行であることを示している。", "上下相反的两个箭头表示前方开始双向通行。", warning_tags.copy())
    additions += pair("warning_uphill", "warning_uphill.png", "这个标志提示前方是坡度为 10% 的陡峭上坡。", "この標識は、前方が勾配10%の急な上り坂であることを示している。", "这个标志表示该路段最高速度为 10km/h。", "この標識は、この区間の最高速度が10km/hであることを示している。", "带有上坡车辆和坡度数值的警告标志表示前方陡峭上坡。", warning_tags.copy())
    additions += pair("warning_downhill", "warning_downhill.png", "这个标志提示前方是坡度为 10% 的陡峭下坡。", "この標識は、前方が勾配10%の急な下り坂であることを示している。", "这个标志表示车辆必须以不低于 10km/h 的速度行驶。", "この標識は、10km/h以上の速度で走行しなければならないことを示している。", "带有下坡车辆和坡度数值的警告标志表示前方陡峭下坡。", warning_tags.copy())

    marking_38 = ["road_markings", "image_recognition", "source_page_38"]
    marking_39 = ["road_markings", "image_recognition", "source_page_39"]
    additions += pair("marking_no_u_turn", "marking_no_u_turn.png", "这个路面标示表示在标明的时间段内禁止掉头。", "この路面標示は、表示された時間帯に転回が禁止されていることを示している。", "这个路面标示表示车辆可以自由掉头。", "この路面標示は、車両が自由に転回できることを示している。", "掉头箭头上带叉号，并附有时间时，表示在该时段内禁止掉头。", marking_38.copy())
    additions += pair("marking_speed_limit_30", "marking_speed_limit_30.png", "这个路面数字标示表示最高速度为 30km/h。", "この路面の数字標示は、最高速度が30km/hであることを示している。", "这个路面数字标示表示最低速度为 30km/h。", "この路面の数字標示は、最低速度が30km/hであることを示している。", "路面上的黄色速度数字用于表示最高速度限制。", marking_38.copy())
    additions += pair("marking_no_entry_zone", "marking_no_entry_zone.png", "黄色边框内的斜线区域表示车辆不得驶入。", "黄色い枠内の斜線部分は、車両が進入してはならない区域を示している。", "黄色边框内的区域是车辆临时停车区。", "黄色い枠内の区域は、車両の一時停止場所を示している。", "禁止驶入区域用于引导交通，车辆不得进入该标示范围。", marking_38.copy())
    additions += pair("marking_bus_lane", "marking_bus_lane.png", "这个路面标示表示指定时间内为公交车专用车道。", "この路面標示は、指定された時間帯にバス専用通行帯となることを示している。", "这个路面标示表示所有车辆在指定时间内都可以使用该车道。", "この路面標示は、指定された時間帯にすべての車両がその車線を利用できることを示している。", "“公交专用”及时间标示表示该时段内车道供规定的公交车辆专用。", marking_38.copy())
    additions += pair("marking_pedestrian_crossing", "marking_pedestrian_crossing.png", "这个白色条纹路面标示表示人行横道。", "この白い縞模様の路面標示は、横断歩道を示している。", "这个路面标示表示车辆停车位。", "この路面標示は、車両の駐車場所を示している。", "平行白色条纹横跨车道时表示人行横道。", marking_39.copy())
    additions += pair("marking_bicycle_crossing", "marking_bicycle_crossing.png", "这个带自行车图案的路面标示表示自行车横道。", "この自転車の図柄がある路面標示は、自転車横断帯を示している。", "这个路面标示表示自行车停车场。", "この路面標示は、自転車駐車場を示している。", "自行车图案与横向标线组合用于表示自行车横道。", marking_39.copy())
    additions += pair("marking_safety_zone", "marking_safety_zone.png", "黄色边线围成的区域表示安全地带，车辆不得驶入。", "黄色い線で囲まれた区域は安全地帯を示し、車両は進入してはならない。", "黄色边线围成的区域是车辆装卸货物的停车区。", "黄色い線で囲まれた区域は、荷物を積み卸しするための駐車場所を示している。", "安全地带用于保护行人或乘客，车辆不得进入。", marking_39.copy())
    additions += pair("marking_guide_zone", "marking_guide_zone.png", "道路上的导流带用于安全、顺畅地引导交通，车辆不得驶入。", "道路上の導流帯は交通を安全かつ円滑に誘導するための区域で、車両は進入してはならない。", "道路上的导流带是允许车辆等待右转的区域。", "道路上の導流帯は、車両が右折待ちをするための区域を示している。", "导流带通过斜线等标示引导车流，属于车辆不能通行的区域。", marking_39.copy())

    if not any(question["id"] == "q_0598" for question in questions):
        additions.append({
            "id": "q_0598",
            "type": "true_false",
            "question": "雨天行驶时，前方路边停着遮挡视线的车辆，应减速并预防有人从车辆前方突然横穿。",
            "question_jp": "雨天に、前方の路肩に視界を遮る駐車車両がある場合は、減速し、車両の前から人が飛び出すことを予測しなければならない。",
            "answer": True,
            "explanation": "雨天制动距离变长，停放车辆又会形成盲区。应减速并做好随时停车的准备。",
            "tags": ["hazard_awareness", "rain", "parked_car"],
        })

    existing_ids = {question["id"] for question in questions}
    new_questions = [question for question in additions if question["id"] not in existing_ids]
    insert_at = next((index for index, question in enumerate(questions) if not question.get("image_url")), len(questions))
    questions[insert_at:insert_at] = new_questions

    QUESTION_PATH.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Removed {len(removed_ids)} invalid image questions; added {len(new_questions)} verified questions; total {len(questions)}")


if __name__ == "__main__":
    main()
