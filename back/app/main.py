from fastapi import FastAPI, HTTPException

from app.indicators.calculator import calculate_indicators
from app.market.mock_provider import generate_mock_ohlcv
from app.models.regime import Regime
from app.regime.detector import RegimeDetector

app = FastAPI()
_detector = RegimeDetector()


@app.get("/")
def root():
    return {"message": "Frequant API is running"}


@app.get("/regime/mock/{scenario}")
def regime_from_mock(scenario: str):
    """Mock OHLCV로 Regime 파이프라인을 확인하는 개발용 엔드포인트.

    실제 거래소/주문과는 무관하다.
    """
    try:
        kind = Regime(scenario.upper())
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"scenario must be one of {[r.value for r in Regime if r != Regime.UNKNOWN]}",
        ) from exc

    if kind == Regime.UNKNOWN:
        raise HTTPException(status_code=400, detail="UNKNOWN mock is not supported")

    candles = generate_mock_ohlcv(kind)
    snap = calculate_indicators(candles)
    regime = _detector.detect(snap)
    return {
        "scenario": kind.value,
        "candles": len(candles),
        "indicators": {
            "adx": snap.adx,
            "ema": snap.ema,
            "ema_slope": snap.ema_slope,
            "atr": snap.atr,
            "atr_ratio": snap.atr_ratio,
            "volume_ratio": snap.volume_ratio,
        },
        "regime": regime.value,
    }
