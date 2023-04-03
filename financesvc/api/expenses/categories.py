from fastapi import APIRouter
from starlette.responses import JSONResponse

from financesvc.domain.repositories import CategoryRepository
from financesvc.settings import DB_URL

router = APIRouter()
category_repo = CategoryRepository(DB_URL)


@router.get('/')
def get_expense_categories():
    categories = category_repo.get_categories()
    return JSONResponse(status_code=200, content=categories)
