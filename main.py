import cv2
from package.MosaicEncoder import MosaicEncoder

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # 0번 카메라 = 기본 카메라, 480 * 640 * 3
    mosaic = MosaicEncoder()

    while True:
        ret, frame = cap.read()  # 프레임 캡처
        if not ret:
            break

        # cv2.imshow("src", frame)
        # 현재 프레임과 함께 관심영역 시작좌표와 끝좌표 전달
        mosaic.makeBlur(frame,
                        [(200, 200), (100, 100)],
                        [(400, 400), (300, 300)])

        key = cv2.waitKey(25)
        if key == 27:  # Esc
            break

    del mosaic
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()