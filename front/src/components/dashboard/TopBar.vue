<template>
  <header class="topbar panel">
    <div class="brand-block">
      <div class="brand-row">
        <span class="brand-name">QuantShift</span>
        <span class="pair muted">BTC/KRW</span>
      </div>
      <p class="brand-sub muted">자동매매 현황을 한눈에 확인하세요</p>
    </div>

    <div class="status-cards">
      <div class="status-card">
        <span class="metric-label">자동매매</span>
        <span class="status-main">꺼짐</span>
        <span class="status-sub muted">준비 중 · 아직 연결되지 않음</span>
      </div>

      <div class="status-card">
        <span class="metric-label">지금 시장</span>
        <template v-if="loading">
          <span class="status-main muted">불러오는 중…</span>
        </template>
        <template v-else>
          <span
            class="status-main"
            :class="regimeClass"
          >{{ regimeCopy.label }}</span>
          <span class="status-sub muted">{{ regimeCopy.description }}</span>
        </template>
      </div>

      <div class="status-card">
        <span class="metric-label">대응 전략</span>
        <span class="status-main">—</span>
        <span class="status-sub muted">준비 중</span>
      </div>

      <div class="status-card">
        <span class="metric-label">오늘 수익/손실</span>
        <span class="status-main">—</span>
        <span class="status-sub muted">준비 중</span>
      </div>
    </div>

    <div
      v-if="!loading && regime"
      class="action-banner"
      :class="actionClass"
    >
      <strong>지금 알아둘 점</strong>
      <span>{{ regimeCopy.actionHint }}</span>
    </div>

    <p
      v-if="error"
      class="top-error"
    >{{ error }}</p>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { getRegimeCopy } from '../../utils/marketCopy'

const props = defineProps({
  regime: { type: String, default: null },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const regimeCopy = computed(() => getRegimeCopy(props.regime))
const regimeClass = computed(() =>
  props.regime ? `regime-${props.regime}` : 'regime-EMPTY',
)
const actionClass = computed(() => {
  if (props.regime === 'HIGH_VOL') return 'action-danger'
  if (props.regime === 'UNKNOWN') return 'action-muted'
  return 'action-info'
})
</script>

<style scoped>
.topbar {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 12px;
}

.brand-row {
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
  font-size: 13px;
}

.brand-sub {
  margin: 4px 0 0;
  font-size: 13px;
}

.status-cards {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.status-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-height: 88px;
}

.status-main {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.25;
}

.status-sub {
  font-size: 12px;
  line-height: 1.35;
}

.action-banner {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  align-items: baseline;
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid var(--border);
  font-size: 13px;
}

.action-info {
  background: #152033;
  border-color: #2f4b6e;
}

.action-danger {
  background: #2a1c14;
  border-color: #7a4a1a;
  color: #ffd79a;
}

.action-muted {
  background: var(--bg-elevated);
}

.top-error {
  margin: 0;
  color: var(--danger);
  font-size: 13px;
}

@media (max-width: 900px) {
  .status-cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 520px) {
  .status-cards {
    grid-template-columns: 1fr;
  }
}
</style>
