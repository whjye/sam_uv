import json

from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.parser import event_parser

from meteostat import Daily, Point

from models.event import WeatherHistoryEvent
from models.weather import WeatherDataList, WeatherDataRecord

logger = Logger()


@event_parser(model=WeatherHistoryEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: WeatherHistoryEvent, context: LambdaContext) -> dict:
    point = Point(
        lat=event.coordinates.latitude,
        lon=event.coordinates.longitude,
        alt=event.coordinates.altitude
    )

    start = event.datetime

    data = WeatherDataList(
        data=[WeatherDataRecord(**wdr) 
            for wdr 
            in (
                Daily(point, start, start)
                .fetch()
                .to_dict('records')
            )
        ]
    )

    return {
        "statusCode": 200,
        "body": json.dumps(data.model_dump())
    }
