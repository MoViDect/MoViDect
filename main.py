import cv2
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image
from package.MosaicEncoder import MosaicEncoder


def select_camera(camera):
    if camera == "카메라 1":
        return 0
    elif camera == "카메라 2":
        return 1
    else:
        return 0


if __name__ == '__main__':
    window = ttk.Window(themename="darkly")
    window.title("TK-CV2 TEST")
    window.resizable(False, False)
    window.geometry('1520x560')

    # 틀 추가
    tframe1 = ttk.Labelframe(window, text="ORIGINAL (INPUT)", width=640, height=500)
    tframe1.place(x=10, y=30)
    tframe2 = ttk.Labelframe(window, text="OUTPUT", width=640, height=500)
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
    label11 = ttk.Label(ctrlframe, text='CAMERA', font=('Arial', 10))
    camera_combobox = ttk.Combobox(ctrlframe, values=["카메라 1", "카메라 2"])
    camera_combobox.pack()

    #입력값(타겟)
    label21 = ttk.Label(ctrlframe, text='TARGET', font=('Arial', 10))
    label21.pack()
    num2 = tk.StringVar()
    nin2 = tk.Entry(ctrlframe, textvariable=num2)
    nin2.pack()
    nin2.insert(0, "0")

    cap = cv2.VideoCapture(select_camera(camera_combobox.get()))
    print(camera_combobox.get())
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
        img_w_mosaic = mosaic.makeBlur2(frame,
                                       xy1=[(300, 300), (100, 100), (400, 100)],
                                       xy2=[(400, 400), (300, 300), (550, 250)],
                                       target = target_getter(num2.get()))

        img2 = img_w_mosaic
        img2 = Image.fromarray(img2)  # Image 객체로 변환
        imgtk2 = ImageTk.PhotoImage(image=img2)
        lbl2.imgtk = imgtk2
        lbl2.configure(image=imgtk2)

        lbl1.after(10, run_mosic)

    run_mosic()

    window.mainloop()