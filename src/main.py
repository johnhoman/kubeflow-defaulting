import fastapi


from src import spark


api = fastapi.FastAPI()
api.include_router(spark.router, prefix="/spark")


@api.get("/healthz")
def health_check():
    pass
