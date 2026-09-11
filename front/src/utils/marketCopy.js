/**
 * 메인 대시보드용 쉬운 표현.
 * 백엔드 enum/숫자는 그대로 두고, 화면 표시만 변환한다.
 *
 * 구간 기준은 back/app/regime/thresholds.py 초기값과 맞춤.
 * (확정 전략 아님 — UI 설명용)
 */

const ADX_RANGE_MAX = 20
const ADX_TREND_MIN = 25
const EMA_SLOPE_FLAT_ABS = 0.002
const ATR_HIGH_VOL_MIN = 1.8
const VOLUME_CONFIRM_MIN = 1.2

/** @type {Record<string, { label: string, description: string, actionHint: string }>} */
export const REGIME_COPY = {
  RANGE: {
    label: '횡보장',
    description: '가격이 일정 범위 안에서 움직이고 있습니다.',
    actionHint: '급하게 방향을 쫓기보다 관망해도 됩니다.',
  },
  UPTREND: {
    label: '상승장',
    description: '가격이 상승하는 흐름을 보이고 있습니다.',
    actionHint: '상승 추세용 전략이 연결되면 여기에 표시됩니다.',
  },
  DOWNTREND: {
    label: '하락장',
    description: '가격이 하락하는 흐름을 보이고 있습니다.',
    actionHint: '하락 추세용 전략이 연결되면 여기에 표시됩니다.',
  },
  HIGH_VOL: {
    label: '급변동',
    description: '가격 움직임이 매우 커 자동매매를 멈추는 것이 안전합니다.',
    actionHint: '지금은 자동매매를 잠시 멈추는 편이 안전합니다.',
  },
  UNKNOWN: {
    label: '판단 대기',
    description: '시장 방향이 명확하지 않습니다.',
    actionHint: '데이터가 더 쌓일 때까지 기다려 주세요.',
  },
}

export function getRegimeCopy(regime) {
  if (!regime) {
    return {
      label: '확인 중',
      description: '시장 상태를 불러오는 중입니다.',
      actionHint: '잠시만 기다려 주세요.',
    }
  }
  return (
    REGIME_COPY[regime] || {
      label: '판단 대기',
      description: '시장 방향이 명확하지 않습니다.',
      actionHint: '잠시 후 다시 확인해 주세요.',
    }
  )
}

/** DEV Mock 선택 UI용 라벨 */
export function mockScenarioLabel(scenario) {
  const copy = REGIME_COPY[scenario]
  return copy ? copy.label : scenario
}

export function describeTrendStrength(adx) {
  if (adx === null || adx === undefined || Number.isNaN(adx)) {
    return { text: '확인 중', tone: 'muted' }
  }
  if (adx <= ADX_RANGE_MAX) return { text: '약함', tone: 'muted' }
  if (adx >= ADX_TREND_MIN) return { text: '강함', tone: 'strong' }
  return { text: '보통', tone: 'normal' }
}

export function describePriceDirection(emaSlope) {
  if (emaSlope === null || emaSlope === undefined || Number.isNaN(emaSlope)) {
    return { text: '확인 중', tone: 'muted' }
  }
  if (emaSlope > EMA_SLOPE_FLAT_ABS) return { text: '상승', tone: 'up' }
  if (emaSlope < -EMA_SLOPE_FLAT_ABS) return { text: '하락', tone: 'down' }
  return { text: '횡보', tone: 'muted' }
}

export function describeVolatility(atrRatio) {
  if (atrRatio === null || atrRatio === undefined || Number.isNaN(atrRatio)) {
    return { text: '확인 중', tone: 'muted' }
  }
  if (atrRatio >= ATR_HIGH_VOL_MIN) return { text: '위험', tone: 'danger' }
  if (atrRatio >= 1.2) return { text: '보통', tone: 'warn' }
  return { text: '안정', tone: 'up' }
}

export function describeTradingActivity(volumeRatio) {
  if (
    volumeRatio === null ||
    volumeRatio === undefined ||
    Number.isNaN(volumeRatio)
  ) {
    return { text: '확인 중', tone: 'muted' }
  }
  if (volumeRatio >= VOLUME_CONFIRM_MIN) return { text: '활발', tone: 'strong' }
  if (volumeRatio >= 0.8) return { text: '평소 수준', tone: 'normal' }
  return { text: '평소보다 적음', tone: 'muted' }
}

export function formatNumber(value, digits = 4) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—'
  return Number(value).toFixed(digits)
}
