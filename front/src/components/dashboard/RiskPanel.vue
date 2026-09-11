<template>
  <section class="panel">
    <h2 class="panel-title">위험 관리</h2>
    <div class="metric-grid">
      <div>
        <span class="metric-label">지금 투자 비중</span>
        <span class="placeholder-value">—</span>
      </div>
      <div>
        <span class="metric-label">오늘 손실</span>
        <span class="placeholder-value">—</span>
      </div>
      <div>
        <span class="metric-label">최대 투자 비중</span>
        <span class="placeholder-value">준비 중</span>
      </div>
      <div>
        <span class="metric-label">긴급 중지</span>
        <span class="placeholder-value">준비 중</span>
      </div>
    </div>
    <p class="hint muted">위험한 상태인지, 내가 조치할 일이 있는지는 위쪽 안내를 먼저 보세요.</p>
  </section>
</template>

<style scoped>
.hint {
  margin: 12px 0 0;
  font-size: 12px;
  line-height: 1.4;
}
</style>
