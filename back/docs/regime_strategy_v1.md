"""
# Regime 전략 메모 (v1) — 나중에 따로 볼 문서

> 이 파일은 **확정 투자 전략이 아니다.**
> 시장 상태(Regime) 판단 구조의 초기 기준값을 모아 둔 메모다.
> 백테스트·실데이터 검증 후 `app/regime/thresholds.py`와 함께 수정한다.

관련 코드:
- `app/regime/thresholds.py` — 실제 상수
- `app/regime/detector.py` — 판단 순서
- `app/indicators/calculator.py` — 지표 계산
- `app/market/mock_provider.py` — Mock OHLCV

---

## 1. Regime enum

| 값 | 의미 |
|----|------|
| RANGE | 횡보 |
| UPTREND | 상승 추세 |
| DOWNTREND | 하락 추세 |
| HIGH_VOL | 비정상적으로 큰 변동성 |
| UNKNOWN | 캔들 부족 또는 애매 |

---

## 2. 지표 역할

| 지표 | 역할 |
|------|------|
| ADX | 추세 **강도** (방향 X) |
| EMA / EMA slope | 가격 **방향** (상승/하락/평평) |
| ATR / atr_ratio | **변동성** (직전 정상 구간 ATR 대비 현재 ATR) |
| volume_ratio | **보조** 정보. 단독으로 상승/하락 결정 안 함 |

---

## 3. 현재 초기 기준값

코드 상수 (`thresholds.py`)와 동일:

- `EMA_PERIOD = 20`
- `ADX_PERIOD = 14`
- `ATR_PERIOD = 14`
- `VOLUME_AVG_PERIOD = 20`
- `ATR_BASELINE_PERIOD = 20`
- `EMA_SLOPE_LOOKBACK = 5`
- `ADX_RANGE_MAX = 20.0` — 이하면 횡보 후보
- `ADX_TREND_MIN = 25.0` — 이상이면 추세 후보
- `EMA_SLOPE_FLAT_ABS = 0.002` — slope 절대값이 이하면 평평
- `ATR_HIGH_VOL_MIN = 1.8` — atr_ratio 이상이면 HIGH_VOL
  - atr_ratio = 현재 ATR / (최근 2*period 중 **앞 period** 평균)
  - 바로 직전 구간이 이미 고변동일 수 있어, 그 앞 정상 구간과 비교
- `VOLUME_CONFIRM_MIN = 1.2` — 예비(현재 detector에서 미사용)
- `MIN_CANDLES = 50`

---

## 4. 판단 순서 (detector)

1. 필수 지표 없으면 → `UNKNOWN`
2. `atr_ratio >= ATR_HIGH_VOL_MIN` → `HIGH_VOL` (우선)
3. `adx >= ADX_TREND_MIN`
   - slope > flat → `UPTREND`
   - slope < -flat → `DOWNTREND`
   - 그 외 → `UNKNOWN`
4. `adx <= ADX_RANGE_MAX` 그리고 `|slope| <= flat` → `RANGE`
5. 나머지 → `UNKNOWN`

---

## 5. 나중에 손볼 포인트 (전략 튜닝)

- [ ] ADX / slope / ATR 임계값 백테스트
- [ ] HIGH_VOL을 추세보다 항상 우선할지 여부
- [ ] volume_ratio를 확신도 가중치로 쓸지
- [ ] 타임프레임(1m/5m/1h)별 threshold 분리
- [ ] 실제 거래소 OHLCV 어댑터 추가 후 Mock과 동일 파이프라인 검증
- [ ] Regime 전환 hysteresis (깜빡임 방지)

---

## 6. 아직 하지 않는 것

- 실주문 / Grid / Trend Following 매매
- 거래소 API 연결
- 수익 최적화
"""
