from ultralytics import YOLO
import package.MosaicEncoder as mosaicer
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import torch
import numpy as np

# Setting Variables
cap = cv2.VideoCapture(0) # WebCam Setting
model = YOLO('yolov8n.pt') # YOLO model Setting
face_model = YOLO('face.pt')
mosaic = mosaicer.MosaicEncoder()

# Setting MediaPipe
# base_options = python.BaseOptions(model_asset_path='detector.tflite')
# options = vision.FaceDetectorOptions(base_options=base_options)
# detector = vision.FaceDetector.create_from_options(options)

if __name__ == '__main__':
    while cap.isOpened():
        ret, frame = cap.read() # Read Frame from Capture Device

        # results = model.predict(source=frame, save=False, save_txt=False, device=0, stream=True, classes=0) # Yolo model Predict, Find Person Class Only
        results = face_model.track(source=frame, save=False, save_txt=False, device=0, stream=True, classes=0, tracker='botsort.yaml') # Yolo model Predict, Find Person Class Only

        for r in results: # Only One Time
            r = r.cpu()
            r = r.numpy()
            print(r.boxes.data)
            print(r.boxes.is_track)
            xy1 = []
            xy2 = []
            try:
                for box in r.boxes:
                    find = box.data[0]

                    # 설정한 인물이 모자이크 안되게 하는 부분 (트랙킹)
                    # if find[4]==1:
                    #     continue

                    xy1.append((int(find[0]), int(find[1])))
                    xy2.append((int(find[2]), int(find[3])))

            except Exception as e:
                print(e)
            mosaic.makeBlur(frame, xy1, xy2)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()