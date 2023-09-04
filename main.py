import cv2
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image
from package.MosaicEncoder import MosaicEncoder


if __name__ == '__main__':
    window = ttk.Window(themename="darkly")
    window.title("TK-CV2 TEST")
    window.resizable(False, False)
    window.geometry('1260x560')

    label1 = ttk.Label(window, text='CV2 TEST 2023-08-04 VIEW 1', font=('Arial', 10))
    label1.place(x=10, y=10)
    label11 = ttk.Label(window, text='CAMERA : ', font=('Arial', 10))
    label11.place(x=10, y=30)
    label2 = ttk.Label(window, text='CV2 TEST 2023-08-04 VIEW 2', font=('Arial', 10))
    label2.place(x=620, y=10)
    label21 = ttk.Label(window, text='TARGET : ', font=('Arial', 10))
    label21.place(x=620, y=30)
    # 프레임 추가
    frame1 = tk.Frame(window, bg="white", width=600, height=400)  # 프레임 너비, 높이 설정
    frame1.place(x=10, y=60)
    frame2 = tk.Frame(window, bg="white", width=600, height=400)  # 프레임 너비, 높이 설정
    frame2.place(x=620, y=60)

    # 라벨1 추가
    lbl1 = tk.Label(frame1)
    lbl1.grid()
    lbl2 = tk.Label(frame2)
    lbl2.grid()

    # 입력값(타겟)
    num1 = tk.StringVar()
    nin1 = tk.Entry(window, textvariable=num1)
    nin1.place(x=100, y=30)
    nin1.insert(0, "0")

    #입력값(타겟)
    num2 = tk.StringVar()
    nin2 = tk.Entry(window, textvariable=num2)
    nin2.place(x=700, y=30)
    nin2.insert(0, "0")

    def target_getter(number):
        try:
            if int(number) > 100:
                return 0
            else:
                return int(number)
        except:
            return 0


    # sel1 = tk.
    # todo 카메라 선택 UI 추가 해서 먼저 고를 수 있도록 변경
    cap = cv2.VideoCapture(target_getter(num1))
    mosaic = MosaicEncoder()
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