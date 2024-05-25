- virtualenv onnx_maker
- source onnx_maker/bin/activate
- pip install -r requirements.txt
- bash export-to-onnx.sh fire_model.pt fire_model.onnx 640
- python complete_onnx.py
- python test_onnx.py
  ```text
  2024-05-25 18:40:27.258792260 [W:onnxruntime:, execution_frame.cc:858 VerifyOutputSizes] Expected shape from model of {20,6} does not match actual shape of {1,6} for output bboxes-format:xyxysc;0:Fire;1:default;2:smoke
  0: 0.7942758798599243
  (6, 1), (636, 640)
  ```  
