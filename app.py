import traceback

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.bot import send_telegram_error

from routes.users import users_router

app = FastAPI(
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        openapi_url='/api/openapi.json'
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        await send_telegram_error(traceback.format_exc())
        return Response("Internal server error", status_code=500)

# app.middleware('http')(catch_exceptions_middleware)

app.include_router(users_router, prefix='/api')