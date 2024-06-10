from mangum import Mangum
from src.app.app import app

lambda_handler = Mangum(app)
