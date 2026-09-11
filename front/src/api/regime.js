/**
 * 개발용 Regime Mock API.
 * 실제 거래소 Regime 조회와 분리해서 둔다.
 */
import { apiGet } from './client'

const MOCK_SCENARIOS = ['RANGE', 'UPTREND', 'DOWNTREND', 'HIGH_VOL']

export function listMockScenarios() {
  return [...MOCK_SCENARIOS]
}

/** @param {string} scenario RANGE | UPTREND | DOWNTREND | HIGH_VOL */
export function fetchRegimeFromMock(scenario) {
  return apiGet(`/regime/mock/${encodeURIComponent(scenario)}`)
}
