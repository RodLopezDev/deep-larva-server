"""
Lambda handler for the deep-larva-server
"""

import os

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from mangum import Mangum
from src.app.app import app

logger = Logger()
tracer = Tracer()
metrics = Metrics(namespace=os.getenv("POWERTOOLS_METRICS_NAMESPACE"))

fastapi_api_handler = Mangum(app)


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext):
    return fastapi_api_handler(event, context)  # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.app.app:app", host="0.0.0.0", port=8080, reload=True, workers=1)
