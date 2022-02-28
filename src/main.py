import fastapi


from src import spark


app = fastapi.FastAPI()
app.include_router(spark.router, prefix="/spark")


@app.get("/healthz")
def health_check():
    pass
