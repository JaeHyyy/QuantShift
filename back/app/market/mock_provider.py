"""테스트용 Mock OHLCV 생성기.

완전히 랜덤이 아니라, 각 Regime의 가격 특성이 드러나도록 만든다.
실제 Indicator → Detector 경로를 검증하기 위한 데이터다.
(threshold에 맞춰 결과를 조작하지 않는다.)
"""

from __future__ import annotations

import math
from typing import List

from app.models.ohlcv import OHLCV
from app.models.regime import Regime


def generate_mock_ohlcv(
    scenario: Regime,
    candles: int = 120,
    start_price: float = 100.0,
    start_ts_ms: int = 1_700_000_000_000,
    interval_ms: int = 60_000,
) -> List[OHLCV]:
    """시나리오별 가상 OHLCV 리스트를 만든다."""
    if scenario == Regime.UNKNOWN:
        raise ValueError("UNKNOWN scenario is not supported for mock generation")
    if candles < 2:
        raise ValueError("candles must be >= 2")

    closes = _build_closes(scenario, candles, start_price)
    return _closes_to_ohlcv(closes, scenario, start_ts_ms, interval_ms)


def _build_closes(scenario: Regime, n: int, start: float) -> List[float]:
    """시나리오에 맞는 close 시계열을 만든다."""
    closes: List[float] = []

    if scenario == Regime.RANGE:
        # 좁고 빠른 진동 → 방향성 약함 (ADX↓, slope≈0)
        for i in range(n):
            wave = math.sin(i * 0.9) * 0.6 + math.sin(i * 1.7) * 0.25
            closes.append(start + wave)

    elif scenario == Regime.UPTREND:
        # 꾸준한 상승 + 작은 흔들림 → ADX↑, slope+
        price = start
        for i in range(n):
            drift = 0.35  # 봉당 상승
            wiggle = math.sin(i / 5.0) * 0.25
            price = price + drift + wiggle
            closes.append(price)

    elif scenario == Regime.DOWNTREND:
        # 꾸준한 하락 + 작은 흔들림 → ADX↑, slope-
        price = start
        for i in range(n):
            drift = -0.35
            wiggle = math.sin(i / 5.0) * 0.25
            price = price + drift + wiggle
            closes.append(price)

    elif scenario == Regime.HIGH_VOL:
        # 대부분 잔잔 → 마지막 구간만 급격한 출렁임
        # (직전 정상 ATR 대비 atr_ratio가 커지도록)
        quiet_until = int(n * 0.75)
        for i in range(n):
            if i < quiet_until:
                amp = 0.35
                swing = math.sin(i / 6.0) * amp
            else:
                step = i - quiet_until
                amp = 6.0 + step * 0.8
                swing = math.sin(step * 2.2) * amp + math.cos(step * 1.1) * amp * 0.7
            closes.append(start + swing)
    else:
        raise ValueError(f"unsupported scenario: {scenario}")

    return closes


def _closes_to_ohlcv(
    closes: List[float],
    scenario: Regime,
    start_ts_ms: int,
    interval_ms: int,
) -> List[OHLCV]:
    """close 시계열을 단순 OHLC + volume 봉으로 변환."""
    out: List[OHLCV] = []
    prev = closes[0]
    high_vol_start = len(closes) * 3 // 4

    for i, close in enumerate(closes):
        open_ = prev

        # 봉 내부 고저 / 거래량: 시나리오별 변동 폭 반영
        base_vol = 1000.0
        if scenario == Regime.HIGH_VOL and i >= high_vol_start:
            pad = abs(close - open_) * 0.5 + 2.0
            volume = base_vol * (3.0 + abs(math.sin(i)) * 2.0)
        elif scenario == Regime.RANGE:
            pad = 0.35
            volume = base_vol * (0.9 + abs(math.sin(i / 4.0)) * 0.2)
        elif scenario in (Regime.UPTREND, Regime.DOWNTREND):
            pad = abs(close - open_) * 0.25 + 0.2
            volume = base_vol * (1.1 + abs(math.sin(i / 3.0)) * 0.4)
        else:
            pad = abs(close - open_) * 0.25 + 0.2
            volume = base_vol

        high = max(open_, close) + pad
        low = min(open_, close) - pad

        out.append(
            OHLCV(
                timestamp=start_ts_ms + i * interval_ms,
                open=round(open_, 6),
                high=round(high, 6),
                low=round(low, 6),
                close=round(close, 6),
                volume=round(volume, 4),
            )
        )
        prev = close

    return out
