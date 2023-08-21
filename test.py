import cv2
import mosaicEncoding

Vid = cv2.VideoCapture('car.mp4')


test_tuple1 = [(100, 100), (110, 110), (130, 130), (160, 160), (200, 200)]
test_tuple2 = [(110, 110), (130, 130), (160, 160), (200, 200), (250, 250)]

while True:
    ret, frame = cap.read()  # 프레임 캡처
    if not ret:
        break

    # cv2.imshow("src", frame)
    # 현재 프레임과 함께 관심영역 시작좌표와 끝좌표 전달
    mosaic.makeBlur(frame,
                    test_tuple1,
                    test_tuple2,
                    -1)

print('Frames per second: ', fps, 'FPS')
print('Frame count : ', f_count)
print('Frame width : ', f_width)
print('Frame height : ', f_height)

del mosaic
if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()
