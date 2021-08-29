import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
import threading
import tkinter as tk
import time
# import imageio # pip install imageio
from Pose_Trainer import poseTrainer
import os


class poseTrainer_PushUpGUI():
    def __init__(self):

        self.root = tk.Tk()
        self.root.wm_title("Trainer Ai")
        self.root.geometry("1400x770")

        # videoloop_stop is a simple switcher between ON and OFF modes
        self.videoloop_stop = [False]

        # -------- poseTrainer ---------- #
        self.poseTrainer_run = poseTrainer()
        self.StartPushUp = False  # Pose

        self.StartPlank = False  # Plank
        self.StartSquat = False  # squat

        self.CheckTimeTrainer = True
        # -------- poseTrainer ---------- #

    def quit(self):
        os._exit(0)
        # self.root.quit()
        # sys.exit()

    def BTN_OpenCam(self, Camera):
        print('Camera: ', Camera)
        self.poseTrainer_run.ResetParameter()
        # threading.Thread(target=videoLoop, args=(self.videoloop_stop,)).start()
        threading.Thread(target=self.videoLoop, args=(True, Camera)).start()

    def BTN_StopCam(self):

        self.timeStart_sec = 5
        self.videoloop_stop[0] = True

        self.StartPushUp = False
        self.StartPlank = False
        self.StartSquat = False

    def BTN_StartPushUp(self):
        self.timeStart_sec = 5
        self.StartPushUp = True

    def BTN_StartPlank(self):
        self.timeStart_sec = 5
        self.StartPlank = True

    def BTN_StartSquat(self):
        self.timeStart_sec = 5
        self.StartSquat = True

    def CountDown(self):
        mins, secs = divmod(self.timeStart_sec, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        self.timeStart_sec -= 1

    def Check_Type_trainer(self, Img_to_draw):
        per_left, bar_left, per_right, bar_right = None, None, None, None
        color_bar_left = (0, 0, 0)
        color_bar_right = (0, 0, 0)

        count_left = ''
        count_right = ''

        if self.StartPushUp:
            Img_to_draw, per_left, bar_left, per_right, bar_right = self.poseTrainer_run.Detec_Position_PushUp(
                img=Img_to_draw)

            if bar_left is not None:
                color_bar_right, color_bar_left, count_left, count_right = \
                    self.poseTrainer_run.Check_per_angle_PushUp(per_right, per_left)
                count_left = int(count_left)
                count_right = int(count_right)

        elif self.StartPlank:
            Img_to_draw, per_left, bar_left, per_right, bar_right, timerPlank_count = \
                self.poseTrainer_run.Detec_Position_Plank(img=Img_to_draw)

            cv2.putText(Img_to_draw, str(timerPlank_count - 1), (500, 350), cv2.FONT_HERSHEY_PLAIN, 20, (255, 255, 0),
                        20)

            if bar_left is not None:
                self.button_stop.place_forget() #hide Button stop

                color_bar_right, color_bar_left, count_left, count_right = \
                    self.poseTrainer_run.Check_per_angle_Plank(per_right, per_left)
                count_left, count_right = 'X', 'X'

            if timerPlank_count <= 0:
                self.button_stop.place(x=1250, y=65, width=120, height=90) #Show Button stop
                self.BTN_StopCam()

        elif self.StartSquat:
            Img_to_draw = self.poseTrainer_run.Detec_Position_Squat(img=Img_to_draw)

        return Img_to_draw, bar_left, bar_right, per_left, per_right, color_bar_left, color_bar_right, count_left, count_right

    def videoLoop(self, mirror=False, Camera=0):
        # Camera = 'Test01.mp4'
        cap = cv2.VideoCapture(Camera)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, img_to_draw = cap.read()
            # if isinstance(to_draw, (np.ndarray, np.generic)):
            #     print(type(to_draw))

            if ret:
                # to_draw = to_draw[:, ::-1]
                img_to_draw = cv2.flip(img_to_draw, 1)

            if self.StartPushUp or self.StartPlank or self.StartSquat and ret:
                if self.timeStart_sec >= 0:
                    self.CountDown()
                    cv2.putText(img_to_draw, str(self.timeStart_sec + 1), (500, 350), cv2.FONT_HERSHEY_PLAIN, 20,
                                (0, 0, 255), 20)

                else:
                    img_to_draw, bar_left, bar_right, per_left, per_right, color_bar_left, \
                    color_bar_right, count_left, count_right = self.Check_Type_trainer(Img_to_draw=img_to_draw)

                    if bar_left is not None:
                        # ----------------- bar left % --------------------- #
                        cv2.rectangle(img_to_draw, (50, 120), (110, 650), color_bar_left, 3)
                        cv2.rectangle(img_to_draw, (50, int(bar_left)), (110, 650), color_bar_left, cv2.FILLED)
                        cv2.putText(img_to_draw, f'{int(per_left)}%', (50, 90), cv2.FONT_HERSHEY_PLAIN, 2,
                                    color_bar_left, 2)

                        cv2.rectangle(img_to_draw, (0, 5), (260, 50), (0, 0, 0), cv2.FILLED)
                        cv2.putText(img_to_draw, 'count left: ' + str(count_left), (6, 35), cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 200, 100),
                                    2)

                        # ----------------- bar left % --------------------- #

                        # ----------------- bar right % --------------------- #
                        cv2.rectangle(img_to_draw, (1190, 120), (1250, 650), color_bar_right, 3)
                        cv2.rectangle(img_to_draw, (1190, int(bar_right)), (1250, 650), color_bar_right, cv2.FILLED)
                        cv2.putText(img_to_draw, f'{int(per_right)}%', (1190, 90), cv2.FONT_HERSHEY_PLAIN, 2,
                                    color_bar_right, 2)

                        cv2.rectangle(img_to_draw, (1000, 5), (1280, 50), (0, 0, 0), cv2.FILLED)
                        cv2.putText(img_to_draw, 'count right: ' + str(count_right), (1010, 35), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 200, 100),
                                    2)
                        # ----------------- bar right % --------------------- #

            img_to_draw = cv2.resize(img_to_draw, (1080, 720))

            image = cv2.cvtColor(img_to_draw, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            panel = tk.Label(image=image)
            panel.image = image
            panel.place(x=10, y=20)

            # check switcher value
            if self.videoloop_stop[0]:
                # if switcher tells to stop then we switch it again and stop videoloop
                self.videoloop_stop[0] = False
                panel.destroy()
                break

    def Run_GIF(self):
        pushup_gif = cv2.VideoCapture('./img/pushup.gif')

        Squal_gif = cv2.VideoCapture('./img/Squal.gif')

        img_Plank = cv2.imread('./img/Plank.png')
        frame_gif = cv2.resize(img_Plank, (200, 100))
        img_Plank = cv2.cvtColor(frame_gif, cv2.COLOR_BGR2RGB)
        img_Plank = Image.fromarray(img_Plank)
        img_Plank = ImageTk.PhotoImage(img_Plank)
        panel = tk.Label(image=img_Plank)
        panel.image = img_Plank
        panel.place(x=1150, y=365)

        while True:
            _, frame_Squal = Squal_gif.read()
            ret, frame_Pushup = pushup_gif.read()
            if ret:
                frame_Pushup = cv2.resize(frame_Pushup, (200, 100))
                img_Pushup = cv2.cvtColor(frame_Pushup, cv2.COLOR_BGR2RGB)
                img_Pushup = Image.fromarray(img_Pushup)
                img_Pushup = ImageTk.PhotoImage(img_Pushup)
                panel = tk.Label(image=img_Pushup)
                panel.image = img_Pushup
                panel.place(x=1150, y=175)

                frame_Squal = cv2.resize(frame_Squal, (120, 200))
                img_Squal = cv2.cvtColor(frame_Squal, cv2.COLOR_BGR2RGB)
                img_Squal = Image.fromarray(img_Squal)
                img_Squal = ImageTk.PhotoImage(img_Squal)
                panel = tk.Label(image=img_Squal)
                panel.image = img_Squal
                panel.place(x=1120, y=550)

                time.sleep(0.1)
            else:
                time.sleep(1)
                pushup_gif.set(cv2.CAP_PROP_POS_FRAMES, 0)
                Squal_gif.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def RunGUI_BTN(self):
        # self.Run_GIF()
        RunGif = threading.Thread(target=self.Run_GIF, args=()).start()

        TextCam = tk.Label(self.root, text="Camera: ")
        TextCam.place(x=1120, y=15)
        TextBox = tk.Text(self.root, height=1, width=12)
        TextBox.pack()
        TextBox.place(x=1180, y=15, width=100, height=25)

        TextBox.insert(tk.END, '0')

        print('insert: ', str(TextBox.get("1.0", 'end-1c')))

        # Quit_btn = tk.Button(self.root, text="Quit", command=self.quit).pack()
        Quit_btn = tk.Button(
            self.root, text="Quit", bg="red", font=("", 20),
            command=lambda: self.quit())
        Quit_btn.place(x=1290, y=12, width=80, height=30)

        button_Opencam = tk.Button(
            self.root, text="Start\ncam", bg="#fff", font=("", 20),
            command=lambda: self.BTN_OpenCam(Camera=int(TextBox.get("1.0", 'end-1c'))))
            # command=lambda: self.BTN_OpenCam(Camera='./squat/squat2.mp4'))

        button_Opencam.place(x=1120, y=65, width=120, height=90)

        self.button_stop = tk.Button(
            self.root, text="Stop\ncam", bg="#fff", font=("", 20),
            command=lambda: self.BTN_StopCam())
        self.button_stop.place(x=1250, y=65, width=120, height=90)


        # ----------------- Trainer ---------------- #
        button_StartPushUp = tk.Button(
            self.root, text="Trainer PushUp", fg="#ffffff", bg="#1c6afc", font=("", 22),
            command=lambda: self.BTN_StartPushUp())
        button_StartPushUp.place(x=1120, y=285, width=250, height=50)

        button_StartPlank = tk.Button(
            self.root, text="Trainer Plank", fg="#ffffff", bg="#1c6afc", font=("", 22),
            command=lambda: self.BTN_StartPlank())
        button_StartPlank.place(x=1120, y=475, width=250, height=50)

        button_StartSquat = tk.Button(
            self.root, text="Trainer \nSquat", fg="#ffffff", bg="#1c6afc", font=("", 22),
            command=lambda: self.BTN_StartSquat())
        button_StartSquat.place(x=1250, y=552, width=120, height=200)
        # ----------------- Trainer ---------------- #

        self.root.mainloop()


if __name__ == "__main__":
    poseTrainer_PushUpGUI_RUN = poseTrainer_PushUpGUI()
    poseTrainer_PushUpGUI_RUN.RunGUI_BTN()
