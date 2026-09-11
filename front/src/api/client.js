/**
 * API 베이스 URL.
 * - 개발: .env.development 의 VITE_API_BASE_URL (/api → Vite 프록시)
 * - 배포: .env 또는 환경변수로 실제 API 호스트 지정
 */
export function getApiBaseUrl() {
  const raw = import.meta.env.VITE_API_BASE_URL
  if (raw === undefined || raw === null || String(raw).trim() === '') {
    return '/api'
  }
  return String(raw).replace(/\/$/, '')
}

export async function apiGet(path) {
  const url = `${getApiBaseUrl()}${path.startsWith('/') ? path : `/${path}`}`
  const res = await fetch(url, {
    headers: { Accept: 'application/json' },
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail || JSON.stringify(body)
    } catch {
      // ignore
    }
    throw new Error(`API ${res.status}: ${detail}`)
  }
  return res.json()
}
