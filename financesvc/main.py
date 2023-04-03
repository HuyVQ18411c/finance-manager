from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from financesvc.api.expenses import expenses, categories
from financesvc.api.users import users
from financesvc.settings import ALLOW_ORIGINS

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router, prefix='/categories', tags=['categories'])
app.include_router(expenses.router, prefix='/expenses', tags=['expenses'])
app.include_router(users.router, prefix='/users', tags=['users'])
