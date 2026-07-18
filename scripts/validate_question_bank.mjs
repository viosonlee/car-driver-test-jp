import fs from 'node:fs';
import path from 'node:path';

const questionPath = path.resolve('src/assets/data/all_questions.json');
const questions = JSON.parse(fs.readFileSync(questionPath, 'utf8'));
const errors = [];
const warnings = [];

const byId = new Map();
const byImage = new Map();

for (const question of questions) {
  if (!question.id) errors.push('A question is missing id');
  if (byId.has(question.id)) errors.push(`Duplicate id: ${question.id}`);
  byId.set(question.id, question);

  if (question.type === 'true_false') {
    if (typeof question.answer !== 'boolean') errors.push(`${question.id}: true_false answer must be boolean`);
    if (!question.question) errors.push(`${question.id}: true_false question text is missing`);
  } else if (question.type === 'hazard_prediction') {
    if (!question.scenario || !Array.isArray(question.sub_questions) || question.sub_questions.length === 0) {
      errors.push(`${question.id}: hazard_prediction requires scenario and sub_questions`);
    }
  } else {
    errors.push(`${question.id}: unsupported type ${question.type}`);
  }

  if (!Array.isArray(question.tags)) errors.push(`${question.id}: tags must be an array`);

  if (question.image_url) {
    const relativePath = question.image_url.replace(/^\/+/, '');
    if (!/^(?:https?:|data:|blob:)/i.test(question.image_url)) {
      const assetPath = path.resolve('public', relativePath);
      if (!fs.existsSync(assetPath)) errors.push(`${question.id}: missing image ${question.image_url}`);
    }
    if (!question.question_jp) errors.push(`${question.id}: image question is missing question_jp`);
    const items = byImage.get(question.image_url) ?? [];
    items.push(question);
    byImage.set(question.image_url, items);
  }
}

for (const [imageUrl, items] of byImage) {
  const answers = items.map(item => item.answer).sort();
  if (items.length !== 2 || answers[0] !== false || answers[1] !== true) {
    errors.push(`${imageUrl}: expected one true and one false question, found ${items.length}`);
  }
  const sourced = items.every(item => item.tags.some(tag => tag.startsWith('source_page_')));
  if (!sourced && !imageUrl.includes('/mark_')) warnings.push(`${imageUrl}: missing source_page tag`);
}

const sourceCoverage = new Map();
for (const question of questions) {
  for (const tag of question.tags ?? []) {
    if (!tag.startsWith('source_page_')) continue;
    const page = tag.slice('source_page_'.length);
    sourceCoverage.set(page, (sourceCoverage.get(page) ?? 0) + 1);
  }
}

console.log(`Questions: ${questions.length}`);
console.log(`Image questions: ${[...byImage.values()].reduce((sum, items) => sum + items.length, 0)}`);
console.log(`Unique image assets: ${byImage.size}`);
console.log(`Source pages: ${[...sourceCoverage.keys()].sort((a, b) => Number(a) - Number(b)).join(', ')}`);

for (const warning of warnings) console.warn(`WARN ${warning}`);
if (errors.length) {
  for (const error of errors) console.error(`ERROR ${error}`);
  process.exitCode = 1;
} else {
  console.log('Question bank validation passed.');
}
