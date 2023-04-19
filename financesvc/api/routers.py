from fastapi import APIRouter

from financesvc.api.budgets import budgets
from financesvc.api.expenses import categories, expenses
from financesvc.api.users import users


router = APIRouter()


router.include_router(categories.router, prefix='/categories', tags=['categories'])
router.include_router(expenses.router, prefix='/expenses', tags=['expenses'])
router.include_router(users.router, prefix='/users', tags=['users'])
router.include_router(budgets.router, prefix='/budgets', tags=['budgets'])
