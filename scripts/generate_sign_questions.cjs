const fs = require('fs');
const path = require('path');

const signsData = [
  {
    id: 'stop',
    image: '/signs/stop.svg',
    true_q: '这个标志表示车辆必须在停止线前（没有停止线则在路口前）暂时停车。',
    true_jp: 'この標識は、車両が停止線の直前（停止線がない場合は交差点の直前）で一時停止しなければならないことを示している。',
    false_q: '这个标志表示前方有危险，车辆需要减速慢行，但不需要完全停车。',
    false_jp: 'この標識は、前方に危険があるため徐行しなければならないが、完全に停止する必要はないことを示している。',
    exp: '红色的倒三角且写着「止まれ」是“一时停止”标志。车辆必须完全停止，确认安全后方可通行。'
  },
  {
    id: 'no_entry',
    image: '/signs/no_entry.svg',
    true_q: '这个标志表示车辆（包含自行车）禁止从该方向驶入。',
    true_jp: 'この標識は、車両（自転車を含む）がこの方向から進入してはならないことを示している。',
    false_q: '这个标志表示仅禁止汽车驶入，自行车可以正常驶入。',
    false_jp: 'この標識は、自動車の進入のみを禁止しており、自転車は通常通り進入できることを示している。',
    exp: '红底白横杠是“进入禁止”标志，通常设置在单行道的出口处，所有车辆（除非有辅助标志特许）均不得驶入。'
  },
  {
    id: 'one_way',
    image: '/signs/one_way.svg',
    true_q: '这个标志表示该道路为单行道，车辆只能按照箭头指示的方向行驶。',
    true_jp: 'この標識は、この道路が一方通行であり、車両は矢印の方向にしか進行できないことを示している。',
    false_q: '这个标志表示前方只能直行，禁止左转或右转。',
    false_jp: 'この標識は、前方は直進のみ可能であり、左折や右折が禁止されていることを示している。',
    exp: '蓝底白箭头是“一方通行”（单行道）标志。注意不要与“指定方向外进行禁止”（仅允许直行）的圆形蓝底箭头标志混淆。'
  },
  {
    id: 'speed_limit_50',
    image: '/signs/speed_limit_50.svg',
    true_q: '这个标志表示该路段的最高速度限制为 50km/h。',
    true_jp: 'この標識は、この区間の最高速度が 50km/h であることを示している。',
    false_q: '这个标志表示该路段的最低速度限制为 50km/h。',
    false_jp: 'この標識は、この区間の最低速度が 50km/h であることを示している。',
    exp: '红圈内带数字表示“最高速度”限制。如果是最低速度限制，数字下方会有一条横线。'
  },
  {
    id: 'no_parking',
    image: '/signs/no_parking.svg',
    true_q: '这个标志表示禁止停车，但允许上下客或装卸货物等短时间的驻车。',
    true_jp: 'この標識は、駐車を禁止しているが、人の乗降や荷物の積み下ろしなどの短時間の停車は認められている。',
    false_q: '这个标志表示绝对禁止任何形式的停车和驻车。',
    false_jp: 'この標識は、いかなる形の駐車および停車も絶対に禁止している。',
    exp: '蓝底红圈加一条斜杠是“禁止停车”（駐車禁止），允许短时间驻车（停車）。如果是红圈加红叉（两条斜杠），才是“驻停车禁止”。'
  },
  {
    id: 'no_stopping',
    image: '/signs/no_stopping.svg',
    true_q: '这个标志表示该地点禁止停车和驻车（驻停车禁止）。',
    true_jp: 'この標識は、この場所での駐車および停車を禁止している（駐停車禁止）。',
    false_q: '这个标志表示禁止车辆通行。',
    false_jp: 'この標識は、車両の通行を禁止している。',
    exp: '蓝底红圈加红叉表示“驻停车禁止”（いかなる停車・駐車も禁止）。'
  },
  {
    id: 'pedestrian_crossing',
    image: '/signs/pedestrian_crossing.svg',
    true_q: '这个标志表示前方有人行横道，驾驶员应减速注意行人。',
    true_jp: 'この標識は、前方に横断歩道があることを示しており、運転者は減速して歩行者に注意しなければならない。',
    false_q: '这个标志表示仅允许行人通行，禁止车辆驶入。',
    false_jp: 'この標識は、歩行者の通行のみを許可し、車両の進入を禁止している。',
    exp: '蓝底白三角形内有行人，是“人行横道”的指示标志。'
  },
  {
    id: 'bicycle_crossing',
    image: '/signs/bicycle_crossing.svg',
    true_q: '这个标志表示前方有自行车横道。',
    true_jp: 'この標識は、前方に自転車横断帯があることを示している。',
    false_q: '这个标志表示该道路为自行车专用道。',
    false_jp: 'この標識は、この道路が自転車専用道路であることを示している。',
    exp: '蓝底白三角形内有自行车，是“自行车横道”的指示标志。'
  }
];

const newQuestions = [];
let idCounter = Date.now();

signsData.forEach(s => {
  // Add correct question
  newQuestions.push({
    id: `q_sign_img_${idCounter++}`,
    type: 'true_false',
    question: s.true_q,
    question_jp: s.true_jp,
    answer: true,
    explanation: s.exp,
    image_url: s.image,
    tags: ['traffic_signs', 'image_recognition']
  });
  
  // Add incorrect question
  newQuestions.push({
    id: `q_sign_img_${idCounter++}`,
    type: 'true_false',
    question: s.false_q,
    question_jp: s.false_jp,
    answer: false,
    explanation: s.exp,
    image_url: s.image,
    tags: ['traffic_signs', 'image_recognition']
  });
});

const dataPath = path.join(__dirname, '../src/assets/data/all_questions.json');
const currentData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// Inject new questions
const mergedData = [...newQuestions, ...currentData];
fs.writeFileSync(dataPath, JSON.stringify(mergedData, null, 2));

console.log(`Added ${newQuestions.length} image recognition questions. Total is now ${mergedData.length}.`);
