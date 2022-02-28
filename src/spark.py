from fastapi import APIRouter, Depends
from kubernetes.client import V1Pod

from src import depends

router = APIRouter(tags=["spark"])


@router.post("/mutate-driver-core-v1-pod")
def spark_driver_defaults(pod: V1Pod = Depends(depends.pod)):
    pass
