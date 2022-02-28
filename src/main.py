import fastapi
from pydantic import BaseModel


from src import spark


app = fastapi.FastAPI()
app.include_router(spark.router, prefix="/spark")


class HealthCheck(BaseModel):
    ok: bool


@app.get("/healthz", response_model=HealthCheck)
def health_check():
    return HealthCheck(ok=True)
