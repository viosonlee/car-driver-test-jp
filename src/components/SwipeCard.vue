<script setup lang="ts">
import { computed, ref } from 'vue';
import { resolveAssetUrl } from '../utils/assetUrl';
import type { Question } from '../db';

/**
 * 通用滑动答题卡片：
 * - 右滑 = 判定"正确(○)"，左滑 = 判定"错误(×)"
 * - 松手超过阈值 → emit('answer', value)，由父组件决定飞出或回弹
 * - 答对：父组件调用 flyOut(dir) 卡片滑出屏幕；答错：调用 revert() 抖动回中
 * - 也支持点击下方按钮作答（桌面/无障碍），行为与滑动一致
 */
const props = defineProps<{
  question: Question;
  disabled?: boolean;   // 已作答待处理时锁定
  hint?: string;        // 卡片左上角小标签（如轮次/阶段）
}>();

const emit = defineEmits<{ (e: 'answer', value: boolean): void }>();

const THRESHOLD_RATIO = 0.28; // 触发阈值为卡宽的28%
const cardEl = ref<HTMLElement | null>(null);

const dragX = ref(0);
const dragging = ref(false);
const flying = ref<'left' | 'right' | null>(null);
const shaking = ref(false);
let answeredLocally = false; // 防止滑动判定与按钮点击双触发

let startX = 0;
let startY = 0;
let pointerId: number | null = null;

const threshold = computed(() => (cardEl.value?.offsetWidth || 320) * THRESHOLD_RATIO);
const overlay = computed(() => {
  if (dragX.value > threshold.value * 0.5) return { text: '○ 正确', cls: 'right' };
  if (dragX.value < -threshold.value * 0.5) return { text: '✕ 错误', cls: 'left' };
  return null;
});

const cardStyle = computed(() => {
  if (flying.value === 'right') return { transform: 'translateX(130%) rotate(18deg)', opacity: 0.3 };
  if (flying.value === 'left') return { transform: 'translateX(-130%) rotate(-18deg)', opacity: 0.3 };
  const rotate = dragX.value / 22;
  return { transform: `translateX(${dragX.value}px) rotate(${rotate}deg)` };
});

const onPointerDown = (e: PointerEvent) => {
  if (props.disabled || flying.value || shaking.value) return;
  // 只响应主键（鼠标左键/触摸/笔）
  if (!e.isPrimary) return;
  pointerId = e.pointerId;
  startX = e.clientX;
  startY = e.clientY;
  dragging.value = true;
  (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
};

const onPointerMove = (e: PointerEvent) => {
  if (!dragging.value || e.pointerId !== pointerId) return;
  const dx = e.clientX - startX;
  const dy = e.clientY - startY;
  // 垂直滑动为主时不拖动（避免干扰页面滚动）
  if (Math.abs(dy) > Math.abs(dx) && Math.abs(dx) < 12) return;
  dragX.value = Math.max(-400, Math.min(400, dx));
};

const onPointerUp = (e: PointerEvent) => {
  if (!dragging.value || e.pointerId !== pointerId) return;
  dragging.value = false;
  pointerId = null;
  commitIfPastThreshold();
};

const commitIfPastThreshold = () => {
  if (dragX.value >= threshold.value) emitAnswer(true);
  else if (dragX.value <= -threshold.value) emitAnswer(false);
  else dragX.value = 0; // 弹回
};

const emitAnswer = (value: boolean) => {
  if (props.disabled || answeredLocally) { dragX.value = 0; return; }
  answeredLocally = true;
  emit('answer', value);
};

// ---- 按钮作答：先做小幅飞出预览再走同一流程 ----
const answerByButton = async (value: boolean) => {
  if (props.disabled) return;
  dragX.value = value ? threshold.value * 1.2 : -threshold.value * 1.2;
  emitAnswer(value);
};

const flyOut = (dir: 'left' | 'right') => {
  flying.value = dir;
  window.setTimeout(() => {
    flying.value = null;
    dragX.value = 0;
    answeredLocally = false; // 组件若被复用（未换 key）也能恢复可交互
  }, 320);
};

const shakeAndRevert = () => {
  dragX.value = 0; // 立即归零，避免动画结束后内联 transform 闪跳
  shaking.value = true;
  window.setTimeout(() => {
    shaking.value = false;
  }, 420);
};

defineExpose({ flyOut, shakeAndRevert });
</script>

<template>
  <div class="swipe-stage">
    <div
      ref="cardEl"
      class="swipe-card"
      :class="{ dragging, shaking }"
      :style="cardStyle"
      @pointerdown="onPointerDown"
      @pointermove="onPointerMove"
      @pointerup="onPointerUp"
      @pointercancel="onPointerUp"
    >
      <!-- 滑动方向浮层 -->
      <div v-if="overlay && !flying" class="swipe-overlay" :class="overlay.cls">{{ overlay.text }}</div>

      <!-- 标签行：正常文档流，不与题干/图片重叠 -->
      <div v-if="hint && !overlay" class="hint-row">
        <span class="hint-badge">{{ hint }}</span>
      </div>

      <!-- 题目图片 -->
      <div v-if="question.image_url" class="question-image">
        <img :src="resolveAssetUrl(question.image_url)" alt="题目图片" draggable="false" />
      </div>
      <p v-if="question.scenario" class="scenario-text">{{ question.scenario }}</p>

      <!-- 题干 -->
      <div class="q-text">
        <p class="cn">{{ question.question }}</p>
        <p v-if="question.question_jp" class="jp">{{ question.question_jp }}</p>
      </div>

      <!-- 判断按钮 -->
      <div class="tf-buttons">
        <button class="tf-btn wrong-btn" :disabled="disabled" @click="answerByButton(false)">✕ 错误<br /><small>← 左滑</small></button>
        <button class="tf-btn right-btn" :disabled="disabled" @click="answerByButton(true)">○ 正确<br /><small>右滑 →</small></button>
      </div>
    </div>
    <slot name="below" />
  </div>
</template>

<style scoped>
.swipe-stage { position: relative; touch-action: pan-y; }
.swipe-card {
  position: relative;
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0,0,0,.08);
  user-select: none;
  cursor: grab;
  transition: transform .25s ease, opacity .25s ease;
}
.swipe-card.dragging { transition: none; cursor: grabbing; }
.swipe-card.shaking { animation: card-shake .4s ease; }
@keyframes card-shake {
  0% { transform: translateX(0); }
  20% { transform: translateX(-14px); }
  40% { transform: translateX(12px); }
  60% { transform: translateX(-8px); }
  80% { transform: translateX(5px); }
  100% { transform: translateX(0); }
}
.swipe-overlay {
  position: absolute; top: 14px; z-index: 2;
  font-size: 1.6rem; font-weight: 800; letter-spacing: .1em;
  padding: 4px 14px; border-radius: 8px; border: 3px solid;
  background: rgba(255,255,255,.85); pointer-events: none;
}
.swipe-overlay.right { left: 14px; color: #2c8a5f; border-color: #42b883; transform: rotate(-10deg); }
.swipe-overlay.left { right: 14px; color: #d14d4d; border-color: #ff6b6b; transform: rotate(10deg); }
.hint-row {
  display: flex;
  justify-content: flex-end;
  margin: -2px -4px .35rem 0; /* 贴近卡片右上角 */
}
.hint-badge {
  background: #eef2fb; color: #4b6cb7;
  font-size: .75rem; padding: 3px 10px; border-radius: 999px;
}
.question-image img {
  display: block; width: auto; max-width: 100%; height: auto;
  max-height: 300px; object-fit: contain; border-radius: 8px; margin: .6rem auto;
  -webkit-user-drag: none;
}
.scenario-text { font-style: italic; color: #666; font-size: .9rem; }
.q-text { margin-top: .8rem; }
.q-text .cn { font-size: 1.12rem; font-weight: 500; line-height: 1.55; margin: 0 0 .4rem; }
.q-text .jp { font-size: .92rem; color: #888; line-height: 1.45; margin: 0; }
.tf-buttons { display: flex; gap: 1rem; margin-top: 1.4rem; }
.tf-btn {
  flex: 1; padding: .9rem .5rem;
  border: 2px solid #eaeaea; border-radius: 10px; background: white;
  font-size: 1.05rem; font-weight: 600; cursor: pointer; transition: all .15s;
}
.tf-btn small { display: block; font-weight: 400; font-size: .72rem; color: #aaa; margin-top: 2px; }
.tf-btn:active:not(:disabled) { transform: scale(.97); }
.tf-btn:disabled { opacity: .45; cursor: default; }
.right-btn:hover:not(:disabled) { border-color: #42b883; background: #f0faf5; }
.wrong-btn:hover:not(:disabled) { border-color: #ff6b6b; background: #fff5f5; }
</style>
