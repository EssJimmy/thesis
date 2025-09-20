from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectDetectionRequest(_message.Message):
    __slots__ = ("camera_id", "success")
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    camera_id: int
    success: bool
    def __init__(self, camera_id: _Optional[int] = ..., success: bool = ...) -> None: ...
