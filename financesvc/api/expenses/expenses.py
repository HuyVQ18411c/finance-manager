from datetime import datetime

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from financesvc.api.expenses.dto import ExpenseDto
from financesvc.domain.repositories import ExpenseRepository, CategoryRepository
from financesvc.settings import DB_URL
from financesvc.utils.serializers import Serializer

EXPENSE_EXCLUDE_FIELDS = ['created_date', 'last_updated_date']

router = APIRouter()
expense_repo = ExpenseRepository(DB_URL)
category_repo = CategoryRepository(DB_URL)


@router.get('/')
def get_expenses(request: Request):
    data = expense_repo.get_expenses(request.state.user.code)
    serialized_data = Serializer(
        data,
        exclude_fields=EXPENSE_EXCLUDE_FIELDS,
        include_relationship=True
    ).to_representation()

    return JSONResponse(status_code=200, content=serialized_data)


@router.get('/{expense_id}')
def delete_expense(request: Request):
    pass


@router.post('/')
def add_expense(expense_data: ExpenseDto, request: Request):
    if not expense_data.title and not expense_data.amount and not expense_data.category_id:
        return JSONResponse(status_code=400, content={'error': True, 'detail': 'Missing required data.'})

    if expense_data.amount <= 0:
        return JSONResponse(status_code=400, content={'error': True, 'detail': 'Amount can not be smaller than 0.'})

    expense_data.spent_date = datetime.strptime(expense_data.spent_date, '%Y-%m-%d')
    new_expense = expense_repo.create_expense(**expense_data.dict(), created_by_id=request.state.user.id)

    return JSONResponse(
        status_code=201,
        content=Serializer(
            new_expense,
            exclude_fields=EXPENSE_EXCLUDE_FIELDS
        ).to_representation()
    )


@router.get('/statistic/')
def get_dashboard(request: Request):
    user = request.state.user
    expenses = expense_repo.get_expenses(user.code)

    data = {'bar': {}, 'line': {}}

    # Collect data for bar chart
    for expense in expenses:
        # Spent amount collected by category
        if not data['bar'].get(expense.category.name, None):
            data['bar'][expense.category.name] = expense.amount
        else:
            data['bar'][expense.category.name] += expense.amount

        # Spent amount collected by day
        if not data['line'].get(str(expense.spent_date.strftime('%d-%m')), None):
            data['line'][str(expense.spent_date.strftime('%d-%m'))] = expense.amount
        else:
            data['line'][str(expense.spent_date.strftime('%d-%m'))] += expense.amount

    return JSONResponse(status_code=200, content=data)
