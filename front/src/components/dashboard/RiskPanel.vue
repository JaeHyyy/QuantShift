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
    <p class="hint muted">위험 여부·조치 안내는 위쪽 상태 카드에서 먼저 확인하세요.</p>
  </section>
</template>

<style scoped>
.hint {
  margin: 14px 0 0;
  font-size: 12px;
  line-height: 1.45;
}
</style>
