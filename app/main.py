
import logging
from utils.errors import ApiException
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from routes.route import api_router

from services.logs.set_logs import set_logger
# app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

#ログファイルを作成
_logger = logging.getLogger(__name__)
set_logger(_logger)

app = FastAPI()

# CORSを回避するために設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ApiException)
async def http_exception_handler(request: Request, exc: ApiException):
    """
    例外エラーハンドラー関数

    この関数がないと自作例外がfastAPI側でエラーとして扱われず500エラーとなる
    """
    return JSONResponse(
        status_code= exc.status_code,
        content={"status":exc.status,"detail":exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    FastAPIのHTTPリクエスト検証例外をオーバーライドして
    ログファイルに出力できるようにする
    
    以下の検証例外を400エラーとして返す
    ・422
    ・400
    ・その他

    """
    _logger.warning(f"request failed. status_code = 400 detail = {str(exc)}")
    return PlainTextResponse(str(exc), status_code=400)

app.include_router(api_router)


