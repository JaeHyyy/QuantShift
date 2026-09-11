<template>
  <div class="dashboard">
    <TopBar
      :regime="regime"
      :loading="loading"
      :error="error"
    />

    <div class="dashboard-grid">
      <ChartPlaceholder class="area-chart" />
      <AssetPanel class="area-asset" />
      <PerformancePanel class="area-perf" />
      <MarketAnalysisPanel
        class="area-market"
        :regime="regime"
        :indicators="indicators"
        :scenario="scenario"
        :loading="loading"
        :error="error"
        @change-scenario="onScenarioChange"
        @refresh="loadRegime"
      />
      <OrdersPanel class="area-orders" />
      <RiskPanel class="area-risk" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchRegimeFromMock } from '../../api/regime'
import TopBar from './TopBar.vue'
import ChartPlaceholder from './ChartPlaceholder.vue'
import AssetPanel from './AssetPanel.vue'
import PerformancePanel from './PerformancePanel.vue'
import MarketAnalysisPanel from './MarketAnalysisPanel.vue'
import OrdersPanel from './OrdersPanel.vue'
import RiskPanel from './RiskPanel.vue'

const scenario = ref('RANGE')
const regime = ref(null)
const indicators = ref(null)
const loading = ref(false)
const error = ref('')

async function loadRegime() {
  loading.value = true
  error.value = ''
  try {
    const data = await fetchRegimeFromMock(scenario.value)
    regime.value = data.regime
    indicators.value = data.indicators
  } catch (e) {
    error.value = e.message || String(e)
    regime.value = null
    indicators.value = null
  } finally {
    loading.value = false
  }
}

function onScenarioChange(next) {
  scenario.value = next
  loadRegime()
}

onMounted(loadRegime)
</script>

<style scoped>
.dashboard {
  max-width: 1440px;
  margin: 0 auto;
  padding: 16px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  grid-template-areas:
    "chart asset"
    "chart perf"
    "market market"
    "orders risk";
  gap: 12px;
}

.area-chart { grid-area: chart; }
.area-asset { grid-area: asset; }
.area-perf { grid-area: perf; }
.area-market { grid-area: market; }
.area-orders { grid-area: orders; }
.area-risk { grid-area: risk; }

@media (max-width: 900px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "chart"
      "asset"
      "perf"
      "market"
      "orders"
      "risk";
  }
}
</style>
