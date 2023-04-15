from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class BudgetDto(BaseModel):
    amount: float
    receive_date: date
    source_id: int
    notes: Optional[str] = None
