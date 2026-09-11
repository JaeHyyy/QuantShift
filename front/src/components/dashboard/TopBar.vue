<template>
  <header class="topbar panel">
    <div class="brand">
      <span class="brand-name">QuantShift</span>
      <span class="pair muted">BTC/KRW</span>
    </div>

    <div class="status-group">
      <div class="status-item">
        <span class="metric-label">Bot 상태</span>
        <span class="placeholder-value">미연결</span>
      </div>
      <div class="status-item">
        <span class="metric-label">현재 시장 Regime</span>
        <span
          v-if="loading"
          class="placeholder-value"
        >불러오는 중…</span>
        <span
          v-else-if="regime"
          class="regime-badge"
          :class="`regime-${regime}`"
        >{{ regime }}</span>
        <span
          v-else
          class="regime-badge regime-EMPTY"
        >—</span>
      </div>
    </div>

    <p
      v-if="error"
      class="top-error"
    >{{ error }}</p>
  </header>
</template>

<script setup>
defineProps({
  regime: { type: String, default: null },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})
</script>

<style scoped>
.topbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 12px;
}

.brand {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.brand-name {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.pair {
  font-family: var(--mono);
  font-size: 13px;
}

.status-group {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.status-item {
  min-width: 120px;
}

.top-error {
  width: 100%;
  margin: 0;
  color: var(--danger);
  font-size: 13px;
}
</style>
