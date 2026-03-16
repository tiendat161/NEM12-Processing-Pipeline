from dataclasses import dataclass
from datetime import datetime


@dataclass
class RecordSchema:
    nmi: str
    timestamp: datetime
    consumption: float
