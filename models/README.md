# Models

The supplied GhostVision assets belong in this directory:

- `weights.onnx`
- `class_names.txt` (the actual class mapping: `Crab-Pot`)

Set `DETECTOR_TYPE=onnx` (the default) to activate REAL AI MODEL mode. The ONNX model has
input `images` float32 `[1,3,640,640]` and output `[1,5,8400]`; the adapter applies NMS and
maps boxes back to original-image coordinates. If loading fails, the app visibly switches to the
deterministic DEMO DETECTOR with the actual failure reason.

The older optional PyTorch adapter remains available with `DETECTOR_TYPE=pytorch`.

The expected model output format (see `backend/app/ai/pytorch_detector.py`) is a dict with
`boxes`, `scores`, and `labels` tensors, similar to torchvision detection models
(e.g. Faster R-CNN / RetinaNet output format).

If no weights file is found, or `torch` is not installed, or `DETECTOR_TYPE` is left at its
default (`demo`), the application automatically falls back to the built-in DEMO MODEL so the
entire workflow remains exercisable without any trained model.

The DEMO MODEL is a deterministic heuristic contour-based pseudo-detector intended for
development and UI/workflow testing only. Its outputs are NOT scientifically validated
predictions of debris type, location, or risk.
