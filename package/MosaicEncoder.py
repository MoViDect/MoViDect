import cv2


class MosaicEncoder:
    def __init__(self):
        file_path = "encoding_test.mp4"
        fps = 25.40
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # 인코딩 포맷 문자
        self.frames = cv2.VideoWriter(file_path, fourcc, fps, (640, 480))

    def makeBlur(self, frame, xy1, xy2):
        img_w_mosaic = frame.copy()
        for i in range(len(xy1)):
            mosaic_loc = frame[xy1[i][1]:xy2[i][1], xy1[i][0]:xy2[i][0]]
            mosaic_loc = cv2.blur(mosaic_loc, (50, 50))
            # cv2.imshow("mosaic_test" + str(i), mosaic_loc)
            img_w_mosaic[xy1[i][1]:xy2[i][1], xy1[i][0]:xy2[i][0]] = mosaic_loc

        return img_w_mosaic