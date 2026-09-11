"""Regime 판단 초기 기준값 (v1).

중요:
- 아래 숫자는 확정된 투자 전략이 아니다.
- 구조·흐름 테스트용 초기값이다.
- 백테스트 후 thresholds만 바꿔서 조정하면 된다.
자세한 설명은 back/docs/regime_strategy_v1.md 참고.
"""

# --- 지표 lookback ---
EMA_PERIOD = 20
ADX_PERIOD = 14
ATR_PERIOD = 14
VOLUME_AVG_PERIOD = 20
ATR_BASELINE_PERIOD = 20  # atr_ratio: 직전 정상 구간(앞 period) 평균용
EMA_SLOPE_LOOKBACK = 5  # slope = (ema_now - ema_n봉전) / ema_n봉전

# --- Regime 임계값 (초기값) ---
# ADX: 추세 강도. 낮으면 횡보 후보, 높으면 추세 후보
ADX_RANGE_MAX = 20.0
ADX_TREND_MIN = 25.0

# EMA slope: 가격 방향. 절대값이 작으면 평평(횡보)
# close 대비 상대 변화율 (예: 0.002 = 0.2%)
EMA_SLOPE_FLAT_ABS = 0.002

# ATR ratio: 최근 정상 ATR 대비 현재 ATR이 얼마나 큰지
# 너무 크면 HIGH_VOL 후보
ATR_HIGH_VOL_MIN = 1.8

# Volume ratio: 보조 정보만. 단독으로 상승/하락을 결정하지 않음
# (나중에 확신도·필터용으로 쓸 수 있게 계산만 해둔다)
VOLUME_CONFIRM_MIN = 1.2

# 최소 캔들 수 (지표 warm-up 포함)
MIN_CANDLES = 50
