import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from financesvc.api.routers import router
from financesvc.domain.repositories import UserRepository
from financesvc.settings import ALLOW_ORIGINS, DB_URL

logger = logging.getLogger(__name__)

# Paths to skip custom middlewares
ALLOW_PATHS = [
    '/users/',
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown event"""
    logger.info('Application is starting up...')
    # Ensure all the database settings are set
    assert DB_URL is not None
    yield
    logger.info('Application is shutting down...')


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def get_request_user(request: Request, call_next):
    # This is not an efficient way to do this
    # Todo: do some thing more effective to pull user from database
    user_repo = UserRepository(DB_URL)
    for path in ALLOW_PATHS:
        if path in request.url.path:
            break
    else:
        code = request.headers.get('X-Token', '')
        matched_user = user_repo.get_user(code)
        logger.info('A user %s is using application', code)
        request.state.user = matched_user

    response = await call_next(request)
    return response


app.include_router(router)
