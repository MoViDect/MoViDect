import cv2
import tkinter as tk
from PIL import ImageTk, Image
from package.MosaicEncoder import MosaicEncoder


if __name__ == '__main__':
    window = tk.Tk()
    window.title("TK-CV2 TEST")
    window.resizable(False, False)
    window.geometry('1200x450')

    label1 = tk.Label(window, text='CV2 TEST 2023-08-04 VIEW 1', font=('Arial', 10))
    label1.place(x=0, y=0)
    label2 = tk.Label(window, text='CV2 TEST 2023-08-04 VIEW 2', font=('Arial', 10))
    label2.place(x=600, y=0)
    # 프레임 추가
    frame1 = tk.Frame(window, bg="white", width=600, height=400)  # 프레임 너비, 높이 설정
    frame1.place(x=0, y=20)
    frame2 = tk.Frame(window, bg="white", width=600, height=400)  # 프레임 너비, 높이 설정
    frame2.place(x=600, y=20)

    # 라벨1 추가
    lbl1 = tk.Label(frame1)
    lbl1.grid()
    lbl2 = tk.Label(frame2)
    lbl2.grid()

    cap = cv2.VideoCapture(1)
    mosaic = MosaicEncoder()
    def run_mosic():
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return
        # cv2.imshow("src", frame)
        # 현재 프레임과 함께 관심영역 시작좌표와 끝좌표 전달
        img_w_mosaic = mosaic.makeBlur(frame,
                        [(200, 200), (100, 100)],
                        [(400, 400), (300, 300)])

        img = Image.fromarray(img_w_mosaic)  # Image 객체로 변환
        imgtk = ImageTk.PhotoImage(image=img)  # ImageTk 객체로 변환
        lbl1.imgtk = imgtk
        lbl1.configure(image=imgtk)

        img2 = Image.fromarray(frame)  # Image 객체로 변환
        imgtk2 = ImageTk.PhotoImage(image=img2)
        lbl2.imgtk = imgtk2
        lbl2.configure(image=imgtk2)
        lbl1.after(10, run_mosic)

    run_mosic()

    window.mainloop()