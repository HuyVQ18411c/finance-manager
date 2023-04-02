from datetime import datetime

from pydantic import BaseModel


class ExpenseDto(BaseModel):
    title: str
    amount: float
    category_id: int

    description: str | None = ''
    spent_date: str | None = datetime.now().strftime('%Y-%m-%d')
    created_by_id: int | None = None
    is_archived: bool | None = False
