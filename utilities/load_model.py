import torch
from ultralytics import YOLO

def load_model(model_path):
    """
    Loads a YOLO model onto the GPU if available, otherwise uses CPU
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} for YOLO inference")

    model = YOLO(model_path).to(device)
    return model, device