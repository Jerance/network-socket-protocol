from dataclasses import dataclass
from protocol.protocol_commons import Request, Response


@dataclass(kw_only=True)
class RequestError(Request):
    error_message: str


@dataclass(kw_only=True)
class ResponseError(Response):
    error_message: str
