<template>
  <section class="panel">
    <div class="head">
      <h2 class="panel-title">시장 분석 / 전략</h2>
      <!-- 개발용 Mock 전환 — 실제 서비스 기능 아님 -->
      <div class="dev-controls">
        <span class="dev-label">DEV Mock</span>
        <select
          :value="scenario"
          :disabled="loading"
          @change="onSelect"
        >
          <option
            v-for="s in scenarios"
            :key="s"
            :value="s"
          >
            {{ s }}
          </option>
        </select>
        <button
          type="button"
          class="btn"
          :disabled="loading"
          @click="$emit('refresh')"
        >
          {{ loading ? '조회 중…' : '다시 조회' }}
        </button>
      </div>
    </div>

    <p
      v-if="error"
      class="err"
    >{{ error }}</p>

    <div class="market-layout">
      <div class="summary">
        <div>
          <span class="metric-label">현재 Regime</span>
          <span
            v-if="regime"
            class="regime-badge"
            :class="`regime-${regime}`"
          >{{ regime }}</span>
          <span
            v-else
            class="placeholder-value"
          >—</span>
        </div>
        <div>
          <span class="metric-label">현재 선택된 전략</span>
          <span class="placeholder-value">미연결</span>
        </div>
        <div>
          <span class="metric-label">Mock 시나리오</span>
          <span class="metric-value">{{ scenario }}</span>
        </div>
      </div>

      <div class="metric-grid indicators">
        <div>
          <span class="metric-label">ADX</span>
          <span class="metric-value">{{ fmt(indicators?.adx) }}</span>
        </div>
        <div>
          <span class="metric-label">EMA slope</span>
          <span class="metric-value">{{ fmt(indicators?.ema_slope, 6) }}</span>
        </div>
        <div>
          <span class="metric-label">ATR</span>
          <span class="metric-value">{{ fmt(indicators?.atr) }}</span>
        </div>
        <div>
          <span class="metric-label">ATR ratio</span>
          <span class="metric-value">{{ fmt(indicators?.atr_ratio) }}</span>
        </div>
        <div>
          <span class="metric-label">Volume ratio</span>
          <span class="metric-value">{{ fmt(indicators?.volume_ratio) }}</span>
        </div>
        <div>
          <span class="metric-label">EMA</span>
          <span class="metric-value">{{ fmt(indicators?.ema) }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { listMockScenarios } from '../../api/regime'

defineProps({
  regime: { type: String, default: null },
  indicators: { type: Object, default: null },
  scenario: { type: String, required: true },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const emit = defineEmits(['change-scenario', 'refresh'])
const scenarios = listMockScenarios()

function onSelect(e) {
  emit('change-scenario', e.target.value)
}

function fmt(value, digits = 4) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—'
  return Number(value).toFixed(digits)
}
</script>

<style scoped>
.head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 4px;
}

.head .panel-title {
  margin-bottom: 0;
}

.dev-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border: 1px dashed #4a5564;
  border-radius: 6px;
  background: #141a22;
}

.dev-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--warn);
  letter-spacing: 0.04em;
}

select,
.btn {
  background: var(--bg-elevated);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 13px;
}

.btn {
  cursor: pointer;
}

.btn:disabled,
select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.err {
  color: var(--danger);
  font-size: 13px;
  margin: 0 0 10px;
}

.market-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 16px;
}

.summary {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.indicators {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

@media (max-width: 800px) {
  .market-layout {
    grid-template-columns: 1fr;
  }

  .indicators {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
