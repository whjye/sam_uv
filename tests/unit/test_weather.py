import json
import os

import pytest
from weather import app

from tests.unit.lambda_context import LambdaTestContext


@pytest.fixture(scope="session")
def weather_event():
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "events/weather.json")) as f:
        return json.load(f)

def test_lambda_handler(weather_event):
    resp = app.lambda_handler(
        weather_event, LambdaTestContext(function_name="weather-fn")
    )
    resp_body = json.loads(resp["body"])

    assert resp["statusCode"] == 200

    columns = [
        "tavg",
        "tmin",
        "tmax",
        "prcp",
        "snow",
        "wdir",
        "wspd",
        "wpgt",
        "pres",
        "tsun",
    ]

    assert all(col in resp_body['data'][0] for col in columns)