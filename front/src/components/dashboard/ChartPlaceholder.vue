<template>
  <section class="panel chart-panel">
    <h2 class="panel-title">BTC 가격 차트</h2>
    <div class="chart-placeholder">
      <p class="placeholder-value">차트 준비 중</p>
      <p class="muted hint">실제 거래소 OHLCV / 차트 라이브러리 연결 예정</p>
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
}
</style>
