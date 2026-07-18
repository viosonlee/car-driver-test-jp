<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useExamEngine } from '../stores/examEngine';
import { resolveAssetUrl } from '../utils/assetUrl';

const router = useRouter();
const { 
  examState, 
  timeRemaining, 
  initExam, 
  finishExam, 
  nextQuestion, 
  prevQuestion, 
  setAnswer, 
  formatTime 
} = useExamEngine();

onMounted(() => {
  if (!examState.isActive && !examState.isFinished) {
    initExam();
  }
});

const currentQ = computed(() => examState.questions[examState.currentIndex]);

const submitExam = () => {
  if (confirm('确定要提前交卷吗？')) {
    finishExam();
  }
};

const goHome = () => {
  router.push('/');
};

const handleAnswer = (val: boolean) => {
  setAnswer(currentQ.value.id, val);
  // Auto advance on single choice
  if (currentQ.value.type === 'true_false') {
    setTimeout(() => {
      nextQuestion();
    }, 300);
  }
};

const handleHazardAnswer = (index: number, val: boolean) => {
  const currentAns = examState.answers[currentQ.value.id] || [null, null, null];
  currentAns[index] = val;
  setAnswer(currentQ.value.id, [...currentAns]);
};
</script>

<template>
  <div class="exam-container" v-if="currentQ && !examState.isFinished">
    <header class="exam-header">
      <div class="progress">外免切替: {{ examState.currentIndex + 1 }} / {{ examState.questions.length }}</div>
      <div class="timer" :class="{ 'timer-danger': timeRemaining < 300000 }">
        ⏱ {{ formatTime(timeRemaining) }}
      </div>
      <button class="submit-btn" @click="submitExam">交卷</button>
    </header>

    <div class="question-card">
      <div class="q-type-badge">{{ currentQ.type === 'hazard_prediction' ? '危险预测题 (2分)' : '单选题 (1分)' }}</div>
      
      <!-- Question Image -->
      <div v-if="currentQ.image_url || currentQ.scenario" class="question-image">
        <img v-if="currentQ.image_url" :src="resolveAssetUrl(currentQ.image_url)" alt="题目图片" />
        <p v-if="currentQ.scenario" class="scenario-text">{{ currentQ.scenario }}</p>
      </div>

      <div class="q-text">
        <p class="cn">{{ currentQ.question }}</p>
        <p class="jp" v-if="currentQ.question_jp">{{ currentQ.question_jp }}</p>
      </div>

      <!-- True/False Options -->
      <div class="options-container" v-if="currentQ.type === 'true_false' || !currentQ.sub_questions?.length">
        <button 
          class="option-btn" 
          :class="{ selected: examState.answers[currentQ.id] === true }"
          @click="handleAnswer(true)"
        >
          <span class="icon">⭕️</span> 正确
        </button>
        <button 
          class="option-btn" 
          :class="{ selected: examState.answers[currentQ.id] === false }"
          @click="handleAnswer(false)"
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
              :class="{ selected: examState.answers[currentQ.id]?.[idx] === true }"
              @click="handleHazardAnswer(idx, true)"
            >⭕️</button>
            <button 
              class="option-btn" 
              :class="{ selected: examState.answers[currentQ.id]?.[idx] === false }"
              @click="handleHazardAnswer(idx, false)"
            >❌</button>
          </div>
        </div>
      </div>
    </div>

    <footer class="exam-footer">
      <button :disabled="examState.currentIndex === 0" @click="prevQuestion">上一题</button>
      <button v-if="examState.currentIndex < examState.questions.length - 1" @click="nextQuestion">下一题</button>
      <button v-else class="finish-btn" @click="finishExam">完成考试</button>
    </footer>
  </div>

  <div class="result-container" v-else-if="examState.isFinished">
    <h2>考试结束</h2>
    <div class="score-display">
      <span class="score">{{ examState.score }}</span>
      <span class="max-score">/ 50</span>
    </div>
    <p class="result-msg" v-if="examState.score >= 45">🎉 恭喜！您已达到外免切替知识确认及格线（45题以上）。</p>
    <p class="result-msg danger" v-else>😢 很遗憾，未达到 45 题及格线，请继续努力！</p>
    <button class="primary-btn" @click="goHome">返回主页</button>
  </div>
</template>

<style scoped>
.exam-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
  margin-bottom: 1rem;
}

.timer {
  font-weight: bold;
  color: #4b6cb7;
  font-variant-numeric: tabular-nums;
}

.timer-danger {
  color: #FF6B6B;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.submit-btn {
  background: transparent;
  border: 1px solid #FF6B6B;
  color: #FF6B6B;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 0.85rem;
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

.question-image {
  margin-bottom: 1rem;
}

.question-image img {
  display: block;
  width: auto;
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  max-height: 360px;
  object-fit: contain;
  margin-left: auto;
  margin-right: auto;
}

.scenario-text {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
  font-style: italic;
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

.option-btn:active {
  transform: scale(0.98);
}

.option-btn.selected {
  border-color: #4b6cb7;
  background: #f0f4f8;
}

.mini .option-btn {
  padding: 0.5rem;
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

.exam-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.exam-footer button {
  padding: 12px 24px;
  border: none;
  background: #e2e8f0;
  color: #333;
  border-radius: 8px;
  font-weight: 500;
}

.exam-footer button:disabled {
  opacity: 0.5;
}

.finish-btn {
  background: #4b6cb7 !important;
  color: white !important;
}

.result-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.score-display {
  margin: 2rem 0;
}

.score {
  font-size: 4rem;
  font-weight: 800;
  color: #4b6cb7;
}

.max-score {
  font-size: 1.5rem;
  color: #999;
}

.result-msg {
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.result-msg.danger {
  color: #FF6B6B;
}

.primary-btn {
  background: #4b6cb7;
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: 24px;
  font-size: 1.1rem;
}
</style>
