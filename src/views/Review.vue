<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import allQuestions from '../assets/data/all_questions.json';
import { db, type ErrorRecord, type Question } from '../db';
import { recordQuestionResult } from '../stores/errorBook';

const router = useRouter();
const questionMap = new Map((allQuestions as Question[]).map(question => [question.id, question]));
const records = ref<ErrorRecord[]>([]);
const currentIndex = ref(0);
const selectedAnswer = ref<boolean | null>(null);
const answered = ref(false);
const answerCorrect = ref(false);

const reviewItems = computed(() => records.value
  .map(record => ({ record, question: questionMap.get(record.questionId) }))
  .filter((item): item is { record: ErrorRecord; question: Question } => Boolean(item.question)));
const currentItem = computed(() => reviewItems.value[currentIndex.value]);

const loadRecords = async () => {
  records.value = await db.errorBook.orderBy('nextReviewDate').toArray();
  currentIndex.value = Math.min(currentIndex.value, Math.max(0, records.value.length - 1));
};

onMounted(loadRecords);

const answer = async (value: boolean) => {
  if (answered.value || !currentItem.value) return;
  selectedAnswer.value = value;
  answerCorrect.value = value === currentItem.value.question.answer;
  answered.value = true;
  await recordQuestionResult(currentItem.value.question.id, answerCorrect.value);
};

const next = async () => {
  await loadRecords();
  selectedAnswer.value = null;
  answered.value = false;
  answerCorrect.value = false;
  if (reviewItems.value.length && currentIndex.value < reviewItems.value.length - 1) currentIndex.value++;
};
</script>

<template>
  <div class="review-container">
    <header class="review-header">
      <button class="back-btn" @click="router.push('/')">← 返回</button>
      <h2>错题本</h2>
      <span class="count">{{ reviewItems.length }} 题</span>
    </header>

    <div v-if="currentItem" class="question-card">
      <div class="progress">{{ currentIndex + 1 }} / {{ reviewItems.length }} · 连续答对2次后移出</div>
      <!-- Question Image -->
      <div v-if="currentItem.question.image_url" class="question-image">
        <img :src="currentItem.question.image_url" alt="Question Image" />
      </div>
      <p class="question">{{ currentItem.question.question }}</p>
      <div class="options">
        <button :class="{ selected: selectedAnswer === true, correct: answered && currentItem.question.answer === true, wrong: answered && selectedAnswer === true && !answerCorrect }" :disabled="answered" @click="answer(true)">⭕ 正确</button>
        <button :class="{ selected: selectedAnswer === false, correct: answered && currentItem.question.answer === false, wrong: answered && selectedAnswer === false && !answerCorrect }" :disabled="answered" @click="answer(false)">❌ 错误</button>
      </div>
      <div v-if="answered" class="explanation">
        <strong>{{ answerCorrect ? '回答正确' : '回答错误' }}</strong>
        <p>{{ currentItem.question.explanation }}</p>
        <button class="primary-btn" @click="next">下一题</button>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>目前没有错题，继续保持！</p>
      <button class="primary-btn" @click="router.push('/')">返回首页</button>
    </div>
  </div>
</template>

<style scoped>
.review-container { display: flex; flex-direction: column; min-height: 100%; }
.review-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.review-header h2 { flex: 1; margin: 0; font-size: 1.2rem; }
.back-btn { border: 0; background: transparent; color: #4b6cb7; cursor: pointer; }
.count, .progress { color: #777; font-size: .9rem; }
.question-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,.05); }
.question-image { margin: 1rem 0; }
.question-image img { width: 100%; max-height: 200px; object-fit: cover; border-radius: 8px; }
.question { margin: 1.5rem 0; font-size: 1.15rem; line-height: 1.6; }
.options { display: flex; gap: 1rem; }
.options button { flex: 1; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 8px; background: white; font-size: 1rem; }
.options button.selected { border-color: #4b6cb7; }
.options button.correct { border-color: #42b883; background: #e6f6ef; }
.options button.wrong { border-color: #ff6b6b; background: #ffeded; }
.explanation { margin-top: 1.5rem; padding: 1rem; border-left: 4px solid #4b6cb7; background: #f8f9fa; }
.empty-state { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #777; }
.primary-btn { border: 0; border-radius: 20px; padding: 9px 24px; background: #4b6cb7; color: white; cursor: pointer; }
</style>
