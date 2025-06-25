from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectDetectionRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ObjectDetectionResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class DepthRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DepthResponse(_message.Message):
    __slots__ = ("depth_values", "timestamp", "x_coord", "y_coord")
    DEPTH_VALUES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    X_COORD_FIELD_NUMBER: _ClassVar[int]
    Y_COORD_FIELD_NUMBER: _ClassVar[int]
    depth_values: float
    timestamp: str
    x_coord: int
    y_coord: int
    def __init__(self, depth_values: _Optional[float] = ..., timestamp: _Optional[str] = ..., x_coord: _Optional[int] = ..., y_coord: _Optional[int] = ...) -> None: ...
