#!/usr/bin/bash

DC="./depth_camera_service"
NC="./normal_camera_service"

python -m grpc_tools.protoc -I./protos --python_out=$DC --grpc_python_out=$DC --pyi_out=$DC ./protos/depth_camera.proto
python -m grpc_tools.protoc -I./protos --python_out=$NC --grpc_python_out=$NC --pyi_out=$NC ./protos/normal_camera.proto