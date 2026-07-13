<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const goHome = () => {
  router.push('/');
};
</script>

<template>
  <div class="review-container">
    <header class="review-header">
      <button class="back-btn" @click="goHome">← 返回</button>
      <h2>错题本 (SRS)</h2>
    </header>
    
    <div class="empty-state">
      <p>目前没有需要复习的错题。</p>
      <button class="primary-btn" @click="goHome">去模拟考</button>
    </div>
  </div>
</template>

<style scoped>
.review-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.back-btn {
  background: transparent;
  border: none;
  font-size: 1rem;
  color: #4b6cb7;
  cursor: pointer;
  margin-right: 1rem;
}

h2 {
  margin: 0;
  font-size: 1.2rem;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #777;
}

.primary-btn {
  margin-top: 1rem;
  background: #4b6cb7;
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 20px;
}
</style>
