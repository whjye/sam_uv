import json

from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext

from geopy.geocoders import Nominatim
from models.event import GeolocatorEvent
from models.geo import Coordinates

geolocator = Nominatim(user_agent="locator")
logger = Logger()


@event_parser(model=GeolocatorEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: GeolocatorEvent, context: LambdaContext) -> dict:
    address = event.address

    location = geolocator.geocode(address)

    coordinates = Coordinates(
        latitude=location.latitude,
        longitude=location.longitude
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "data": [
                    {
                        "coordinates": coordinates.model_dump()
                    }
                ],
            }
        ),
    }
