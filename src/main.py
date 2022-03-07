import fastapi
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator


from src import spark, profile


app = fastapi.FastAPI()
app.include_router(spark.router, prefix="/spark")
app.include_router(profile.router, prefix="/profile")

# something in this is throwing warnings
Instrumentator().instrument(app).expose(app, should_gzip=True)


class HealthCheck(BaseModel):
    ok: bool


@app.get("/healthz", response_model=HealthCheck)
def health_check():
    return HealthCheck(ok=True)
