<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import allQuestions from '../assets/data/all_questions.json';
import { type Question } from '../db';
import { recordQuestionResult } from '../stores/errorBook';

const router = useRouter();
const STORAGE_KEY = 'study-progress-v1';
const questionMap = new Map((allQuestions as Question[]).map(question => [question.id, question]));
const savedProgress = (() => {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
  } catch {
    return null;
  }
})();
const savedQuestions = Array.isArray(savedProgress?.questionIds)
  ? savedProgress.questionIds.map((id: string) => questionMap.get(id)).filter(Boolean) as Question[]
  : [];
const questions = savedQuestions.length === allQuestions.length
  ? savedQuestions
  : [...allQuestions].sort(() => 0.5 - Math.random()) as Question[];
const currentIndex = ref(Math.min(Math.max(savedProgress?.currentIndex || 0, 0), questions.length - 1));
const currentQ = computed(() => questions[currentIndex.value]);

// User's answer state for current question
const answers = ref<Record<string, any>>(savedProgress?.answers || {});
const currentAns = computed({
  get: () => answers.value[currentQ.value.id] ?? null,
  set: value => { answers.value[currentQ.value.id] = value; }
});
const hasAnswered = computed(() => {
  const answer = currentAns.value;
  return currentQ.value.sub_questions?.length
    ? Array.isArray(answer) && answer.every(value => value !== null)
    : typeof answer === 'boolean';
});

watch([currentIndex, answers], () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    questionIds: questions.map(question => question.id),
    currentIndex: currentIndex.value,
    answers: answers.value
  }));
}, { deep: true, immediate: true });

const goHome = () => {
  router.push('/');
};

const nextQuestion = () => {
  if (currentIndex.value < questions.length - 1) {
    currentIndex.value++;
  } else {
    alert('已经是最后一题了！');
  }
};

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  }
};

const handleAnswer = async (val: boolean) => {
  if (hasAnswered.value) return; // Prevent changing answer in study mode
  currentAns.value = val;
  await recordQuestionResult(currentQ.value.id, val === currentQ.value.answer);
};

const handleHazardAnswer = async (index: number, val: boolean) => {
  if (hasAnswered.value) return;
  if (!Array.isArray(currentAns.value)) {
    currentAns.value = Array(currentQ.value.sub_questions?.length || 0).fill(null);
  }
  currentAns.value[index] = val;
  if (currentAns.value.every((answer: boolean | null) => answer !== null)) {
    const correct = currentQ.value.sub_questions?.every((subQuestion, subIndex) => subQuestion.answer === currentAns.value[subIndex]) ?? false;
    await recordQuestionResult(currentQ.value.id, correct);
  }
};
</script>

<template>
  <div class="study-container" v-if="currentQ">
    <header class="study-header">
      <button class="back-btn" @click="goHome">← 返回</button>
      <div class="progress">学习模式: {{ currentIndex + 1 }} / {{ questions.length }}</div>
    </header>

    <div class="question-card">
      <div class="q-type-badge">{{ currentQ.type === 'hazard_prediction' ? '危险预测题' : '单选题' }}</div>
      
      <!-- Hazard Prediction Image -->
      <div v-if="currentQ.type === 'hazard_prediction' && currentQ.image_url" class="hazard-image">
        <img :src="currentQ.image_url" alt="Hazard Scenario" />
        <p class="scenario-text">{{ currentQ.scenario }}</p>
      </div>

      <div class="q-text">
        <p class="cn">{{ currentQ.question }}</p>
        <p class="jp" v-if="currentQ.question_jp">{{ currentQ.question_jp }}</p>
      </div>

      <!-- True/False Options -->
      <div class="options-container" v-if="currentQ.type === 'true_false' || !currentQ.sub_questions?.length">
        <button 
          class="option-btn" 
          :class="{ 
            selected: currentAns === true, 
            correct: hasAnswered && currentQ.answer === true,
            wrong: hasAnswered && currentAns === true && currentQ.answer !== true
          }"
          @click="handleAnswer(true)"
          :disabled="hasAnswered"
        >
          <span class="icon">⭕️</span> 正确
        </button>
        <button 
          class="option-btn" 
          :class="{ 
            selected: currentAns === false,
            correct: hasAnswered && currentQ.answer === false,
            wrong: hasAnswered && currentAns === false && currentQ.answer !== false
          }"
          @click="handleAnswer(false)"
          :disabled="hasAnswered"
        >
          <span class="icon">❌</span> 错误
        </button>
      </div>

      <!-- Hazard Sub-questions -->
      <div class="hazard-options" v-if="currentQ.type === 'hazard_prediction' && currentQ.sub_questions">
        <div class="sub-q" v-for="(sq, idx) in currentQ.sub_questions" :key="idx">
          <p class="sub-text">{{ sq.question }}</p>
          <div class="options-container mini">
            <button 
              class="option-btn" 
              :class="{ 
                selected: currentAns?.[idx] === true,
                correct: hasAnswered && sq.answer === true,
                wrong: hasAnswered && currentAns?.[idx] === true && sq.answer !== true
              }"
              @click="handleHazardAnswer(idx, true)"
              :disabled="hasAnswered"
            >⭕️</button>
            <button 
              class="option-btn" 
              :class="{ 
                selected: currentAns?.[idx] === false,
                correct: hasAnswered && sq.answer === false,
                wrong: hasAnswered && currentAns?.[idx] === false && sq.answer !== false
              }"
              @click="handleHazardAnswer(idx, false)"
              :disabled="hasAnswered"
            >❌</button>
          </div>
          <div v-if="hasAnswered" class="explanation-box small">
            解析: {{ sq.explanation }}
          </div>
        </div>
      </div>

      <!-- Explanation Box -->
      <div v-if="hasAnswered && currentQ.type === 'true_false'" class="explanation-box" :class="{ 'is-correct': currentAns === currentQ.answer }">
        <div class="status-indicator">
          {{ currentAns === currentQ.answer ? '🎉 回答正确' : '⚠️ 回答错误' }}
        </div>
        <p class="exp-text">{{ currentQ.explanation }}</p>
      </div>
    </div>

    <footer class="study-footer">
      <button :disabled="currentIndex === 0" @click="prevQuestion">上一题</button>
      <button :disabled="currentIndex === questions.length - 1" @click="nextQuestion" :class="{ 'highlight-next': hasAnswered }">下一题</button>
    </footer>
  </div>
</template>

<style scoped>
.study-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.study-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
  margin-bottom: 1rem;
}

.back-btn {
  background: transparent;
  border: none;
  color: #4b6cb7;
  font-size: 1rem;
  cursor: pointer;
}

.progress {
  color: #666;
  font-size: 0.9rem;
}

.question-card {
  flex: 1;
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  overflow-y: auto;
}

.q-type-badge {
  display: inline-block;
  background: #eee;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 1rem;
}

.q-text .cn {
  font-size: 1.15rem;
  font-weight: 500;
  color: #333;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.q-text .jp {
  font-size: 0.95rem;
  color: #888;
  line-height: 1.4;
  margin-bottom: 1.5rem;
}

.options-container {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.option-btn {
  flex: 1;
  padding: 1rem;
  border: 2px solid #eaeaea;
  border-radius: 8px;
  background: white;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-btn:active:not(:disabled) {
  transform: scale(0.98);
}

.option-btn:disabled {
  cursor: default;
}

.option-btn.selected {
  border-color: #4b6cb7;
  background: #f0f4f8;
}

.option-btn.correct {
  border-color: #42b883;
  background: #e6f6ef;
  color: #2c8a5f;
}

.option-btn.wrong {
  border-color: #ff6b6b;
  background: #ffeded;
  color: #d14d4d;
}

.explanation-box {
  margin-top: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-left: 4px solid #4b6cb7;
  border-radius: 0 8px 8px 0;
  animation: fadeIn 0.3s ease-out;
}

.explanation-box.is-correct {
  border-left-color: #42b883;
}

.explanation-box.small {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  padding: 0.8rem;
}

.status-indicator {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.is-correct .status-indicator {
  color: #42b883;
}

.exp-text {
  color: #444;
  line-height: 1.5;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

.hazard-image img {
  width: 100%;
  border-radius: 8px;
  max-height: 200px;
  object-fit: cover;
  margin-bottom: 0.5rem;
}

.scenario-text {
  font-style: italic;
  color: #666;
  font-size: 0.9rem;
}

.sub-q {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px dashed #eee;
}

.sub-text {
  font-size: 1rem;
  margin-bottom: 0.8rem;
}

.mini .option-btn {
  padding: 0.5rem;
}

.study-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.study-footer button {
  padding: 12px 24px;
  border: none;
  background: #e2e8f0;
  color: #333;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s;
}

.study-footer button:disabled {
  opacity: 0.5;
}

.study-footer button.highlight-next {
  background: #4b6cb7;
  color: white;
  animation: pulse-soft 2s infinite;
}

@keyframes pulse-soft {
  0% { box-shadow: 0 0 0 0 rgba(75, 108, 183, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(75, 108, 183, 0); }
  100% { box-shadow: 0 0 0 0 rgba(75, 108, 183, 0); }
}
</style>
