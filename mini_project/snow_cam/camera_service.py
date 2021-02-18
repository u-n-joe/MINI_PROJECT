import threading
import os
import cv2
import time
from PIL import Image
from PIL import ImageTk

def preview_th(stop, app, effect=None):
    cam = cv2.VideoCapture(0)
    while stop():
        ret, frame = cam.read()
        if ret:
            app.change_img1(frame, effect)
            cv2.waitKey(0)
    cam.release()


def slide_th(stop, app, flist):  # 슬라이드
    while 1:
        for i in flist:
            if stop() == False:  # ()를 써주면 동기화처리를 해주기때문에 쓴다.
                # stop의 boolean값을 하나씩 받아와서 확인해야 하기 때문에 동기화가 필요
                return
            img = cv2.imread('img/' + i)
            app.change_img(img)
            time.sleep(3)


def video_th(stop, app, fname):  # 동영상 저장
    cam = cv2.VideoCapture(0)
    codec = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('video/' + fname, codec, 25.0, (640, 480))

    while stop():
        ret, frame = cam.read()
        if ret:
            out.write(frame)
            app.change_img(frame)
            cv2.waitKey(0)
    cam.release()
    out.release()


def vv_th(stop, app, fname):  # 검색한 동영상 재생
    cap = cv2.VideoCapture('video/' + fname)
    while stop():
        ret, frame = cap.read()
        if ret == False:
            break
        app.change_img(frame)
        cv2.waitKey(13)
    cap.release()

class CameraService:
    def __init__(self, app):
        self.cam = None
        self.app = app
        self.flag = True

    def stop(self):
        self.flag = False

    def preview(self):
        self.flag = True
        cam_th = threading.Thread(target=preview_th, args=(lambda: self.flag, self.app))
        cam_th.start()

    def capture(self, fname):
        self.stop()
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640)
        self.cam.set(4, 400)
        ret, frame = self.cam.read()
        self.app.change_img1(frame)
        cv2.imwrite('img/' + fname, frame)
        self.cam.release()
        print('사진저장완료')

    def videoStart(self, fname):
        self.flag = True
        cam_th = threading.Thread(target=video_th, args=(lambda: self.flag, self.app, fname))
        cam_th.start()

    def view_img(self, fname):
        img = cv2.imread('img/' + fname)
        self.app.change_img1(img)

    def view_video(self, fname):
        self.flag = True
        a = threading.Thread(target=vv_th, args=(lambda: self.flag, self.app, fname))
        a.start()

    def slideOn(self):
        flist = os.listdir('img')
        self.flag = True
        print(flist)
        sl_th = threading.Thread(target=slide_th, args=(lambda: self.flag, self.app, flist))
        sl_th.start()

    def eff(self, effect):
        self.flag = True
        cam_th = threading.Thread(target=preview_th, args=(lambda: self.flag, self.app, effect))
        cam_th.start()

