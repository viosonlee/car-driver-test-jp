const fs = require('fs');
const path = require('path');
const dir = path.join(__dirname, '../src/assets/data');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.json') && (f.startsWith('gen_') || f === 'questions_batch_1.json'));

let all = [];
files.forEach(f => {
  try {
    const d = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
    all = all.concat(d);
  } catch(e) {
    console.error('Error parsing ' + f);
  }
});

// Remove duplicates and ensure unique IDs
const finalQuestions = [];
const seenQs = new Set();
all.forEach((q, i) => {
  if (!seenQs.has(q.question)) {
    q.id = 'q_' + String(finalQuestions.length).padStart(4, '0');
    finalQuestions.push(q);
    seenQs.add(q.question);
  }
});

fs.writeFileSync(path.join(dir, 'all_questions.json'), JSON.stringify(finalQuestions, null, 2));
console.log('Total questions merged: ' + finalQuestions.length);
