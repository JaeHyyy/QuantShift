"""시장 상태(Regime)와 지표 스냅샷 모델."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Regime(str, Enum):
    """현재 시장 상태. 매매 전략이 아니라 '상태 분류'용."""

    RANGE = "RANGE"
    UPTREND = "UPTREND"
    DOWNTREND = "DOWNTREND"
    HIGH_VOL = "HIGH_VOL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class IndicatorSnapshot:
    """Regime 판단에 쓰는 최신 지표 묶음.

    None 이면 캔들 부족 등으로 아직 계산 불가.
    """

    adx: Optional[float]
    ema: Optional[float]
    ema_slope: Optional[float]
    atr: Optional[float]
    atr_ratio: Optional[float]  # 현재 ATR / 최근 ATR 평균
    volume_ratio: Optional[float]  # 현재 volume / 최근 volume 평균
