# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a robotics thesis project that integrates computer vision with robotic manipulation using:
- **RealSense depth camera** for 3D object detection and distance measurement
- **UFACTORY xArm robot** for robotic manipulation
- **gRPC services** for distributed communication between camera and robot systems
- **YOLO11** for object detection and segmentation

## Architecture

The project is structured as three main modules:

### 1. realsense/
Contains camera-related services:
- `depth_camera.py`: RealSense D435i depth camera server with YOLO11 object detection
- `normal_camera.py`: Standard camera server for initial object detection
- Provides gRPC services for object detection and depth measurement

### 2. ufactory/
Robot control implementation:
- `xarm-implementation.py`: Main robot control logic that coordinates camera services
- Uses xArm Python SDK for robot manipulation
- Integrates with gRPC clients to communicate with camera services

### 3. grpc_cv_service/
gRPC service definitions and generated code:
- `protos/`: Protocol buffer definitions for camera services
- `depth_camera_service/`: Generated gRPC code for depth camera
- `normal_camera_service/`: Generated gRPC code for normal camera

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install local packages in development mode
pip install -e realsense/
pip install -e grpc_cv_service/
```

### Running Services

#### Start Depth Camera Server (RealSense)
```bash
cd realsense/
python depth_camera.py
# Runs on port 50051
```

#### Start Normal Camera Server
```bash
cd realsense/
python normal_camera.py
# Runs on port 50052
```

#### Run Robot Control
```bash
cd ufactory/
python xarm-implementation.py [robot_ip]
# Or configure robot.conf with xArm IP address
```

### Testing
```bash
# Test depth camera service
python grpc_cv_service/depth_camera_service/tests/server_test.py
python grpc_cv_service/depth_camera_service/tests/client_test.py

# Test normal camera
python realsense/tests/normal_camera_test.py
python realsense/tests/depth_camera_test.py

# Test robot configuration
python ufactory/tests/conf-test.py
```

### Development Workflow

1. **Camera Setup**: Requires USB 3.0+ connection for RealSense D435i camera
2. **Robot Configuration**: Configure robot IP in `ufactory/robot.conf` or pass as command line argument
3. **YOLO Model**: Default model path is `./realsense/yolo/yolo11n-seg.pt`
4. **Service Communication**:
   - Depth camera service: `localhost:50051`
   - Normal camera service: `localhost:50052`

## Key Implementation Notes

- The system uses object tracking with distance thresholds (default: 850mm) for manipulation decisions
- Robot performs 360° search pattern when objects are not detected in main camera view
- All camera services use YOLO11 for object detection and segmentation
- The project supports distributed deployment via gRPC for potential multi-machine setups

## Hardware Requirements

- Intel RealSense D435i depth camera
- UFACTORY xArm robotic arm
- USB 3.0+ ports for camera connectivity
- Compatible YOLO11 model weights for target objects