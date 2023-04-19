from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from financesvc.api.routers import router
from financesvc.domain.repositories import UserRepository
from financesvc.settings import ALLOW_ORIGINS, DB_URL


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
    user_repo = UserRepository(DB_URL)
    for path in ALLOW_PATHS:
        if path in request.url.path:
            break
    else:
        code = request.headers.get('X-Token', '')
        matched_user = user_repo.get_user(code)
        request.state.user = matched_user
    response = await call_next(request)
    return response


app.include_router(router)
