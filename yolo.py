from ultralytics import YOLO
import torch

print(torch.cuda.is_available()) # cuda 사용 가능 유무 확인 (True)

model = YOLO("yolov8m.pt")

results = model.predict(source="0", show=True, save=False, save_txt=False, device=0)