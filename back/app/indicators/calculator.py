"""OHLCV → 지표 계산.

Regime 판단 로직은 여기에 넣지 않는다. 숫자만 계산한다.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

from app.models.ohlcv import OHLCV
from app.models.regime import IndicatorSnapshot
from app.regime import thresholds as T


def calculate_indicators(candles: Sequence[OHLCV]) -> IndicatorSnapshot:
    """캔들 리스트로 최신 IndicatorSnapshot을 만든다."""
    if len(candles) < T.MIN_CANDLES:
        return IndicatorSnapshot(
            adx=None,
            ema=None,
            ema_slope=None,
            atr=None,
            atr_ratio=None,
            volume_ratio=None,
        )

    closes = [c.close for c in candles]
    highs = [c.high for c in candles]
    lows = [c.low for c in candles]
    volumes = [c.volume for c in candles]

    ema_series = _ema(closes, T.EMA_PERIOD)
    atr_series = _atr(highs, lows, closes, T.ATR_PERIOD)
    adx_series = _adx(highs, lows, closes, T.ADX_PERIOD)

    ema_now = ema_series[-1]
    ema_slope = _ema_slope(ema_series, T.EMA_SLOPE_LOOKBACK)
    atr_now = atr_series[-1]
    atr_ratio = _ratio_vs_avg(atr_series, T.ATR_BASELINE_PERIOD)
    volume_ratio = _volume_ratio(volumes, T.VOLUME_AVG_PERIOD)
    adx_now = adx_series[-1]

    return IndicatorSnapshot(
        adx=_round_opt(adx_now),
        ema=_round_opt(ema_now),
        ema_slope=_round_opt(ema_slope, digits=8),
        atr=_round_opt(atr_now),
        atr_ratio=_round_opt(atr_ratio),
        volume_ratio=_round_opt(volume_ratio),
    )


def _round_opt(value: Optional[float], digits: int = 6) -> Optional[float]:
    if value is None:
        return None
    return round(value, digits)


def _ema(values: Sequence[float], period: int) -> List[Optional[float]]:
    """표준 EMA. 앞 period-1 구간은 None, seed는 SMA."""
    out: List[Optional[float]] = [None] * len(values)
    if len(values) < period:
        return out

    k = 2.0 / (period + 1)
    seed = sum(values[:period]) / period
    out[period - 1] = seed
    prev = seed
    for i in range(period, len(values)):
        prev = values[i] * k + prev * (1.0 - k)
        out[i] = prev
    return out


def _true_ranges(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
) -> List[float]:
    """True Range 시계열. 첫 봉은 high-low."""
    trs: List[float] = [highs[0] - lows[0]]
    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    return trs


def _wilder_smooth(values: Sequence[float], period: int) -> List[Optional[float]]:
    """Wilder smoothing (ADX/ATR에서 사용)."""
    out: List[Optional[float]] = [None] * len(values)
    if len(values) < period:
        return out

    seed = sum(values[:period]) / period
    out[period - 1] = seed
    prev = seed
    for i in range(period, len(values)):
        prev = (prev * (period - 1) + values[i]) / period
        out[i] = prev
    return out


def _atr(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    period: int,
) -> List[Optional[float]]:
    """Average True Range — 변동성."""
    return _wilder_smooth(_true_ranges(highs, lows, closes), period)


def _adx(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    period: int,
) -> List[Optional[float]]:
    """Average Directional Index — 추세 강도(방향은 DI로 따로 봄)."""
    n = len(closes)
    out: List[Optional[float]] = [None] * n
    if n < period * 2:
        return out

    plus_dm: List[float] = [0.0]
    minus_dm: List[float] = [0.0]
    trs = _true_ranges(highs, lows, closes)

    for i in range(1, n):
        up = highs[i] - highs[i - 1]
        down = lows[i - 1] - lows[i]
        plus_dm.append(up if up > down and up > 0 else 0.0)
        minus_dm.append(down if down > up and down > 0 else 0.0)

    atr_s = _wilder_smooth(trs, period)
    plus_s = _wilder_smooth(plus_dm, period)
    minus_s = _wilder_smooth(minus_dm, period)

    dx: List[Optional[float]] = [None] * n
    for i in range(n):
        if atr_s[i] is None or plus_s[i] is None or minus_s[i] is None:
            continue
        if atr_s[i] == 0:
            dx[i] = 0.0
            continue
        plus_di = 100.0 * (plus_s[i] / atr_s[i])
        minus_di = 100.0 * (minus_s[i] / atr_s[i])
        denom = plus_di + minus_di
        dx[i] = 0.0 if denom == 0 else 100.0 * abs(plus_di - minus_di) / denom

    # ADX = DX의 Wilder smooth. DX가 채워진 구간부터 period개로 seed
    first_dx = next((i for i, v in enumerate(dx) if v is not None), None)
    if first_dx is None:
        return out

    start = first_dx + period - 1
    if start >= n:
        return out

    seed_vals = [dx[i] for i in range(first_dx, first_dx + period) if dx[i] is not None]
    if len(seed_vals) < period:
        return out

    prev = sum(seed_vals) / period
    out[start] = prev
    for i in range(start + 1, n):
        if dx[i] is None:
            continue
        prev = (prev * (period - 1) + dx[i]) / period
        out[i] = prev
    return out


def _ema_slope(ema_series: Sequence[Optional[float]], lookback: int) -> Optional[float]:
    """EMA 상대 기울기. (now - past) / past.

    양수=상승, 음수=하락, 0 근처=평평.
    """
    if lookback <= 0 or len(ema_series) <= lookback:
        return None
    now = ema_series[-1]
    past = ema_series[-1 - lookback]
    if now is None or past is None or past == 0:
        return None
    return (now - past) / past


def _ratio_vs_avg(series: Sequence[Optional[float]], period: int) -> Optional[float]:
    """최신 값 / '직전 정상 구간' 평균.

    바로 직전 period는 이미 고변동일 수 있으므로,
    그 앞 period(vals[-(2*period):-period])를 기준으로 둔다.
    → 갑자기 커진 변동성(HIGH_VOL)을 잡기 위함.
    """
    vals = [v for v in series if v is not None]
    if len(vals) < period * 2:
        return None
    current = vals[-1]
    baseline = vals[-(period * 2) : -period]
    avg = sum(baseline) / len(baseline)
    if avg == 0:
        return None
    return current / avg


def _volume_ratio(volumes: Sequence[float], period: int) -> Optional[float]:
    """현재 거래량 / 최근 평균 거래량 (보조 정보)."""
    if len(volumes) < period + 1:
        return None
    current = volumes[-1]
    avg = sum(volumes[-(period + 1) : -1]) / period
    if avg == 0:
        return None
    return current / avg
