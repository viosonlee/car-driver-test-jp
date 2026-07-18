<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { db } from '../db';
import { useExamEngine } from '../stores/examEngine';
import { migrateLegacyErrorBookRecords } from '../stores/errorBook';
import { migrateAnswerRecord } from '../utils/questionIds';

const router = useRouter();
const { initExam } = useExamEngine();
const practicedCount = ref(0);
const errorCount = ref(0);
const lastExamScore = ref<number | null>(null);

onMounted(async () => {
  await migrateLegacyErrorBookRecords();
  try {
    const progress = JSON.parse(localStorage.getItem('study-progress-v1') || 'null');
    practicedCount.value = progress?.answers ? Object.keys(migrateAnswerRecord(progress.answers)).length : 0;
  } catch {
    practicedCount.value = 0;
  }

  errorCount.value = await db.errorBook.count();
  const latestExam = await db.examHistory.orderBy('date').last();
  lastExamScore.value = latestExam?.score ?? null;
});

const startExam = async () => {
  await initExam();
  router.push('/exam');
};

const goToReview = () => {
  router.push('/review');
};
</script>

<template>
  <div class="home-container">
    <div class="stats-card">
      <h2>学习进度</h2>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="value">{{ practicedCount }}</span>
          <span class="label">已练习题目</span>
        </div>
        <div class="stat-item">
          <span class="value">{{ errorCount }}</span>
          <span class="label">错题本</span>
        </div>
        <div class="stat-item">
          <span class="value">{{ lastExamScore === null ? '--' : `${lastExamScore}分` }}</span>
          <span class="label">上次模拟考</span>
        </div>
      </div>
    </div>

    <div class="action-buttons">
      <button class="study-btn" @click="router.push('/study')">
        <span class="icon">📖</span>
        <div class="btn-text">
          <span class="title">自由练习 (学习模式)</span>
          <span class="subtitle">无倒计时，答题后即时查看权威解析</span>
        </div>
      </button>

      <button class="primary-btn" @click="startExam">
        <span class="icon">⏱️</span>
        <div class="btn-text">
          <span class="title">外免切替知识确认模拟</span>
          <span class="subtitle">30分钟 · 50道判断题 · 45题合格</span>
        </div>
      </button>

      <button class="secondary-btn" @click="goToReview">
        <span class="icon">🧠</span>
        <div class="btn-text">
          <span class="title">弱点复习 (SRS)</span>
          <span class="subtitle">基于记忆曲线的智能复习</span>
        </div>
      </button>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stats-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.stats-card h2 {
  margin-top: 0;
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item .value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #4b6cb7;
}

.stat-item .label {
  font-size: 0.8rem;
  color: #777;
  margin-top: 4px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

button {
  display: flex;
  align-items: center;
  border: none;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: left;
}

button:active {
  transform: scale(0.98);
}

.icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.btn-text {
  display: flex;
  flex-direction: column;
}

.btn-text .title {
  font-size: 1.1rem;
  font-weight: 600;
}

.btn-text .subtitle {
  font-size: 0.85rem;
  opacity: 0.9;
  margin-top: 4px;
}

.primary-btn {
  background: linear-gradient(135deg, #FF6B6B 0%, #EE5D5D 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.study-btn {
  background: linear-gradient(135deg, #42b883 0%, #35495e 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(66, 184, 131, 0.3);
}

.secondary-btn {
  background: white;
  color: #333;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.secondary-btn .subtitle {
  color: #777;
}
</style>
