<template>
  <header class="topbar">
    <div class="brand-row">
      <div class="brand-left">
        <span class="logo-mark" aria-hidden="true" />
        <div>
          <div class="title-line">
            <h1 class="brand-name">QuantShift</h1>
            <span class="pair">BTC / KRW</span>
          </div>
          <p class="brand-sub">자동매매 현황을 한눈에</p>
        </div>
      </div>
    </div>

    <div class="status-strip">
      <div class="status-item">
        <span class="metric-label">자동매매</span>
        <span class="status-main">꺼짐</span>
        <span class="status-sub muted">준비 중 · 아직 연결되지 않음</span>
      </div>

      <div class="status-item featured">
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

      <div class="status-item">
        <span class="metric-label">대응 전략</span>
        <span class="status-main">—</span>
        <span class="status-sub muted">준비 중</span>
      </div>

      <div class="status-item">
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
      <span class="action-dot" aria-hidden="true" />
      <div>
        <strong>지금 알아둘 점</strong>
        <span>{{ regimeCopy.actionHint }}</span>
      </div>
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
  gap: 18px;
  margin-bottom: 16px;
  padding: 8px 2px 4px;
}

.brand-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo-mark {
  width: 14px;
  height: 36px;
  border-radius: 99px;
  background: linear-gradient(180deg, #2dd4bf, var(--brand-strong));
  box-shadow: 0 0 0 4px var(--brand-soft);
  flex-shrink: 0;
}

.title-line {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.brand-name {
  margin: 0;
  font-family: var(--display);
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text);
}

.pair {
  font-size: 13px;
  color: var(--brand);
  font-weight: 600;
}

.brand-sub {
  margin: 2px 0 0;
  font-size: 13px;
  color: var(--text-muted);
}

.status-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0;
  border: 1px solid var(--border-soft);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--bg-panel);
  box-shadow: var(--shadow);
}

.status-item {
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-height: 104px;
  border-right: 1px solid var(--border-soft);
}

.status-item:last-child {
  border-right: none;
}

.status-item.featured {
  background: linear-gradient(180deg, var(--brand-soft), transparent 70%);
}

.status-main {
  font-family: var(--display);
  font-size: 22px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.status-sub {
  font-size: 12px;
  line-height: 1.4;
}

.action-banner {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  line-height: 1.45;
}

.action-banner strong {
  display: inline-block;
  margin-right: 8px;
}

.action-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
  background: var(--brand);
}

.action-info {
  background: var(--brand-soft);
  border: 1px solid rgba(15, 159, 143, 0.35);
}

.action-danger {
  background: rgba(232, 168, 56, 0.12);
  border: 1px solid rgba(232, 168, 56, 0.35);
  color: #f3d59a;
}

.action-danger .action-dot {
  background: var(--warn);
}

.action-muted {
  background: var(--bg-elevated);
  border: 1px solid var(--border-soft);
}

.action-muted .action-dot {
  background: var(--text-muted);
}

.top-error {
  margin: 0;
  color: var(--danger);
  font-size: 13px;
}

@media (max-width: 900px) {
  .status-strip {
    grid-template-columns: 1fr 1fr;
  }

  .status-item:nth-child(2n) {
    border-right: none;
  }

  .status-item:nth-child(-n + 2) {
    border-bottom: 1px solid var(--border-soft);
  }
}

@media (max-width: 520px) {
  .status-strip {
    grid-template-columns: 1fr;
  }

  .status-item {
    border-right: none;
    border-bottom: 1px solid var(--border-soft);
  }

  .status-item:last-child {
    border-bottom: none;
  }
}
</style>
