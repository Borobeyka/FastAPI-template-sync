import traceback

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

from app.api.routers.base import get_all_routers
from app.api.utils.logger import log_config
from app.config.secrets import ENV

app = FastAPI(
    title=ENV.get("FA_TITLE"),
    description=ENV.get("FA_DESCRIPTION"),
    version=ENV.get("FA_VERSION"),
)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(e, traceback.format_exc())
        return Response("Internal server error", status_code=500)


app.middleware("http")(catch_exceptions_middleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in get_all_routers():
    app.include_router(router)


def main():
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=int(ENV.get("FA_PORT")),
        timeout_keep_alive=10000,
        reload=ENV.get("FA_RELOAD") == "1",
        debug=ENV.get("FA_DEBUG") == "1",
        log_config=log_config,
    )


if __name__ == "__main__":
    main()
