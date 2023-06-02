from ultralytics import YOLO
import package.MosaicEncoder as mosaicer
import cv2
import torch
import numpy as np

# Setting Variables
cap = cv2.VideoCapture(0) # WebCam Setting
model = YOLO('yolov8m.pt') # YOLO model Setting
mosaic = mosaicer.MosaicEncoder()

if __name__ == '__main__':
    while cap.isOpened():
        ret, frame = cap.read() # Read Frame from Capture Device

        results = model.predict(source=frame, save=False, save_txt=False, device=0, stream=True, classes=0) # Yolo model Predict, Find Person Class Only

        for r in results: # Only One Time
            r = r.cpu()
            r = r.numpy()
            xy1 = []
            xy2 = []
            try:
                for box in r.boxes:
                    find = box.data[0]
                    xy1.append((int(find[0]), int(find[1])))
                    xy2.append((int(find[2]), int(find[3])))
            except:
                pass
            mosaic.makeBlur(frame, xy1, xy2)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()