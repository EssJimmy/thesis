```c
syntax = "proto3";
import "google/protobuf/empty.proto";
package depth_camera;

service DepthCamera {
    rpc SendDepthImage(DepthRequest) 
    returns (google.protobuf.Empty);
}

message DepthRequest {
    // Depth values in meters
    float depth_values = 1; 
    // How far is the object along the x-axis
    uint32 x_coord = 2; 
    // How far is the object along the y-axis
    uint32 y_coord = 3; 
}
```

```c
syntax = "proto3";
import "google/protobuf/empty.proto";
package normal_camera;

service NormalCamera {
    rpc ObjectDetection(ObjectDetectionRequest)
    returns (google.protobuf.Empty);
}

message ObjectDetectionRequest {
    // Identifier for the camera
    uint32 camera_id = 1; 
    // Indicates if the object detection was successful
    bool success = 2; 
}
```