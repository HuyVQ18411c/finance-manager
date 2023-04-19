import calendar

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from financesvc.api.budgets.dto import BudgetDto
from financesvc.domain.repositories import BudgetRepository, MoneySourceRepository
from financesvc.settings import DB_URL
from financesvc.utils.serializers import Serializer

router = APIRouter()
budget_repo = BudgetRepository(DB_URL)
money_source_repo = MoneySourceRepository(DB_URL)


@router.post('/')
def create_new_budget(request: Request, data: BudgetDto):
    if not all([data.source_id, data.amount, data.receive_date]):
        return JSONResponse(status_code=400, content={'success': False, 'detail': 'Dữ liệu không hợp lệ.'})

    matched_source = money_source_repo.get_source_by_id(data.source_id)
    if not matched_source:
        return JSONResponse(status_code=400, content={'success': False, 'detail': 'Nguồn tiền không hợp lệ.'})

    new_budget = budget_repo.create_budget(
        amount=data.amount,
        source_id=data.source_id,
        receive_date=data.receive_date,
        created_by_id=request.state.user.code
    )

    return JSONResponse(status_code=201, content=Serializer(data=new_budget).to_representation())


@router.get('/')
def get_budget(request: Request):
    user_code = request.state.user.code
    budgets = budget_repo.get_budgets(user_code)

    return JSONResponse(
        status_code=200,
        content=Serializer(
            data=budgets,
            include_relationship=True,
            exclude_fields=['created_by']
        ).to_representation()
    )


def get_budgets_for_statistic(user_code):
    budgets = budget_repo.get_budgets(user_code)

    data = {'bar': {}}

    for k in range(budgets[0].receive_date.month, 13):
        data['bar'][calendar.month_abbr[k]] = 0

    for budget in budgets:
        data['bar'][calendar.month_abbr[budget.receive_date.month]] += budget.amount
    return data
