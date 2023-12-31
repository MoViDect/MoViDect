import cv2
import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image
from package.MosaicEncoder import MosaicEncoder
from ultralytics import YOLO


model = YOLO('face.pt') # YOLO model Setting


def find_targets(frame):
    results = model.track(source=frame, save=False, save_txt=False, device=0, stream=True, classes=0, tracker='botsort.yaml')  # Yolo model Predict, Find Person Class Only

    for r in results:  # Only One Time
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
        return [xy1, xy2]

def select_camera(camera):
    if camera == "카메라 1":
        return 0
    elif camera == "카메라 2":
        return 1
    else:
        return 0


def increase_i():
    global target
    target += 1
    update_label()


def decrease_i():
    global target
    if target > 0:
        target -= 1
    update_label()


def update_label():
    label.config(text=f"target: {target}")
    if target == 0:
        decrease_button.config(state=tk.DISABLED)
    else:
        decrease_button.config(state=tk.NORMAL)


if __name__ == '__main__':
    target = 0
    window = ttk.Window(themename="darkly")
    window.title("MoviDict")
    path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    if os.path.isfile(path):
        window.iconbitmap(path)
    window.resizable(False, False)
    window.geometry('1520x560')

    # 틀 추가
    tframe1 = ttk.Labelframe(window, text="ORIGINAL (INPUT)", width=640, height=500)
    tframe1.place(x=10, y=30)
    tframe2 = ttk.Labelframe(window, text="OUTPUT", width=640, height=500, bootstyle="danger")
    tframe2.place(x=660, y=30)
    ctrlframe = ttk.Labelframe(window, text="CONTROL", width=250, height=500)
    ctrlframe.place(x=1320, y=30)

    # 프레임 추가 (웹캠및 출력 이미지 삽입 프레임)
    frame1 = tk.Frame(tframe1, bg="white", width=640, height=480)  # 프레임 너비, 높이 설정
    frame1.pack()
    frame2 = tk.Frame(tframe2, bg="white", width=640, height=480)  # 프레임 너비, 높이 설정
    frame2.pack()

    # 라벨1 추가
    lbl1 = tk.Label(frame1)
    lbl1.grid()
    lbl2 = tk.Label(frame2)
    lbl2.grid()

    # 입력값(카메라 선택)
    # label11 = ttk.Label(ctrlframe, text='CAMERA', font=('Arial', 10))
    # camera_combobox = ttk.Combobox(ctrlframe, values=["카메라 1", "카메라 2"])
    # camera_combobox.pack()

    #입력값(타겟)
    label = ttk.Label(ctrlframe, text=f"TARGET : {target}")
    label.pack(padx=20, pady=10)
    increase_button = ttk.Button(ctrlframe, text="+ Increase", command=increase_i)
    increase_button.pack(padx=20, pady=5)
    decrease_button = ttk.Button(ctrlframe, text="- Decrease", command=decrease_i)
    decrease_button.pack(padx=20, pady=5)

    cap = cv2.VideoCapture(select_camera(0))
    print(0)
    mosaic = MosaicEncoder()
    def target_getter(number):
        try:
            if int(number) > 100:
                return 0
            else:
                return int(number)
        except:
            return 0



    def run_mosic():
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return

        img = frame
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)  # Image 객체로 변환
        imgtk = ImageTk.PhotoImage(image=img)  # ImageTk 객체로 변환
        lbl1.imgtk = imgtk
        lbl1.configure(image=imgtk)

        # cv2.imshow("src", frame)
        # 현재 프레임과 함께 관심영역 시작좌표와 끝좌표 전달
        # 좌표 순서는
        # [(1x시작,1y시작), (2x,2y)...
        # [(1x끝,1y끝), (2x,2y)...
        target_axis = find_targets(frame)
        img_w_mosaic = mosaic.makeBlur3(frame,
                                       target_axis[0],
                                       target_axis[1],
                                       target = target_getter(target))

        img2 = img_w_mosaic
        img2 = Image.fromarray(img2)  # Image 객체로 변환
        imgtk2 = ImageTk.PhotoImage(image=img2)
        lbl2.imgtk = imgtk2
        lbl2.configure(image=imgtk2)

        lbl1.after(10, run_mosic)

    run_mosic()

    window.mainloop()