from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExpenseDto(BaseModel):
    title: str
    amount: float
    category_id: int

    description: Optional[str | None] = ''
    spent_date: Optional[str | None] = datetime.now().strftime('%Y-%m-%d')
