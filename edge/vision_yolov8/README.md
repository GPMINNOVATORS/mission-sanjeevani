# YOLOv8 Landing-Zone Detection (planned)

Status: **planned / under testing**.

Goal: detect a landing pad ("H" marker) and obstacles from the drone camera to support autonomous landing, with inference on Jetson Nano.
Suggested layout: `train/` (dataset config, training script), `infer/` (Jetson-optimised runtime, TensorRT export), `eval/` (metrics on held-out scenes).
