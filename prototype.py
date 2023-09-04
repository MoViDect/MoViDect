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
model = YOLO('yolov8m.pt') # YOLO model Setting
mosaic = mosaicer.MosaicEncoder()

# Setting MediaPipe
base_options = python.BaseOptions(model_asset_path='detector.tflite')
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)


def find_targets():
    results = model.predict(source=frame, save=False, save_txt=False, device=0, stream=True,
                            classes=0)  # Yolo model Predict, Find Person Class Only
    for r in results:  # Only One Time
        r = r.cpu()
        r = r.numpy()
        xy1 = []
        xy2 = []
        try:
            for box in r.boxes:
                find = box.data[0]
                face_frame = frame[int(find[1]):int(find[3]), int(find[0]):int(find[2])].astype(np.uint8)
                mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=face_frame)
                face_detector_result = detector.detect(mp_img)

                for detection in face_detector_result.detections:
                    bbox = detection.bounding_box
                    print(bbox)
                    xy1.append((int(find[0]) + bbox.origin_x, int(find[1]) + bbox.origin_y))
                    xy2.append((int(find[0]) + bbox.origin_x + bbox.width, int(find[1]) + bbox.origin_y + bbox.height))
        except Exception as e:
            print(e)
        mosic_frame = mosaic.makeBlur2(frame, xy1, xy2, 0)
    return mosic_frame


if __name__ == '__main__':
    while cap.isOpened():
        ret, frame = cap.read() # Read Frame from Capture Device
        mosic_frame = find_targets()
        cv2.imshow('frame', mosic_frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()