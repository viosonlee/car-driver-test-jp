<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import allQuestions from '../assets/data/all_questions.json';
import type { Question } from '../db';
import { recordQuestionResult } from '../stores/errorBook';
import SwipeCard from '../components/SwipeCard.vue';

/**
 * 练习模式（滑卡交互）：
 * - 每轮从全部题库随机洗牌，答过的本轮不再出现
 * - 答对：卡片右滑/点击飞出屏幕，自动进入下一题
 * - 答错：卡片左滑后抖动回弹，下方显示解析，手动进入下一题
 * - 一轮全部练完 → 统计页 → 开始第二轮重新洗牌
 */
const router = useRouter();
const STORAGE_KEY = 'study-progress-v2';
const all = allQuestions as Question[];

interface Progress {
  round: number;
  remainingIds: string[];
  answers: Record<string, boolean>; // 累计作答记录（供进度统计）
  roundStats?: { total: number; correct: number };
}
const shuffle = <T,>(arr: T[]): T[] => {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

const loadProgress = (): Progress => {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    if (saved && Array.isArray(saved.remainingIds)) {
      const valid = saved.remainingIds.filter((id: string) => all.some(q => q.id === id));
      return {
        round: saved.round || 1,
        remainingIds: valid,
        answers: saved.answers || {},
        roundStats: saved.roundStats || { total: 0, correct: 0 }
      };
    }
  } catch { /* ignore */ }
  return { round: 1, remainingIds: shuffle(all.map(q => q.id)), answers: {}, roundStats: { total: 0, correct: 0 } };
};

const progress = ref<Progress>(loadProgress());
const locked = ref(false);          // 已判定、等待离开当前卡
const showWrongPanel = ref(false);
const roundFinished = ref(false);
const cardRef = ref<InstanceType<typeof SwipeCard> | null>(null);

const remainingQuestions = computed(() =>
  progress.value.remainingIds
    .map(id => all.find(q => q.id === id))
    .filter((q): q is Question => Boolean(q))
);
const currentQ = computed(() => remainingQuestions.value[0]);
const doneTotal = computed(() => Object.keys(progress.value.answers).length);
const roundStats = computed(() => progress.value.roundStats || { total: 0, correct: 0 });

const persist = () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress.value));
};

const handleAnswer = async (value: boolean) => {
  if (!currentQ.value || locked.value) return;
  locked.value = true;
  const correct = value === currentQ.value.answer;
  progress.value.answers[currentQ.value.id] = value;
  const stats = progress.value.roundStats || (progress.value.roundStats = { total: 0, correct: 0 });
  stats.total++;
  if (correct) stats.correct++;

  await recordQuestionResult(currentQ.value.id, correct);

  if (correct) {
    // 卡片飞出屏幕 → 自动下一题
    cardRef.value?.flyOut(value ? 'right' : 'left');
    window.setTimeout(() => advance(), 320);
  } else {
    // 抖动回弹 → 显示解析，手动下一题
    cardRef.value?.shakeAndRevert();
    showWrongPanel.value = true;
  }
  persist();
};

const advance = () => {
  progress.value.remainingIds.shift();
  locked.value = false;
  showWrongPanel.value = false;
  if (!progress.value.remainingIds.length) roundFinished.value = true;
  persist();
};

const startNextRound = () => {
  progress.value.round++;
  progress.value.remainingIds = shuffle(all.map(q => q.id));
  progress.value.roundStats = { total: 0, correct: 0 };
  roundFinished.value = false;
  persist();
};
</script>

<template>
  <div class="study-container">
    <header class="study-header">
      <button class="back-btn" @click="router.push('/')">← 返回</button>
      <div class="progress">
        第 {{ progress.round }} 轮 · 剩余 {{ remainingQuestions.length }} 题 · 已练 {{ doneTotal }}
      </div>
    </header>

    <!-- 答题中 -->
    <template v-if="currentQ && !roundFinished">
      <SwipeCard
        ref="cardRef"
        :key="currentQ.id"
        :question="currentQ"
        :disabled="locked"
        :hint="`○=对 ✕=错`"
        @answer="handleAnswer"
      >
        <template #below>
          <!-- 错误解析面板 -->
          <div v-if="showWrongPanel" class="wrong-panel">
            <strong>⚠️ 回答错误</strong>
            <p>正确答案：{{ currentQ.answer ? '○ 正确' : '✕ 错误' }}</p>
            <p class="exp-text">{{ currentQ.explanation }}</p>
            <button class="primary-btn" @click="advance">下一题 →</button>
          </div>
          <div v-else-if="locked" class="waiting-tip">正在进入下一题…</div>
        </template>
      </SwipeCard>

      <p class="gesture-tip">👉 右滑或点「正确」＝ 判为正确 · 左滑或点「错误」＝ 判为错误</p>
    </template>

    <!-- 一轮完成 -->
    <div v-else-if="roundFinished" class="round-done">
      <h2>🎉 第 {{ progress.round }} 轮练习完成！</h2>
      <p>本轮 {{ roundStats.total }} 题 · 答对 {{ roundStats.correct }} 题<span v-if="roundStats.total">（{{ Math.round(roundStats.correct / roundStats.total * 100) }}%）</span></p>
      <p class="sub-tip">第二轮将重新随机打乱全部题目</p>
      <button class="primary-btn big" @click="startNextRound">开始第 {{ progress.round + 1 }} 轮</button>
      <button class="ghost-btn" @click="router.push('/')">返回首页</button>
    </div>

    <!-- 异常兜底 -->
    <div v-else class="empty-state">
      <p>题库加载异常，请返回首页重试。</p>
      <button class="primary-btn" @click="router.push('/')">返回首页</button>
    </div>
  </div>
</template>

<style scoped>
.study-container { display: flex; flex-direction: column; height: 100%; }
.study-header {
  display: flex; justify-content: space-between; align-items: center;
  padding-bottom: .8rem; border-bottom: 1px solid #eee; margin-bottom: 1rem;
}
.back-btn { background: transparent; border: none; color: #4b6cb7; font-size: 1rem; cursor: pointer; }
.progress { color: #666; font-size: .9rem; }

.wrong-panel {
  margin-top: 1rem; padding: 1rem;
  border-left: 4px solid #ff6b6b; background: #fff5f5; border-radius: 0 10px 10px 0;
  animation: slide-up .25s ease-out;
}
.wrong-panel strong { color: #d14d4d; display: block; margin-bottom: .3rem; }
.wrong-panel p { margin: .25rem 0; line-height: 1.5; }
.exp-text { color: #444; }
.waiting-tip { margin-top: 1rem; text-align: center; color: #999; font-size: .9rem; }

.gesture-tip { text-align: center; color: #aaa; font-size: .82rem; margin-top: .8rem; }

.primary-btn {
  margin-top: .8rem; border: 0; border-radius: 22px; padding: 10px 26px;
  background: #4b6cb7; color: white; font-weight: 600; cursor: pointer;
}
.primary-btn.big { font-size: 1.05rem; padding: 12px 34px; }
.ghost-btn {
  margin-top: .6rem; border: 1px solid #ddd; border-radius: 22px; padding: 9px 26px;
  background: white; color: #666; cursor: pointer;
}

.round-done, .empty-state {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: .4rem;
  background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 6px 20px rgba(0,0,0,.06);
}
.round-done h2 { margin: 0 0 .4rem; }
.round-done p, .empty-state p { margin: .15rem 0; color: #555; }
.sub-tip { color: #999 !important; font-size: .88rem; }

@keyframes slide-up { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
</style>
