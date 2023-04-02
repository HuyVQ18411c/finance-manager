from fastapi import FastAPI

from financesvc.api.expenses import expenses
from financesvc.api.users import users


app = FastAPI()

app.include_router(expenses.router, prefix='/expenses', tags=['expenses'])
app.include_router(users.router, prefix='/users', tags=['users'])
