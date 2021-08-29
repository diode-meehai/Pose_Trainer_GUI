import cv2
import mediapipe as mp
import time
import math


class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)

        self.get_mediapipe_path()

    def get_mediapipe_path(self):
        mediapipe_path = mp.__path__[0]
        print('mediapipe_path: ', mediapipe_path)
        return mediapipe_path

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

    def findAngle_PON_right(self, img, p1, p2, p3, draw=True):

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle right
        angle_right = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle_right < 0:
            # angle += 360
            angle_right += 360

        # print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (255, 100, 100), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (255, 100, 100), 2)
            cv2.circle(img, (x2, y2), 10, (255, 100, 100), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 100, 100), 2)
            cv2.circle(img, (x3, y3), 10, (255, 100, 100), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 100, 100), 2)

            cv2.putText(img, str(int(angle_right)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        return angle_right


    def findAngle_PON_Left(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle Left
        angle_Left = math.degrees(math.atan2(x3 - x2, y3 - y2) -
                             math.atan2(x1 - x2, y1 - y2))

        if angle_Left < 0:
            angle_Left += 360

        # print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (100, 100, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (100, 100, 255), 2)
            cv2.circle(img, (x2, y2), 10, (100, 100, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (100, 100, 255), 2)
            cv2.circle(img, (x3, y3), 10, (100, 100, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (100, 100, 255), 2)

            cv2.putText(img, str(int(angle_Left)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        return angle_Left

    def PointBall_PON_LeftRight(self, img, Point_L1, Point_L2, Point_L3,draw=True):
        # Get the landmarks
        Point_x1_L, Pont_y1_L = self.lmList[Point_L1][1:]
        Point_x2_L, Pont_y2_L = self.lmList[Point_L2][1:]
        Point_x3_L, Pont_y3_L = self.lmList[Point_L3][1:]

        # Point_x1_R, Pont_y1_R = self.lmList[Point_R1][1:]
        # Ball_x1_R, Ball_y1_R = self.lmList[Ball_R][1:]

        # Calculate the Angle Left
        angle_Left = math.degrees(math.atan2(Point_x3_L - Point_x2_L, Pont_y3_L - Pont_y2_L) -
                                  math.atan2(Point_x1_L - Point_x2_L, Pont_y1_L - Pont_y2_L))
        # angle_Left = math.degrees(math.atan2(Ball_x1_L - Point_x1_L, Ball_y1_L - Pont_y1_L ))


        # angle_Right = math.degrees(math.atan2(Point_x1_R - Ball_x1_R, Pont_y1_R - Ball_y1_R))
        # angle_Right = math.degrees(math.atan2(Ball_x1_R - Point_x1_R, Ball_y1_R- Pont_y1_R))
        # angle_Right = math.degrees(math.atan2(Ball_y1_R - Pont_y1_R, Ball_x1_R - Point_x1_R))

        if angle_Left < 0:
            angle_Left += 360

        # if angle_Right < 0:
        #     angle_Right += 360

        if draw:
            cv2.line(img, (Point_x1_L, Pont_y1_L), (Point_x2_L, Pont_y2_L), (255, 0, 100), 5)
            cv2.line(img, (Point_x2_L, Pont_y2_L), (Point_x3_L, Pont_y3_L), (255, 0, 100), 5)

            cv2.circle(img, (Point_x2_L, Pont_y2_L), 20, (255, 0, 100), -1)

            cv2.putText(img, str(int(angle_Left)), (Point_x2_L - 50, Pont_y2_L + 50),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255,255, 255), 3)


        # return Left_x1, Left_y1, Right_x1, Right_y1
        return int(angle_Left)



def main():
    # cap = cv2.VideoCapture('PoseVideos/1.mp4')
    cap = cv2.VideoCapture(1)
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()