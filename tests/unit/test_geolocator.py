import json
import os

import pytest

from geolocator import app
from tests.unit.lambda_context import LambdaTestContext


@pytest.fixture(scope="session")
def geolocator_event():
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "events/geolocator.json")) as f:
        return json.load(f)

def test_lambda_handler(geolocator_event):

    resp = app.lambda_handler(geolocator_event, LambdaTestContext("geolocator-fn"))
    resp_body = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    
    columns = [
        "latitude",
        "longitude",
    ]

    print(resp_body)

    assert all(col in resp_body['data'][0]['coordinates'] for col in columns)
    