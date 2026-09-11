"""Regime v1 파이프라인 테스트: Mock → Indicator → Detector."""

from app.indicators.calculator import calculate_indicators
from app.market.mock_provider import generate_mock_ohlcv
from app.models.regime import Regime
from app.regime.detector import RegimeDetector


def _run(scenario: Regime):
    candles = generate_mock_ohlcv(scenario, candles=120)
    snap = calculate_indicators(candles)
    regime = RegimeDetector().detect(snap)
    return candles, snap, regime


def test_range_mock_detects_range_or_reasonable():
    _, snap, regime = _run(Regime.RANGE)
    assert snap.adx is not None
    assert snap.ema_slope is not None
    # 횡보는 RANGE가 이상적. 애매하면 UNKNOWN도 허용(초기 threshold)
    assert regime in (Regime.RANGE, Regime.UNKNOWN)
    assert abs(snap.ema_slope) < 0.01


def test_uptrend_mock_detects_uptrend():
    _, snap, regime = _run(Regime.UPTREND)
    assert snap.adx is not None
    assert snap.ema_slope is not None and snap.ema_slope > 0
    assert regime == Regime.UPTREND


def test_downtrend_mock_detects_downtrend():
    _, snap, regime = _run(Regime.DOWNTREND)
    assert snap.adx is not None
    assert snap.ema_slope is not None and snap.ema_slope < 0
    assert regime == Regime.DOWNTREND


def test_high_vol_mock_detects_high_vol():
    _, snap, regime = _run(Regime.HIGH_VOL)
    assert snap.atr_ratio is not None
    assert regime == Regime.HIGH_VOL


def test_too_few_candles_returns_unknown():
    candles = generate_mock_ohlcv(Regime.UPTREND, candles=10)
    snap = calculate_indicators(candles)
    assert RegimeDetector().detect(snap) == Regime.UNKNOWN


def test_indicators_populated_on_enough_candles():
    candles = generate_mock_ohlcv(Regime.UPTREND, candles=120)
    snap = calculate_indicators(candles)
    assert snap.adx is not None
    assert snap.ema is not None
    assert snap.ema_slope is not None
    assert snap.atr is not None
    assert snap.atr_ratio is not None
    assert snap.volume_ratio is not None
