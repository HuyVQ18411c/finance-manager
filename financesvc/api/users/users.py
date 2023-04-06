import logging

from fastapi import APIRouter
from starlette.responses import JSONResponse

from financesvc.api.users.dto import UserDto, CreateUserDto
from financesvc.domain.repositories import UserRepository
from financesvc.settings import DB_URL
from financesvc.utils.utils import is_valid_email

logger = logging.getLogger(__name__)

router = APIRouter()
user_repo = UserRepository(DB_URL)


@router.post('/')
def create_new_user(data: CreateUserDto):
    if data.email and not is_valid_email(data.email):
        return JSONResponse(status_code=400, content={'error': {'email': 'Email không hợp lệ.'}})

    if user_repo.get_user(email=data.email):
        return JSONResponse(status_code=400, content={'error': {'email': 'Email đã tồn tại.'}})

    new_user = user_repo.create_user(
        email=data.email,
        password=data.password
    )

    logger.info('A new user created with code: %s', new_user['code'])

    return JSONResponse(
        status_code=201,
        content={
            'user_code': new_user['code'],
            'email': new_user['email']
        }
    )


@router.post('/ping')
def ping_user(data: UserDto):

    if not data.user_code and not data.email:
        return JSONResponse(status_code=400, content={'success': False})

    if data.email and not is_valid_email(data.email):
        return JSONResponse(status_code=400, content={'success': False})

    matched_user = user_repo.get_user(user_code=data.user_code, email=data.email)

    if matched_user:
        if matched_user.password:
            if matched_user.validate_password(data.password):
                return JSONResponse(
                    status_code=200,
                    content={
                        'success': True,
                        'email': matched_user.email,
                        'user_code': matched_user.code
                    }
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={
                        'success': False,
                        'error': {'password': 'Mật khẩu không hợp lệ.'}
                    }
                )
        else:
            return JSONResponse(
                status_code=200,
                content={
                    'success': True,
                    'email': matched_user.email,
                    'user_code': matched_user.code
                }
            )
    else:
        return JSONResponse(status_code=404, content={'success': False})

    return JSONResponse(status_code=400, content={'success': False})
