from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DepthRequest(_message.Message):
    __slots__ = ("depth_values", "x_coord", "y_coord")
    DEPTH_VALUES_FIELD_NUMBER: _ClassVar[int]
    X_COORD_FIELD_NUMBER: _ClassVar[int]
    Y_COORD_FIELD_NUMBER: _ClassVar[int]
    depth_values: float
    x_coord: int
    y_coord: int
    def __init__(self, depth_values: _Optional[float] = ..., x_coord: _Optional[int] = ..., y_coord: _Optional[int] = ...) -> None: ...
