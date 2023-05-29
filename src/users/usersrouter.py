from fastapi import APIRouter


router = APIRouter(prefix='/api/v1/users', tags=['Users'])


@router.get('/')
def get_users():
    return {'message': 'Users'}
