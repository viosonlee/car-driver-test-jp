<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import allQuestions from '../assets/data/all_questions.json';
import { db, type ErrorRecord, type Question } from '../db';
import { migrateLegacyErrorBookRecords, recordQuestionResult, EBBINGHAUS_STAGES } from '../stores/errorBook';
import SwipeCard from '../components/SwipeCard.vue';

/**
 * 错题复习（滑卡交互，与练习模式一致）：
 * - 按艾宾浩斯曲线只出现「到期」的题目
 * - 答对：卡片飞出，按曲线推进下一复习间隔；走完全部阶段毕业移出错题本
 * - 答错：卡片抖动回弹，显示解析，回到第一阶段（5分钟后再练），手动进入下一题
 */
const router = useRouter();
const questionMap = new Map((allQuestions as Question[]).map(q => [q.id, q]));

const dueItems = ref<{ record: ErrorRecord; question: Question }[]>([]);
const pendingCount = ref(0); // 尚未到期的数量
const locked = ref(false);
const showWrongPanel = ref(false);

const cardRef = ref<InstanceType<typeof SwipeCard> | null>(null);

const currentItem = computed(() => dueItems.value[0]);
const currentStageLabel = computed(() => {
  const stage = currentItem.value?.record.stage ?? 0;
  return `记忆阶段 ${stage + 1}/${EBBINGHAUS_STAGES.length} · 下次间隔 ${EBBINGHAUS_STAGES[stage]?.label}`;
});

const loadDue = async () => {
  await migrateLegacyErrorBookRecords();
  const now = Date.now();
  const all: ErrorRecord[] = await db.errorBook.toArray();
  const due = all.filter(r => r.nextReviewDate <= now).sort((a, b) => a.nextReviewDate - b.nextReviewDate);
  pendingCount.value = all.length - due.length;
  dueItems.value = due
    .map(record => ({ record, question: questionMap.get(record.questionId) }))
    .filter((item): item is { record: ErrorRecord; question: Question } => Boolean(item.question));
};

onMounted(loadDue);

const handleAnswer = async (value: boolean) => {
  if (!currentItem.value || locked.value) return;
  locked.value = true;
  const correct = value === currentItem.value.question.answer;

  await recordQuestionResult(currentItem.value.question.id, correct);

  if (correct) {
    // 答对：卡片飞出屏幕，自动进入下一题
    cardRef.value?.flyOut(value ? 'right' : 'left');
    window.setTimeout(advance, 320);
  } else {
    // 答错：抖动回弹，下方显示解析，手动进入下一题
    cardRef.value?.shakeAndRevert();
    showWrongPanel.value = true;
  }
};

// 以数据库为准刷新到期列表（毕业的自然移除、答错的排到未来）
const advance = async () => {
  await loadDue();
  locked.value = false;
  showWrongPanel.value = false;
};
</script>

<template>
  <div class="review-container">
    <header class="review-header">
      <button class="back-btn" @click="router.push('/')">← 返回</button>
      <h2>错题复习</h2>
      <span class="count">到期 {{ dueItems.length }} 题<span v-if="pendingCount"> · 待定 {{ pendingCount }}</span></span>
    </header>

    <!-- 有到期题：滑卡作答 -->
    <template v-if="currentItem">
      <SwipeCard
        ref="cardRef"
        :key="currentItem.question.id"
        :question="currentItem.question"
        :disabled="locked"
        :hint="currentStageLabel"
        @answer="handleAnswer"
      >
        <template #below>
          <div v-if="showWrongPanel" class="wrong-panel">
            <strong>⚠️ 回答错误</strong>
            <p>正确答案：{{ currentItem.question.answer ? '○ 正确' : '✕ 错误' }}</p>
            <p class="exp-text">{{ currentItem.question.explanation }}</p>
            <p class="sub-tip">该题已重置到记忆第 1 阶段（5 分钟后重新出现）</p>
            <button class="primary-btn" @click="advance">下一题 →</button>
          </div>
          <div v-else-if="locked" class="waiting-tip">正在进入下一题…</div>
        </template>
      </SwipeCard>
      <p class="gesture-tip">👉 右滑＝记住正确 · 左滑＝记错 · 与练习模式相同</p>
    </template>

    <!-- 无到期题 -->
    <div v-if="!currentItem" class="empty-state">
      <template v-if="pendingCount > 0">
        <p>✅ 今日到期的错题已全部复习完！</p>
        <p class="sub-tip">还有 {{ pendingCount }} 题在记忆周期中，到期后会自动出现在这里</p>
      </template>
      <template v-else>
        <p>目前没有错题，继续保持！</p>
      </template>
      <button class="primary-btn" @click="router.push('/')">返回首页</button>
    </div>
  </div>
</template>

<style scoped>
.review-container { display: flex; flex-direction: column; min-height: 100%; }
.review-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.review-header h2 { flex: 1; margin: 0; font-size: 1.2rem; }
.back-btn { border: 0; background: transparent; color: #4b6cb7; cursor: pointer; }
.count { color: #777; font-size: .9rem; }

.wrong-panel {
  margin-top: 1rem; padding: 1rem;
  border-left: 4px solid #ff6b6b; background: #fff5f5; border-radius: 0 10px 10px 0;
  animation: slide-up .25s ease-out;
}
.wrong-panel strong { color: #d14d4d; display: block; margin-bottom: .3rem; }
.wrong-panel p { margin: .25rem 0; line-height: 1.5; }
.exp-text { color: #444; }
.sub-tip { color: #999 !important; font-size: .85rem; }
.waiting-tip { margin-top: 1rem; text-align: center; color: #999; font-size: .9rem; }

.gesture-tip { text-align: center; color: #aaa; font-size: .82rem; margin-top: .8rem; }

.primary-btn {
  margin-top: .8rem; border: 0; border-radius: 22px; padding: 10px 26px;
  background: #4b6cb7; color: white; font-weight: 600; cursor: pointer;
}

.empty-state {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: .4rem;
  color: #777; text-align: center; padding: 2rem;
}
.empty-state p { margin: .15rem 0; }
.sub-tip { color: #aaa; font-size: .88rem; }

@keyframes slide-up { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
</style>
