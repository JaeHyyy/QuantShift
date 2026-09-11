<template>
  <section class="panel chart-panel">
    <h2 class="panel-title">가격 흐름</h2>
    <div class="chart-placeholder">
      <div class="ghost-bars" aria-hidden="true">
        <span /><span /><span /><span /><span /><span /><span />
      </div>
      <p class="placeholder-value">차트 준비 중</p>
      <p class="muted hint">시세가 연결되면 여기에 가격 그래프가 표시됩니다.</p>
    </div>
  </section>
</template>

<style scoped>
.chart-panel {
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.chart-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 1px dashed rgba(15, 159, 143, 0.35);
  border-radius: var(--radius-sm);
  background:
    linear-gradient(180deg, var(--brand-soft), transparent 55%),
    var(--bg-elevated);
}

.ghost-bars {
  display: flex;
  align-items: flex-end;
  gap: 6px;
  height: 54px;
  margin-bottom: 6px;
  opacity: 0.45;
}

.ghost-bars span {
  width: 10px;
  border-radius: 3px 3px 0 0;
  background: var(--brand);
}

.ghost-bars span:nth-child(1) { height: 18px; }
.ghost-bars span:nth-child(2) { height: 28px; }
.ghost-bars span:nth-child(3) { height: 22px; }
.ghost-bars span:nth-child(4) { height: 40px; }
.ghost-bars span:nth-child(5) { height: 30px; }
.ghost-bars span:nth-child(6) { height: 46px; }
.ghost-bars span:nth-child(7) { height: 34px; }

.hint {
  margin: 0;
  font-size: 12px;
  text-align: center;
  padding: 0 16px;
}
</style>
