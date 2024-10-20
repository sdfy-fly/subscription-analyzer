from fastapi import FastAPI

from src.presentation.api.v1.user import router as user_router


def create_fastapi_app() -> FastAPI:
    app = FastAPI(
        title='Subscription Service',
        docs_url='/api/docs',
        debug=True
    )
    app.include_router(user_router, prefix='/api/v1/user', tags=['User'])

    return app
