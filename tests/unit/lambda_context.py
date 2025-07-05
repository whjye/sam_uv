import uuid
from aws_lambda_powertools.utilities.typing import LambdaContext

class LambdaTestContext(LambdaContext):
    def __init__(self, function_name: str, version: str = "1", region: str = "us-east-1", account_id: str = "111122223333"):
        self._function_name = function_name
        self._function_version = version
        self._memory_limit_in_mb = 128
        self._invoked_function_arn = f"arn:aws:lambda:{region}:{account_id}:function:{function_name}:{version}"
        self._aws_request_id = str(uuid.uuid4())
        self._log_group_name = f"/aws/lambda/{function_name}"
        self._log_stream_name = str(uuid.uuid4())