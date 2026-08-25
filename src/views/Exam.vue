<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useExamEngine } from '../stores/examEngine';
import SwipeCard from '../components/SwipeCard.vue';

const router = useRouter();
const {
  examState,
  timeRemaining,
  initExam,
  finishExam,
  nextQuestion,
  setAnswer,
  formatTime
} = useExamEngine();

const cardRef = ref<InstanceType<typeof SwipeCard> | null>(null);
const advancing = ref(false); // 本题已作答、卡片飞出中，锁定输入

onMounted(() => {
  if (!examState.isActive && !examState.isFinished) {
    initExam();
  }
});

const currentQ = computed(() => examState.questions[examState.currentIndex]);
const answeredCount = computed(
  () => examState.questions.filter(q => examState.answers[q.id] !== undefined).length
);

// 考试模式不即时判对错：按滑动方向飞出后自动进入下一题（最后一题则交卷）
const handleAnswer = (val: boolean) => {
  if (advancing.value) return;
  advancing.value = true;
  setAnswer(currentQ.value.id, val);
  cardRef.value?.flyOut(val ? 'right' : 'left');
  setTimeout(() => {
    advancing.value = false;
    nextQuestion(); // 内部会在最后一题时调用 finishExam
  }, 320);
};

const submitExam = () => {
  if (confirm(`确定要提前交卷吗？（已作答 ${answeredCount.value} / ${examState.questions.length} 题）`)) {
    finishExam();
  }
};

const goHome = () => {
  router.push('/');
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

    <SwipeCard
      ref="cardRef"
      :key="currentQ.id"
      :question="currentQ"
      :hint="`第 ${examState.currentIndex + 1} 题`"
      class="exam-card"
      @answer="handleAnswer"
    >
      <template #below>
        <p class="swipe-tip">左右滑动卡片作答（右滑=正确，左滑=错误），也可点击按钮</p>
      </template>
    </SwipeCard>

    <footer class="exam-footer">
      <span class="answered-count">已答 {{ answeredCount }} / {{ examState.questions.length }}</span>
      <button class="finish-btn" @click="submitExam">提前交卷</button>
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

.progress {
  font-size: 0.9rem;
  color: #666;
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
  cursor: pointer;
}

.exam-card {
  flex: 1;
  overflow-y: auto;
}

.swipe-tip {
  text-align: center;
  font-size: 0.8rem;
  color: #aaa;
  margin: 0.6rem 0 0;
}

.exam-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.answered-count {
  font-size: 0.85rem;
  color: #888;
  font-variant-numeric: tabular-nums;
}

.finish-btn {
  padding: 10px 24px;
  border: none;
  background: #4b6cb7;
  color: white;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
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
  cursor: pointer;
}
</style>
