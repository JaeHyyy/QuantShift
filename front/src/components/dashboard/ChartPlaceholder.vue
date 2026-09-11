<template>
  <section class="panel chart-panel">
    <h2 class="panel-title">가격 흐름</h2>
    <div class="chart-placeholder">
      <p class="placeholder-value">차트 준비 중</p>
      <p class="muted hint">실제 시세가 연결되면 여기에 가격 그래프가 표시됩니다.</p>
    </div>
  </section>
</template>

<style scoped>
.chart-panel {
  min-height: 280px;
  display: flex;
  flex-direction: column;
}

.chart-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px dashed var(--border);
  border-radius: 6px;
  background: var(--bg-elevated);
  gap: 6px;
}

.hint {
  margin: 0;
  font-size: 12px;
  text-align: center;
  padding: 0 16px;
}
</style>
