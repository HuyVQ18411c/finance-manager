from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from financesvc.api.budgets import budgets
from financesvc.api.expenses import expenses, categories
from financesvc.api.users import users
from financesvc.domain.repositories import UserRepository
from financesvc.settings import ALLOW_ORIGINS, DB_URL


user_repo = UserRepository(DB_URL)

ALLOW_PATHS = [
    '/users/',
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def get_request_user(request: Request, call_next):
    for path in ALLOW_PATHS:
        if path in request.url.path:
            response = await call_next(request)
            break
    else:
        code = request.headers.get('X-Token', '')
        matched_user = user_repo.get_user(code)
        request.state.user = matched_user
        response = await call_next(request)
    return response

app.include_router(categories.router, prefix='/categories', tags=['categories'])
app.include_router(expenses.router, prefix='/expenses', tags=['expenses'])
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(budgets.router, prefix='/budgets', tags=['budgets'])
