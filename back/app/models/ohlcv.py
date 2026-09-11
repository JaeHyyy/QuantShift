"""거래소와 독립적인 OHLCV 캔들 모델.

실제 Bithumb 등 API를 붙일 때도 이 형태로 변환해서 쓰면 된다.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class OHLCV:
    """한 봉(캔들)의 Open / High / Low / Close / Volume."""

    timestamp: int  # unix ms (거래소 공통 포맷에 맞춤)
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self) -> None:
        # 잘못된 봉이 지표 계산을 깨지 않도록 최소 검증
        if self.high < self.low:
            raise ValueError("high must be >= low")
        if self.volume < 0:
            raise ValueError("volume must be >= 0")
