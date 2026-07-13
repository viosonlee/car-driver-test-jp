<script setup lang="ts">
// Main App Component
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1>交通规则教程</h1>
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 100vw;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.app-header {
  background: linear-gradient(135deg, #182848 0%, #4b6cb7 100%);
  color: white;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 10;
}

.app-header h1 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
}

main {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}
</style>
