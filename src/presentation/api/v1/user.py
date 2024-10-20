from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.commands.user import RegisterCommand
from src.application.commands.user.auth_user_command import AuthUserCommand
from src.application.exceptions.user import AuthException, UserNotFound
from src.application.mediator import Mediator
from src.application.queries.user import GetUserByIdQuery
from src.domain.entity.user import User
from src.domain.exceptions.base import DomainException
from src.presentation.dependencies import get_mediator
from src.presentation.schemas.user import (
    AuthUserRequest,
    AuthUserResponse,
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponse,
)


router = APIRouter()


@router.post(path='/', summary='Регистрация пользователя', status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest, mediator: Mediator = Depends(get_mediator)):
    command = RegisterCommand(
        username=request.username,
        password=request.password,
        email=request.email,
    )

    try:
        token: str = await mediator.handle_command(command)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return CreateUserResponse(token=token)


@router.post(path='/auth', summary='Авторизация пользователя')
async def auth_user(request: AuthUserRequest, mediator: Mediator = Depends(get_mediator)):
    command = AuthUserCommand(username=request.username, password=request.password)

    try:
        token: str = await mediator.handle_command(command)
    except AuthException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)

    return AuthUserResponse(token=token)


@router.get(path='/{user_id}', summary='Получить пользователя по id')
async def get_user_by_id(user_id: UUID, mediator: Mediator = Depends(get_mediator)):
    query = GetUserByIdQuery(user_id=user_id)

    try:
        user: User = await mediator.handle_query(query)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    return GetUserResponse(id=user.id, username=user.username.value, created_at=user.created_at)
