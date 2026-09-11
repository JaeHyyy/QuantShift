"""IndicatorSnapshot → Regime 판단.

지표 계산은 calculator에 두고, 여기서는 규칙만 적용한다.
임계값은 thresholds.py (초기값, 확정 전략 아님).
"""

from __future__ import annotations

from app.models.regime import IndicatorSnapshot, Regime
from app.regime import thresholds as T


class RegimeDetector:
    """지표 스냅샷으로 시장 상태 enum을 반환한다."""

    def detect(self, snap: IndicatorSnapshot) -> Regime:
        # 필수 지표가 없으면 판단 불가
        if (
            snap.adx is None
            or snap.ema_slope is None
            or snap.atr_ratio is None
        ):
            return Regime.UNKNOWN

        adx = snap.adx
        slope = snap.ema_slope
        atr_ratio = snap.atr_ratio

        # 1) 변동성이 정상 대비 지나치게 크면 HIGH_VOL 우선
        #    (초기값: ATR_HIGH_VOL_MIN — 확정 전략 아님)
        if atr_ratio >= T.ATR_HIGH_VOL_MIN:
            return Regime.HIGH_VOL

        # 2) 강한 추세 + 방향
        #    volume_ratio는 보조일 뿐, 여기서 상승/하락을 단독 결정하지 않음
        if adx >= T.ADX_TREND_MIN:
            if slope > T.EMA_SLOPE_FLAT_ABS:
                return Regime.UPTREND
            if slope < -T.EMA_SLOPE_FLAT_ABS:
                return Regime.DOWNTREND
            # ADX는 높은데 slope가 평평하면 애매 → UNKNOWN
            return Regime.UNKNOWN

        # 3) 약한 추세 + 평평한 EMA → 횡보 후보
        if adx <= T.ADX_RANGE_MAX and abs(slope) <= T.EMA_SLOPE_FLAT_ABS:
            return Regime.RANGE

        # 4) ADX 중간대(20~25) 또는 slope/ADX 조합이 애매하면 UNKNOWN
        return Regime.UNKNOWN
