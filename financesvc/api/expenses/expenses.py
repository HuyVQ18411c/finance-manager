from fastapi import APIRouter
from starlette.responses import JSONResponse

from financesvc.api.expenses.dto import ExpenseDto
from financesvc.domain.repositories import ExpenseRepository, CategoryRepository
from financesvc.settings import DB_URL

router = APIRouter()
expense_repo = ExpenseRepository(DB_URL)


@router.get('/')
def get_all_expenses():
    return JSONResponse(status_code=200, content={})


@router.post('/')
def add_expense(expense_data: ExpenseDto):
    if not expense_data.title and not expense_data.amount and not expense_data.category_id:
        return {'error': True, 'detail': 'Missing required data.'}

    if expense_data.amount <= 0:
        return JSONResponse(status_code=400, content={'error': True, 'detail': 'Amount can not be smaller than 0.'})

    if isinstance(expense_data.created_by_id, int) and expense_data.created_by_id <= 0:
        return JSONResponse(status_code=400, content={'error': True, 'detail': 'Invalid expense creator.'})

    new_expense = expense_repo.create_expense(**expense_data.dict())

    return JSONResponse(status_code=201, content=new_expense)
