<template>
  <section class="panel market-panel">
    <div class="head">
      <h2 class="panel-title">시장 상황 · 전략</h2>
      <div class="dev-controls">
        <span class="dev-label">개발용 예시</span>
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
            {{ mockScenarioLabel(s) }}
          </option>
        </select>
        <button
          type="button"
          class="btn"
          :disabled="loading"
          @click="$emit('refresh')"
        >
          {{ loading ? '확인 중…' : '다시 확인' }}
        </button>
      </div>
    </div>

    <p
      v-if="error"
      class="err"
    >{{ error }}</p>

    <div class="hero">
      <div class="hero-main">
        <span class="metric-label">지금 시장은</span>
        <p
          class="hero-label"
          :class="regimeClass"
        >{{ regimeCopy.label }}</p>
        <p class="hero-desc">{{ regimeCopy.description }}</p>
      </div>
      <div class="hero-side">
        <div class="side-box">
          <span class="metric-label">지금 쓰는 전략</span>
          <p class="side-value">—</p>
          <p class="side-hint muted">준비 중</p>
        </div>
        <div class="side-box">
          <span class="metric-label">내가 할 일</span>
          <p class="side-value-sm">{{ regimeCopy.actionHint }}</p>
        </div>
      </div>
    </div>

    <div class="plain-grid">
      <div class="plain-card">
        <span class="metric-label">추세 강도</span>
        <span
          class="plain-value"
          :class="`tone-${trendStrength.tone}`"
        >{{ trendStrength.text }}</span>
      </div>
      <div class="plain-card">
        <span class="metric-label">가격 방향</span>
        <span
          class="plain-value"
          :class="`tone-${priceDirection.tone}`"
        >{{ priceDirection.text }}</span>
      </div>
      <div class="plain-card">
        <span class="metric-label">가격 변동성</span>
        <span
          class="plain-value"
          :class="`tone-${volatility.tone}`"
        >{{ volatility.text }}</span>
      </div>
      <div class="plain-card">
        <span class="metric-label">거래 활발도</span>
        <span
          class="plain-value"
          :class="`tone-${activity.tone}`"
        >{{ activity.text }}</span>
      </div>
    </div>

    <details class="details">
      <summary>상세 지표 보기</summary>
      <p class="details-hint muted">
        개발·점검용 숫자입니다. 평소에는 위 상태만 보시면 됩니다.
      </p>
      <div class="metric-grid details-grid">
        <div>
          <span class="metric-label">ADX (추세 강도)</span>
          <span class="metric-value">{{ formatNumber(indicators?.adx) }}</span>
        </div>
        <div>
          <span class="metric-label">EMA slope (가격 방향)</span>
          <span class="metric-value">{{ formatNumber(indicators?.ema_slope, 6) }}</span>
        </div>
        <div>
          <span class="metric-label">ATR (변동 폭)</span>
          <span class="metric-value">{{ formatNumber(indicators?.atr) }}</span>
        </div>
        <div>
          <span class="metric-label">ATR ratio (변동성 배수)</span>
          <span class="metric-value">{{ formatNumber(indicators?.atr_ratio) }}</span>
        </div>
        <div>
          <span class="metric-label">Volume ratio (거래량 배수)</span>
          <span class="metric-value">{{ formatNumber(indicators?.volume_ratio) }}</span>
        </div>
        <div>
          <span class="metric-label">EMA</span>
          <span class="metric-value">{{ formatNumber(indicators?.ema) }}</span>
        </div>
      </div>
    </details>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { listMockScenarios } from '../../api/regime'
import {
  describePriceDirection,
  describeTradingActivity,
  describeTrendStrength,
  describeVolatility,
  formatNumber,
  getRegimeCopy,
  mockScenarioLabel,
} from '../../utils/marketCopy'

const props = defineProps({
  regime: { type: String, default: null },
  indicators: { type: Object, default: null },
  scenario: { type: String, required: true },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const emit = defineEmits(['change-scenario', 'refresh'])
const scenarios = listMockScenarios()

const regimeCopy = computed(() => getRegimeCopy(props.regime))
const regimeClass = computed(() =>
  props.regime ? `regime-${props.regime}` : 'regime-EMPTY',
)
const trendStrength = computed(() =>
  describeTrendStrength(props.indicators?.adx),
)
const priceDirection = computed(() =>
  describePriceDirection(props.indicators?.ema_slope),
)
const volatility = computed(() =>
  describeVolatility(props.indicators?.atr_ratio),
)
const activity = computed(() =>
  describeTradingActivity(props.indicators?.volume_ratio),
)

function onSelect(e) {
  emit('change-scenario', e.target.value)
}
</script>

<style scoped>
.market-panel {
  border-top: 2px solid var(--brand);
}

.head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.head .panel-title {
  margin-bottom: 0;
  font-family: var(--display);
  font-size: 15px;
  color: var(--text);
}

.dev-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border: 1px dashed rgba(15, 159, 143, 0.45);
  border-radius: var(--radius-sm);
  background: var(--brand-soft);
}

.dev-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--brand);
}

select,
.btn {
  background: var(--bg-elevated);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 7px 11px;
  font-size: 13px;
}

.btn {
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease;
}

.btn:hover:not(:disabled) {
  border-color: var(--brand);
  background: rgba(15, 159, 143, 0.12);
}

.btn:disabled,
select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.err {
  color: var(--danger);
  font-size: 13px;
  margin: 0 0 12px;
}

.hero {
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  gap: 14px;
  margin-bottom: 14px;
}

.hero-main {
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(135deg, var(--brand-soft), transparent 55%),
    var(--bg-elevated);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius);
  padding: 18px 20px;
}

.hero-label {
  margin: 6px 0 10px;
  font-family: var(--display);
  font-size: 34px;
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.15;
}

.hero-desc {
  margin: 0;
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.5;
  max-width: 42ch;
}

.hero-side {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.side-box {
  background: var(--bg-elevated);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}

.side-value {
  margin: 4px 0 0;
  font-family: var(--display);
  font-size: 22px;
  font-weight: 700;
}

.side-value-sm {
  margin: 6px 0 0;
  font-size: 14px;
  line-height: 1.45;
}

.side-hint {
  margin: 2px 0 0;
  font-size: 12px;
}

.plain-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.plain-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.plain-value {
  font-family: var(--display);
  font-size: 18px;
  font-weight: 700;
}

.tone-up { color: var(--up); }
.tone-down { color: var(--down); }
.tone-danger { color: var(--danger); }
.tone-warn { color: var(--warn); }
.tone-strong { color: var(--brand); }
.tone-normal { color: var(--text); }
.tone-muted { color: var(--text-muted); }

.details {
  border-top: 1px solid var(--border-soft);
  padding-top: 12px;
}

.details summary {
  cursor: pointer;
  color: var(--brand);
  font-size: 13px;
  font-weight: 600;
  user-select: none;
}

.details-hint {
  margin: 8px 0;
  font-size: 12px;
}

.details-grid {
  margin-top: 8px;
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .plain-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
