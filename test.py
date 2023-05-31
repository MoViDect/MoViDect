import cv2

Vid = cv2.VideoCapture('car.mp4')

if Vid.isOpened():
fps = Vid.get(cv2.CAP_PROP_FPS)
f_count = Vid.get(cv2.CAP_PROP_FRAME_COUNT)
f_width = round(Vid.get(cv2.CAP_PROP_FRAME_WIDTH))
f_height = round(Vid.get(cv2.CAP_PROP_FRAME_HEIGHT))


print('Frames per second: ', fps, 'FPS')
print('Frame count : ', f_count)
print('Frame width : ', f_width)
print('Frame height : ', f_height)

codec = "DIVX"
fourcc = cv2.VideoWriter_fourcc(*codec)
encoded_avi = cv2.VideoWriter("car_en.avi", fourcc, fps, (f_width, f_height))


while Vid.isOpened():
	ret, frame = Vid.read()
	if ret:
		key = cv2.waitKey(10)
        encoded_avi.write(frame)
        if key == ord('q'):
            break
        else:
            break


Vid.release()
cv2.destroyAllWindows()