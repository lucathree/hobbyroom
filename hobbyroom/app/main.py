import http
from fastapi import FastAPI, Response


app = FastAPI(
    title="Hobbyroom API",
    description="취미모임 프로젝트 API 서버",
)
app.get("/health-check", include_in_schema=False)(
    lambda: Response(status_code=http.HTTPStatus.OK)
)
