import cv2
import numpy as np
# import mediapipe as mp
import time
import PoseModule as pm
import threading


class poseTrainer():

    def __init__(self):
        self.detector = pm.poseDetector()
        # self.cap = cv2.VideoCapture(camera)
        self.ResetParameter()

    def ResetParameter(self):

        # ---------- PushUp --------- #
        self.count_right = 0
        self.dir_right = 0

        self.count_left = 0
        self.dir_left = 0
        # ---------- PushUp --------- #

        # ---------- Plank --------- #
        self.countdown_time = False
        self.TimePlankStart = False
        self.timerPlank_count = 30
        self.CheckPlank = 0
        # ---------- Plank --------- #

        # ---------- Squat --------- #
        self.countdown_TimeSquat = True
        self.TimeSquat = 5
        self.ScorSquat = 0
        # ---------- Squat --------- #

    def countdown_start(self, time_sec):
        for t in range(time_sec):
            mins, secs = divmod(t, 60)
            timer_p = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            t -= 1
            print(timer_p)
        self.countdown_time = True
        print('countdown_start')

    # ============================= PushUp ================================= #
    def Check_per_angle_PushUp(self, per_right, per_left):
        # ------------- right -------------- #
        color_bar_right = (255, 100, 100)
        if per_right == 100:
            color_bar_right = (0, 255, 255)
            if self.dir_right == 0:
                self.count_right += 0.5
                self.dir_right = 1
        if per_right == 0:
            color_bar_right = (0, 255, 255)
            if self.dir_right == 1:
                self.count_right += 0.5
                self.dir_right = 0
        # ------------- right -------------- #

        # ------------- left -------------- #
        color_bar_left = (100, 100, 255)
        if per_left == 100:
            color_bar_left = (0, 255, 255)
            if self.dir_left == 0:
                self.count_left += 0.5
                self.dir_left = 1
        if per_left == 0:
            color_bar_left = (0, 255, 255)
            if self.dir_left == 1:
                self.count_left += 0.5
                self.dir_left = 0
        # ------------- left -------------- #
        # print(self.count)
        return color_bar_right, color_bar_left, self.count_left, self.count_right

    def Detec_Position_PushUp(self, img):
        per_left, bar_left, per_right, bar_right = None, None, None, None
        img = cv2.resize(img, (1280, 720))
        # img = cv2.flip(img, 1)
        img = self.detector.findPose(img, draw=False)
        lmList = self.detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            angle_left = self.detector.findAngle_PON_Left(img, 12, 14, 16)  # ซ้าย
            per_left = np.interp(angle_left, (200, 260), (0, 100))  # %
            bar_left = np.interp(angle_left, (200, 260), (650, 100))  # bar %

            angle_right = self.detector.findAngle_PON_right(img, 11, 13, 15)  # ขวา
            per_right = np.interp(angle_right, (200, 260), (0, 100))  # %
            bar_right = np.interp(angle_right, (200, 260), (650, 100))  # bar %

        return img, per_left, bar_left, per_right, bar_right

    # ============================= PushUp ================================= #

    # ============================= Plank ================================= #
    def TimePlank_start(self):
        # global TimePlank_thread
        while self.timerPlank_count > 0:
            self.timerPlank_count -= 1
            time.sleep(1)
            print('TimePlank_start: ', self.timerPlank_count)
        # TimePlank_thread = threading.Timer(1, self.TimePlank_start)
        # TimePlank_thread.start()

    def Check_per_angle_Plank(self, per_right, per_left):
        # ------------- right -------------- #
        color_bar_right = (255, 100, 100)
        if per_right == 100:
            color_bar_right = (0, 255, 0)
        if per_right < 100:
            color_bar_right = (0, 0, 255)
        # ------------- right -------------- #

        # ------------- left -------------- #
        color_bar_left = (100, 100, 255)
        if per_left == 100:
            color_bar_left = (0, 255, 0)
        if per_left < 100:
            color_bar_left = (0, 0, 255)
        # ------------- left -------------- #
        # print(self.count)
        return color_bar_right, color_bar_left, None, None

    def Detec_Position_Plank(self, img):
        per_left, bar_left, per_right, bar_right = None, None, None, None
        img = cv2.resize(img, (1280, 720))
        # img = cv2.flip(img, 1)
        img = self.detector.findPose(img)
        lmList = self.detector.findPosition(img, True)

        if len(lmList) != 0:
            angle_left = self.detector.findAngle_PON_Left(img, 12, 14, 16)  # ซ้าย
            angle_right = self.detector.findAngle_PON_right(img, 11, 13, 15)  # ขวา

            if 190 < angle_left < 230 and 190 < angle_right < 230:
                self.CheckPlank = 0

                per_left = 100  # %
                bar_left = 100  # bar %

                per_right = 100  # %
                bar_right = 100  # bar %

                if not self.TimePlankStart:
                    TimePlank = threading.Thread(target=self.TimePlank_start, args=()).start()  #
                    # TimePlank.start()  #
                    # self.TimePlank_start()
                    self.TimePlankStart = True

            # if self.timerPlank_count <= 0:
            #     TimePlank.join()
            else:
                self.CheckPlank += 1
                # print(self.CheckPlank)
                if self.TimePlankStart and self.CheckPlank > 20 and self.timerPlank_count < 30:
                    print('stop', self.timerPlank_count)
                    self.timerPlank_count = self.timerPlank_count + 1
                    # time.sleep(0.5)
                    self.CheckPlank = 0

                per_left = 0  # %
                bar_left = 650  # bar %

                per_right = 0  # %
                bar_right = 650  # bar %

        return img, per_left, bar_left, per_right, bar_right, self.timerPlank_count

    # ============================= Plank ================================= #

    # ============================= squat ================================= #
    def TimeSquat_start(self):
        while self.TimeSquat > 0:
            self.TimeSquat -= 1
            print('self.TimeSquat: ', self.TimeSquat)
            time.sleep(1)


    def angle_squat(self, img, angle_Left):
        bar_left_per = 0
        color_bar = (0, 0, 255)
        if angle_Left < 280:
            # cv2.circle(img, (Ball_x1_L, Ball_y1_L), 15, (0, 0, 255), -1)
            per_left = np.interp(angle_Left, (196, 250), (0, 100))  # %
            # print('per_left: ', per_left)
            bar_left_per = np.interp(angle_Left, (196, 250), (650, 100))  # bar %
            # ------------- waist ball lef -------------- #
            if per_left == 100:
                color_bar = (0, 255, 0)

                if self.TimeSquat <= 0:
                    cv2.putText(img, "OK..UP", (300, 320), cv2.FONT_HERSHEY_PLAIN, 15,
                                (255, 0, 0), 15)
                else:
                    cv2.putText(img, str(self.TimeSquat), (410, 320), cv2.FONT_HERSHEY_PLAIN, 15,
                                (255, 255, 0), 15)
                if self.dir_left == 0:
                    self.ScorSquat += 0.5
                    self.dir_left = 1
                    # cv2.circle(img, (Ball_x1_L, Ball_y1_L), 30, color_track, -1)
                    # self.TimeSquat_start(img=img)
                    if self.TimeSquat == 5:
                        print('countdown_TimeSquat')
                        threading.Thread(target=self.TimeSquat_start, args=()).start()
                        # self.countdown_TimeSquat = False

            elif per_left == 0:
                color_bar = (0, 255, 0)
                if self.dir_left == 1:
                    self.ScorSquat += 0.5
                    self.dir_left = 0
                    self.TimeSquat = 5
                    # self.countdown_TimeSquat == True

        else:
            self.TimeSquat = 5
            cv2.putText(img, 'Too Low', (350, 320), cv2.FONT_HERSHEY_PLAIN, 10,
                        (0, 0, 255), 10)

        return color_bar, bar_left_per

    def Detec_Position_Squat(self, img):
        img = cv2.resize(img, (1280, 720))
        # img = cv2.flip(img, 1)
        img = self.detector.findPose(img, draw=False)
        lmList = self.detector.findPosition(img, False)

        if len(lmList) != 0:

            # --------- waist Left-------- #
            angle_Left = self.detector.PointBall_PON_LeftRight(
               img, Point_L1=26, Point_L2=24, Point_L3=12, draw=True)  # เอว ซ้าย/ขวา

            # if self.countdown_time:
            # threading.Thread(target=self.AddBall_Left, args=(img, angle_Left, Ball_x1, Ball_y1)).start()
            color_bar, bar_left_per = self.angle_squat(img, angle_Left)
            # ----------------- bar left % --------------------- #
            cv2.rectangle(img, (50, 120), (110, 650), color_bar, 3)
            cv2.rectangle(img, (50, int(bar_left_per)), (110, 650), color_bar, cv2.FILLED)

            cv2.rectangle(img, (0, 5), (240, 50), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, 'Squat: ' + str(int(self.ScorSquat)), (5, 35), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 200, 100),
                        2)
        return img

    # ============================= squat ================================= #

    # ------------------------- squat ------------------------------ #
    def loop_pose_Squat(self, camera=''):
        self.cap = cv2.VideoCapture(camera)
        countdown = threading.Thread(target=self.countdown_start, args=(5,))  # .start()  #
        countdown.start()

        # while self.countdown_time:
        while cv2.waitKey(1) < 0:
            success, img_read = self.cap.read()

            if success:
                img = self.Detec_Position_Squat(img=img_read)

            cv2.imshow("Image", img)
            cv2.waitKey(1)

            # return img
        else:
            time.sleep(1)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # ------------------------- squat ------------------------------ #

    # ------------------------- PushUp ------------------------------ #
    def loop_pose_PushUp(self, camera='Test01.mp4'):
        self.cap = cv2.VideoCapture(camera)
        countdown = threading.Thread(target=self.countdown_start, args=(3,)).start()  #
        pTime = 0
        while cv2.waitKey(1) < 0:
            success, img_read = self.cap.read()

            if success:
                img, per_left, bar_left, per_right, bar_right = self.Detec_Position_PushUp(img=img_read)

                if per_left is not None:
                    # ----------- Check_percen_angle ----------- #
                    if self.countdown_time:

                        color_bar_right, color_bar_left, self.count_left, self.count_right = \
                            self.Check_per_angle_PushUp(per_right, per_left)

                        # ----------------- bar left % --------------------- #
                        cv2.rectangle(img, (50, 120), (110, 650), color_bar_left, 3)
                        cv2.rectangle(img, (50, int(bar_left)), (110, 650), color_bar_left, cv2.FILLED)
                        cv2.putText(img, f'{int(per_left)}%', (50, 90), cv2.FONT_HERSHEY_PLAIN, 2, color_bar_left, 2)

                        cv2.rectangle(img, (0, 5), (240, 50), (0, 0, 0), cv2.FILLED)
                        cv2.putText(img, 'count left: ' + str(int(self.count_left)), (5, 35), cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 200, 100),
                                    2)

                        # ----------------- bar left % --------------------- #

                        # ----------------- bar right % --------------------- #
                        cv2.rectangle(img, (1190, 120), (1250, 650), color_bar_right, 3)
                        cv2.rectangle(img, (1190, int(bar_right)), (1250, 650), color_bar_right, cv2.FILLED)
                        cv2.putText(img, f'{int(per_right)}%', (1190, 90), cv2.FONT_HERSHEY_PLAIN, 2, color_bar_right,
                                    2)

                        cv2.rectangle(img, (1000, 5), (1250, 50), (0, 0, 0), cv2.FILLED)
                        cv2.putText(img, 'count right: ' + str(int(self.count_right)), (1010, 35),
                                    cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 200, 100),
                                    2)
                        # ----------------- bar right % --------------------- #

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime

                cv2.putText(img, str(int(fps)) + ' FPS', (650, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                            (255, 0, 0), 2)

                cv2.imshow("Image", img)
                cv2.waitKey(1)

            # return img
            else:
                time.sleep(1)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # ------------------------- PushUp ------------------------------ #

    # ------------------------- Plank ------------------------------ #
    def loop_pose_Plank(self, camera='Test01.mp4'):
        self.cap = cv2.VideoCapture(camera)
        countdown = threading.Thread(target=self.countdown_start, args=(3,))  # .start()  #
        countdown.start()
        pTime = 0

        # while self.countdown_time:
        while cv2.waitKey(1) < 0:
            success, img_read = self.cap.read()

            if success:
                img, per_left, bar_left, per_right, bar_right, timerPlank_count = self.Detec_Position_Plank(
                    img=img_read)

                if per_left is not None and timerPlank_count > 0:
                    # ----------- Check_percen_angle ----------- #
                    if self.countdown_time:
                        countdown.join()
                        color_bar_right, color_bar_left, count_left, count_right = self.Check_per_angle_Plank(per_right,
                                                                                                              per_left)

                        cv2.putText(img, str(self.timerPlank_count), (350, 330), cv2.FONT_HERSHEY_PLAIN, 10,
                                    (255, 255, 0), 10)
                        # ----------------- bar left % --------------------- #
                        cv2.rectangle(img, (50, 120), (110, 650), color_bar_left, 3)
                        cv2.rectangle(img, (50, int(bar_left)), (110, 650), color_bar_left, cv2.FILLED)
                        cv2.putText(img, f'{int(per_left)}%', (50, 90), cv2.FONT_HERSHEY_PLAIN, 2, color_bar_left, 2)

                        cv2.rectangle(img, (0, 5), (240, 50), (0, 0, 0), cv2.FILLED)
                        cv2.putText(img, 'count left: ' + str(int(self.count_left)), (5, 35), cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 200, 100),
                                    2)

                        # ----------------- bar left % --------------------- #

                        # ----------------- bar right % --------------------- #
                        cv2.rectangle(img, (1190, 120), (1250, 650), color_bar_right, 3)
                        cv2.rectangle(img, (1190, int(bar_right)), (1250, 650), color_bar_right, cv2.FILLED)
                        cv2.putText(img, f'{int(per_right)}%', (1190, 90), cv2.FONT_HERSHEY_PLAIN, 2, color_bar_right,
                                    2)

                        cv2.rectangle(img, (1000, 5), (1250, 50), (0, 0, 0), cv2.FILLED)
                        cv2.putText(img, 'count right: ' + str(int(self.count_right)), (1010, 35),
                                    cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 200, 100),
                                    2)
                        # ----------------- bar right % --------------------- #

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime

                cv2.putText(img, str(int(fps)) + ' FPS', (650, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                            (255, 0, 0), 2)

                cv2.imshow("Image", img)
                cv2.waitKey(1)

            # return img
            else:
                time.sleep(1)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # ------------------------- Plank ------------------------------ #


if __name__ == "__main__":
    poseTrainer_PushUp_run = poseTrainer()
    poseTrainer_PushUp_run.loop_pose_Squat(camera='./squat/squat2.mp4')
    # poseTrainer_PushUp_run.loop_pose_Squat(camera=1)

    # poseTrainer_PushUp_run.loop_pose_PushUp(camera=1)
    # poseTrainer_PushUp_run.loop_pose_PushUp(camera='./PushUp/PushUp01.mp4')

    # poseTrainer_PushUp_run.loop_pose_Plank(camera='./plank/Plank01.mp4')
    # poseTrainer_PushUp_run.loop_pose_Plank(camera=1)
    # poseTrainer_PushUp_run.loop_pose_Plank(camera='./plank/Test_plank_true.mp4')
    # poseTrainer_PushUp_run.loop_pose_Plank(camera='./plank/Plank_F.mp4')
