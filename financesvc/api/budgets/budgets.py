from fastapi import APIRouter, Request


router = APIRouter()


@router.post('/')
def create_new_budget(request: Request):
    pass


@router.get('/')
def get_budget(request: Request):
    pass
