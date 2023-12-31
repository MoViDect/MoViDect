import cv2
import numpy as np
import pyvirtualcam


class MosaicEncoder:
    def __init__(self):
        file_path = "encoding_test.mp4"
        fps = 25.40
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # 인코딩 포맷 문자
        self.frames = cv2.VideoWriter(file_path, fourcc, fps, (640, 480))
        self.cam = pyvirtualcam.Camera(width=640, height=480, fps=30)

    # intput: 이미지, 시작좌표(좌측상단) list, 끝좌표(우측하단) list, select변수
    # output: 모자이크 처리된 이미지
    # description: 이미지와 좌표, select변수를 입력받고
    #              좌표에 해당하는 모든 영역을 모자이크
    #              이 때, select 변수에 해당하는 영역은 모자이크 제외
    # target ( 모자이크 예외 필요한 인원 수 (기본갑 null))
    def makeBlur1(self, frame, xy1, xy2, target=None):
        img_w_mosaic = frame.copy()

        for i in range(len(xy1)):
            if i == (target - 1):
                continue
            mosaic_loc = frame[xy1[i][1]:xy2[i][1], xy1[i][0]:xy2[i][0]]
            mosaic_loc = cv2.blur(mosaic_loc, (50, 50))
            img_w_mosaic[xy1[i][1]:xy2[i][1], xy1[i][0]:xy2[i][0]] = mosaic_loc

        cv2.imshow("mosaic_test", img_w_mosaic)
        self.frames.write(img_w_mosaic)

    # intput: 이미지, 시작좌표(좌측상단) list, 끝좌표(우측하단) list, select변수
    # output: 모자이크 처리된 이미지
    # description: 위의 함수와 달리, 영역들을 size별로 정렬하고
    #              총 몇명까지 모자이크를 제외할 것인 지 확인하고
    #              size가 큰 순으로 제외하고 나머지 모자이크
    def makeBlur2(self, frame, xy1, xy2, target=None):
        img_w_mosaic = frame.copy()

        # TODO: 영역 사이즈 별로 정렬
        # 1. 좌표 통합
        new_xy_list = []
        for i in range(len(xy1)):
            new_xy_list.append((xy1[i], xy2[i]))

        # 2. 사이즈 확인
        size_list = []
        for i in range(len(xy1)):
            x = (xy1[i][0] - xy2[i][0])
            y = (xy1[i][1] - xy2[i][1])

            size_list.append(x * y)
        # print("2. ", size_list)

        # 3. 사이즈 오름차순 정렬
        size_sorted = np.sort(size_list)
        size_sorted_index = np.argsort(size_list)

        xy_sorted = [new_xy_list[i] for i in size_sorted_index]

        # 4. 뒤집어서 내림차순으로?
        xy_sorted = xy_sorted[::-1]
        for i, xys in enumerate(xy_sorted):
            print(i, xys)
            if i <= (target - 1):
                continue
            mosaic_loc = frame[xys[0][1]: xys[1][1], xys[0][0]: xys[1][0]]
            mosaic_loc = cv2.blur(mosaic_loc, (50, 50))
            img_w_mosaic[xys[0][1]: xys[1][1], xys[0][0]: xys[1][0]] = mosaic_loc

        img_w_mosaic = cv2.cvtColor(img_w_mosaic, cv2.COLOR_BGR2RGB)

        self.cam.send(img_w_mosaic)
        return img_w_mosaic

        # intput: 이미지, 시작좌표(좌측상단) list, 끝좌표(우측하단) list, select변수
        # output: 모자이크 처리된 이미지
        # description: 위의 함수와 달리, 영역들을 size별로 정렬하고
        #              총 몇명까지 모자이크를 제외할 것인 지 확인하고
        #              size가 큰 순으로 제외하고 나머지 모자이크

    def makeBlur3(self, frame, xy1, xy2, target=None):
        img_w_mosaic = frame.copy()

        # TODO: 영역 사이즈 별로 정렬
        # 1. 좌표 통합
        new_xy_list = []
        for i in range(len(xy1)):
            new_xy_list.append((xy1[i], xy2[i]))
        # print("1. ", new_xy_list)

        # 2. 사이즈 확인
        size_list = []
        for i in range(len(xy1)):
            x = (xy1[i][0] - xy2[i][0])
            y = (xy1[i][1] - xy2[i][1])

            size_list.append(x * y)
        # print("2. ", size_list)

        # 3. 사이즈 오름차순 정렬
        size_sorted = np.sort(size_list)
        size_sorted_index = np.argsort(size_list)

        xy_sorted = [new_xy_list[i] for i in size_sorted_index]
        # print("3. ", xy_sorted)

        # 4. 뒤집어서 내림차순으로?
        xy_sorted = xy_sorted[::-1]
        # print("4. ", xy_sorted)

        for i, xys in enumerate(xy_sorted):
            if i <= (target - 1):
                continue

            mosaic_loc = frame[xys[0][1]: xys[1][1], xys[0][0]: xys[1][0]]
            mosaic_loc2 = cv2.blur(mosaic_loc, (50, 50))
            temp_roi = np.zeros(shape=(mosaic_loc.shape[0], mosaic_loc.shape[1], 3), dtype=np.uint8)

            # 타원형
            cv2.ellipse(temp_roi,
                        (mosaic_loc.shape[1] // 2, mosaic_loc.shape[0] // 2),
                        (mosaic_loc.shape[1] // 2, mosaic_loc.shape[0] // 2),
                        0,
                        0,
                        360,
                        (255, 255, 255),
                        -1)
            temp_roi = cv2.bitwise_and(mosaic_loc2, temp_roi)

            cv2.ellipse(mosaic_loc,
                        (mosaic_loc.shape[1] // 2, mosaic_loc.shape[0] // 2),
                        (mosaic_loc.shape[1] // 2, mosaic_loc.shape[0] // 2),
                        0,
                        0,
                        360,
                        (0, 0, 0),
                        -1)

            mosaic_loc = cv2.bitwise_or(mosaic_loc, temp_roi)
            img_w_mosaic[xys[0][1]: xys[1][1], xys[0][0]: xys[1][0]] = mosaic_loc

            # cv2.imshow("temp", temp_roi)
            # cv2.imshow("1", mosaic_loc)
            # cv2.imshow("2", mosaic_loc2)
            # cv2.waitKey(0)

        img_w_mosaic = cv2.cvtColor(img_w_mosaic, cv2.COLOR_BGR2RGB)

        self.cam.send(img_w_mosaic)
        return img_w_mosaic
