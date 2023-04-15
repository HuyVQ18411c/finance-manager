import calendar
from datetime import datetime, timedelta

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from financesvc.api.budgets.budgets import get_budgets_for_statistic
from financesvc.api.expenses.dto import ExpenseDto
from financesvc.domain.models import Expense
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
        # include_relationship=True
    ).to_representation()

    return JSONResponse(status_code=200, content=serialized_data)


@router.delete('/{expense_id}')
def delete_expense(request: Request, expense_id: int):
    user_code = request.state.user.code
    matched_expense = expense_repo.get_expense_by_id(expense_id, user_code)
    if not matched_expense:
        return JSONResponse(status_code=400, content={'error': True, 'detail': 'Không tìm thấy chi tiêu.'})

    expense_repo.delete_expense(matched_expense)

    return JSONResponse(status_code=200, content={'success': True})


@router.post('/')
def add_expense(expense_data: ExpenseDto, request: Request):
    if not expense_data.title and not expense_data.amount and not expense_data.category_id:
        return JSONResponse(status_code=400, content={'error': True, 'detail': 'Dữ liệu không hợp lệ.'})

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


def get_expenses_for_statistic(user_code: str) -> dict[str, dict]:
    expenses = expense_repo.get_expenses(user_code)

    data = {'bar': {}, 'line': {}, 'pie': {}}
    days = (expenses[-1].spent_date - expenses[0].spent_date).days

    for i in range(days + 1):
        # Create initial amount for each day
        data['line'][(expenses[0].spent_date + timedelta(days=i)).strftime('%d-%m')] = 0

    for k in range(expenses[0].spent_date.month, 13):
        data['bar'][calendar.month_abbr[k]] = 0

    for expense in expenses:
        # Spent amount collected by category
        if not data['pie'].get(expense.category.name, None):
            data['pie'][expense.category.name] = expense.amount
        else:
            data['pie'][expense.category.name] += expense.amount

        # Spent amount collected by day
        if not data['line'].get(str(expense.spent_date.strftime('%d-%m')), None):
            data['line'][str(expense.spent_date.strftime('%d-%m'))] = expense.amount
        else:
            data['line'][str(expense.spent_date.strftime('%d-%m'))] += expense.amount

        # Spent amount by month
        data['bar'][calendar.month_abbr[expense.spent_date.month]] += expense.amount

    return data


@router.get('/statistic/')
def get_dashboard(request: Request):
    user = request.state.user

    data = {'expenses': {}, 'budgets': {}}

    expense_data = get_expenses_for_statistic(user.code)
    budget_data = get_budgets_for_statistic(user.code)

    data['expenses'] = expense_data
    data['budgets'] = budget_data

    return JSONResponse(status_code=200, content=data)
