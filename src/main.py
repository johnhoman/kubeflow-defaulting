import fastapi
from fastapi import Depends
from kubernetes.client import V1Pod

from src import depends


api = fastapi.FastAPI()


@api.get("healthz")
def health_check():
    pass


@api.post("/mutate-spark-driver-core-v1-pod")
def spark_driver_defaults(pod: V1Pod = Depends(depends.pod)):
    pass