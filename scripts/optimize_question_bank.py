from pathlib import Path
import json


QUESTION_PATH = Path("src/assets/data/all_questions.json")


def new_question(identifier: str, question: str, answer: bool, explanation: str, page: int, tags: list[str]) -> dict:
    return {
        "id": identifier.replace("q_06", "q_ref_"),
        "type": "true_false",
        "question": question,
        "answer": answer,
        "explanation": explanation,
        "tags": [*tags, f"source_page_{page}"],
    }


def main() -> None:
    questions = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))

    # q_0147 introduces insurance settlement/criminal-liability claims not stated in the book.
    # q_0583 is about licence renewal, which is outside this edition's contents.
    # q_0542 duplicates q_0608 after source-aligned wording; q_0603 duplicates q_0427.
    removed_ids = {"q_0147", "q_0542", "q_0583", "q_0603"}
    questions = [question for question in questions if question["id"] not in removed_ids]

    revisions = {
        "q_0130": {
            "question": "除非为了避免危险，其他车辆不得从侧面靠近或强行插入张贴高龄驾驶者标志的汽车。",
            "answer": True,
            "explanation": "对张贴高龄驾驶者标志的汽车，应给予保护，不得从侧面靠近或强行插入。",
        },
        "q_0169": {
            "question": "在路口以外遇到执行紧急任务的救护车驶近时，应靠道路左侧让行。",
            "answer": True,
            "explanation": "在路口以外，应靠道路左侧给紧急车辆让路；在单行道上靠左反而妨碍通行时，可以靠右让行。",
        },
        "q_0179": {
            "question": "跟随前车行驶时，应保持即使前车突然刹车也能够避免碰撞的安全车距。",
            "answer": True,
            "explanation": "安全车距应结合速度、路面和轮胎状况确定，确保前车突然刹车时也能避免碰撞。",
        },
        "q_0187": {
            "question": "前车遮挡视线时，也不应缩短车距，而应保持能够安全停车的距离。",
            "answer": True,
            "explanation": "紧跟前车会扩大视线盲区，并在前车突然刹车时增加追尾风险，因此必须保持安全车距。",
        },
        "q_0516": {
            "question": "即使饮酒量很少、本人感觉清醒，饮酒后也不得驾驶车辆。",
            "answer": True,
            "explanation": "饮酒会影响判断和操作能力。饮酒后不得驾驶，也不得让饮酒者驾驶车辆。",
        },
        "q_0542": {
            "question": "取得普通驾照未满1年的驾驶者驾驶普通汽车时，应在车辆前后规定位置张贴初学者标志。",
            "answer": True,
            "explanation": "教材规定，取得普通驾照未满1年的初学驾驶者驾驶普通汽车时，应张贴初学者标志。",
        },
        "q_0592": {
            "explanation": "驾驶前应确认自己的身体状态。视力不足时不应勉强驾驶，应佩戴能够保证看清道路的眼镜。",
        },
    }
    for question in questions:
        if question["id"] in revisions:
            question.update(revisions[question["id"]])

    additions = [
        new_question("q_0604", "私家普通载客汽车也需要根据行驶距离和驾驶状态，在适当时间进行日常检查。", True, "日常检查由汽车使用人或驾驶者负责，应根据行驶距离和车辆状态选择适当时间实施。", 9, ["vehicle_check", "pre_drive"]),
        new_question("q_0605", "检查轮胎气压时，只看仪表盘没有报警即可，不需要观察轮胎接地部分的塌陷状态。", False, "教材要求根据轮胎接触地面部分的塌陷状态检查气压是否不足。", 9, ["vehicle_check", "tires"]),
        new_question("q_0606", "驾驶前应检查前照灯、刹车灯和转向灯是否能够正常点亮或闪烁。", True, "车灯装置的工作状态属于日常检查项目。", 9, ["vehicle_check", "lights"]),
        new_question("q_0607", "刹车踏板踩下后感觉软弱无力，可能与制动液泄漏或制动系统混入空气有关。", True, "踏板行程异常或踏感软弱可能表示制动液泄漏或制动系统混入空气。", 9, ["vehicle_check", "brakes"]),
        new_question("q_0608", "只要车辆平时没有发生故障，就不必检查刮雨器和挡风玻璃清洗液。", False, "清洗液液量、喷射状态以及刮雨器的动作和刮净效果都属于检查项目。", 9, ["vehicle_check", "visibility"]),
        new_question("q_0609", "在高速公路上行驶时，除发焰筒等紧急信号用品外，还应配备故障停车警示器材。", True, "教材要求车辆配备紧急信号用品，并在高速公路行驶时配备停车警示器材。", 10, ["vehicle_check", "expressway"]),
        new_question("q_0610", "普通汽车装载物的长度和宽度都可以达到车身相应尺寸的1.2倍以内。", True, "教材规定装载物长度小于车长的1.2倍、宽度小于车宽的1.2倍，并限制前后左右伸出量。", 10, ["loading", "vehicle_rules"]),
        new_question("q_0611", "装载货物时，只要没有超过重量限制，即使遮住牌照、转向灯或刹车灯也没有问题。", False, "装载物不得妨碍驾驶、影响车辆稳定，也不得遮挡牌照和各种车灯。", 10, ["loading", "vehicle_rules"]),
        new_question("q_0612", "驾驶者必须关紧车门并牢固固定货物，防止人员或货物滚落、飞散。", True, "防止人员和货物滚落、飞散是驾驶者的责任。", 10, ["loading", "vehicle_rules"]),
        new_question("q_0613", "施工用安全帽可以代替符合标准的摩托车安全头盔。", False, "摩托车安全头盔应有PSC或JIS标志，施工用安全帽不能代替。", 28, ["motorcycle", "protective_gear"]),
        new_question("q_0614", "取得普通两轮摩托车驾照未满1年时，不得驾驶普通两轮摩托车载人。", True, "教材将取得普通两轮驾照未满1年列为禁止载人的情况。", 28, ["motorcycle", "passenger"]),
        new_question("q_0615", "摩托车驾驶者在夜间应尽量穿容易被发现或带反光材料的服装。", True, "提高可见性有助于其他道路使用者及时发现摩托车驾驶者。", 28, ["motorcycle", "protective_gear"]),
        new_question("q_0616", "摩托车车身较小、机动性强，所以堵车时可以在车辆之间蛇形穿行。", False, "车辆间穿行、蛇形驾驶、强行超车和强行插入都十分危险。", 29, ["motorcycle", "safe_driving"]),
        new_question("q_0617", "摩托车进入弯道前应先在直线路段充分减速，并通过适当倾斜车体自然转弯。", True, "教材要求入弯前减速，转弯时通过倾斜车体自然转弯。", 29, ["motorcycle", "cornering"]),
        new_question("q_0618", "摩托车刹车时应尽量保持车体垂直，并配合前后轮刹车和发动机制动。", True, "保持车体垂直并合理使用前后轮制动及发动机制动，可以降低侧滑风险。", 30, ["motorcycle", "brakes"]),
        new_question("q_0619", "推着已经关闭发动机、未牵引其他车辆且不带挎斗的两轮摩托车行走时，通常被视为步行者。", True, "符合教材所列条件时，推车行走者按步行者处理。", 30, ["motorcycle", "pedestrian_rules"]),
        new_question("q_0620", "客运汽车驾驶者为了准点，可以通过急起步和急刹车缩短运行时间。", False, "客运汽车驾驶者应保护乘客，避免急起步、急刹车和不必要的颠簸。", 31, ["commercial_vehicle", "passenger_safety"]),
        new_question("q_0621", "车辆必须办理登记或申请，取得并安装车牌号后才能依法使用。", True, "教材规定车辆必须登记；轻型汽车办理申请，并领取、安装车牌号。", 34, ["vehicle_management", "registration"]),
        new_question("q_0622", "小型摩托车不需要加入汽车损害赔偿责任保险或责任共济。", False, "教材明确指出小型摩托车也必须加入自赔责保险或责任共济。", 34, ["vehicle_management", "insurance"]),
        new_question("q_0623", "车辆所有人不得把汽车借给无驾照者或饮酒者，并应妥善保管车钥匙。", True, "这是教材列出的车辆管理责任。", 34, ["vehicle_management", "alcohol_drugs"]),
        new_question("q_0624", "“禁止长时及临时停车”标志表示停车和临时停车都被禁止。", True, "该管制标志同时禁止长时停车和临时停车。", 36, ["traffic_signs", "parking"]),
        new_question("q_0625", "警告标志主要用于表示前方道路形状、学校、信号灯、施工或其他危险，提醒驾驶者注意。", True, "附表中的警告标志用于预告弯道、道口、学校、施工及其他危险。", 37, ["traffic_signs", "warning_signs"]),
        new_question("q_0626", "道路上的导流带是为了安全、顺畅地引导交通而设置的车辆不能驶入区域。", True, "指示标示中的导流带属于车辆无法通过的区域。", 39, ["road_markings", "traffic_rules"]),
        new_question("q_0627", "普通汽车是指不属于大型、中型、大型特殊、两轮摩托车或小型特殊汽车等类别的汽车。", True, "附表按照道路交通法列出了普通汽车与其他车辆种类的区分。", 40, ["vehicle_types", "license"]),
    ]

    existing_ids = {question["id"] for question in questions}
    added_questions = [question for question in additions if question["id"] not in existing_ids]
    questions.extend(added_questions)
    QUESTION_PATH.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Removed/kept absent {len(removed_ids)} questions, added {len(added_questions)} questions; total {len(questions)}")


if __name__ == "__main__":
    main()
