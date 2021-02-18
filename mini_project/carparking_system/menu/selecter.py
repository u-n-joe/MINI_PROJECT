import cv2
import numpy as np

from pytesseract import *
import tkinter
import tkinter.font
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk
import os
import datetime

class AppWindow(tkinter.Frame):

    def __init__(self, window=None,title=None,geo=None):
        super().__init__(window)
        self.window = window
        self.window.title(title)
        self.window.geometry(geo)
        self.window['bg'] = '#CCCCCC'
        self['bg'] = '#CCCCCC'
        self.window.resizable(False,False)
        self.pack(side='left')
        self.path = './car'
        self.images = os.listdir(self.path)
        self.cnt = 0
        self.src = cv2.imread(self.path+'/'+self.images[self.cnt])
        self.srcResize = cv2.resize(self.src, (500, 400))

        self.numer_src = None
        self.subfr = None
        self.information = {}
        self.widthImg = 200
        self.heightImg = 50

        self.font = tkinter.font.Font(family="한컴 솔잎 B", size=15)
        self.ui()
        self.ui2()

    def ui(self):
        self.subfr = tkinter.Frame(self.window)
        self.subfr.pack(side='right',anchor='n')
        self.subfr2 = tkinter.Frame(self)
        self.subfr2.pack(side='bottom')
        self.subfr3 = tkinter.Frame(self.subfr)
        self.subfr3.pack(side='bottom',anchor='s')
        self.subfr['bg'] = '#CCCCCC'
        self.subfr2['bg'] = '#CCCCCC'
        self.subfr3['bg'] = '#CCCCCC'

        img = cv2.cvtColor(self.srcResize, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)

        self.label = tkinter.Label(self, image=imgtk)
        self.label.pack(side="top")
        self.label.config(image=imgtk)
        self.label.image = imgtk

        self.prev = tkinter.Button(self, bg='#fa8072', fg='white', width=10, text='prev', command=self.before)
        self.prev.pack(side="left", anchor='n', expand=True)

        self.next = tkinter.Button(self, bg='#fa8072', fg='white', width=10, text='next', command=self.after)
        self.next.pack(side="left", anchor='n', expand=True)

        self.entryBt = tkinter.Button(self, bg='#FFCC00', width=10, text='entry',
                                      command=lambda: self.entry(self.path + '/' + self.images[self.cnt]))
        self.entryBt.pack(side="left", anchor='n', expand=True)

        self.exitBt = tkinter.Button(self, bg='#FFCC00', width=10, text='exit',
                                   command=lambda: self.exit(self.path + '/' + self.images[self.cnt]))
        self.exitBt.pack(side="left", anchor='n', expand=True)

        self.countLabel = tkinter.Label(self, font=self.font, bg='#CCCCCC', text=f'입주차량: {len(self.information)}대')
        self.countLabel.pack(side='left', anchor='n')

    def ui2(self):
        self.numImg = tkinter.Label(self.window, bg='#CCCCCC')
        self.numImg.pack(side='top')

        self.entryLabel = tkinter.Label(self.window, font=self.font, bg='#CCCCCC')
        self.entryLabel.pack(side='top')

        self.exitLabel = tkinter.Label(self.window, font=self.font, bg='#CCCCCC')
        self.exitLabel.pack(side='bottom')

    def count(self):
        self.countLabel['text'] = f'입주차량: {len(self.information)}대'

    def update(self, image):
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.config(image=imgtk)
        self.label.image = imgtk

    def before(self):
        if self.cnt == 0:
            messagebox.showinfo(title='error', message='This is first image')
        else:
            self.cnt-=1
            self.viewImg()

    def after(self):
        if self.cnt == len(self.images)-1:
            messagebox.showinfo(title='error', message='This is last image')
        else:
            self.cnt+=1
            self.viewImg()

    def viewImg(self):
        self.src = cv2.imread(self.path + '/' + self.images[self.cnt])
        self.srcResize = cv2.resize(self.src, (500, 400))
        img = cv2.cvtColor(self.srcResize, cv2.COLOR_BGR2RGB)
        self.update(img)

    def preProcessing(self, img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 200, 200)
        return imgCanny

    def reorder(self, myPoints):
        myPoints = myPoints.reshape((4, 2))  # (4,1,2) -> (4,2)
        myPointsNew = np.zeros((4, 1, 2), np.int32)
        add = myPoints.sum(1)
        # print("add", add)
        myPointsNew[0] = myPoints[np.argmin(add)]  # 좌상
        myPointsNew[3] = myPoints[np.argmax(add)]  # 우하
        diff = np.diff(myPoints, axis=1)
        myPointsNew[1] = myPoints[np.argmin(diff)]  # 우상
        myPointsNew[2] = myPoints[np.argmax(diff)]  # 좌하
        # print("NewPoints",myPointsNew)
        return myPointsNew

    def getWarp(self,img, biggest):
        biggest = self.reorder(biggest)
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [self.widthImg, 0], [0, self.heightImg], [self.widthImg, self.heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgOutput = cv2.warpPerspective(img, matrix, (self.widthImg, self.heightImg))

        # edge를 깔끔하게 하기위해 crop
        imgCropped = imgOutput[2:imgOutput.shape[0] - 2, 2:imgOutput.shape[1] - 2]
        imgCropped = cv2.resize(imgCropped, (self.widthImg, self.heightImg))
        return imgCropped

    def getContour(self,imgThres, img_copy):
        contours, _ = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for pts in contours:
            area = cv2.contourArea(pts)
            if area > 1000:
                approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True) * 0.02, True)
                # print(approx.shape)
                if len(approx) == 4:
                    biggest = np.array(approx)
                    for i in approx:
                        cv2.circle(img_copy, (i[0][0], i[0][1]), 5, (0, 255, 255), -1)
                    self.setLabel(img_copy, pts, 'number')
        return biggest

    def setLabel(self, img, pts, label):
        (x, y, w, h) = cv2.boundingRect(pts)  # 주어진 점을 감싸는 최소 크기 사각형(바운딩 박스) 반환
        cv2.rectangle(img, (x, y, w, h), (0, 0, 255), 2)
        cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))

    def getNum(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, (500, 400))
        img_copy = img.copy()
        imgThres = self.preProcessing(img)
        biggest = self.getContour(imgThres, img_copy)
        result = self.getWarp(img, biggest)

        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        img_result = cv2.GaussianBlur(result, (3,3), sigmaX=0)
        _, img_result = cv2.threshold(img_result, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10,
                                        borderType=cv2.BORDER_CONSTANT, value=(0,0,0))


        cv2.imshow('img_copy', img_copy)
        cv2.imshow('imgThres', imgThres)
        cv2.imshow('result', img_result)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return img_result

    def entry(self, path):
        blur = self.getNum(path)
        text = image_to_string(blur, lang='eng', config='--psm 7')
        now = datetime.datetime.now()
        number = text.split()[0]

        if number in self.information:
            return messagebox.showinfo(title='error', message='이미 입차한 차량입니다.')

        self.entryLabel['text'] = f'최근 입차량\nCar Number: {number}\nTime: {now.strftime("%Y-%m-%d %H:%M:%S")}'
        self.information[number] = now
        self.count()
        print(f"주차정보 : {self.information}")

        img = Image.fromarray(blur)
        imgtk = ImageTk.PhotoImage(image=img)
        self.numImg.config(image=imgtk)
        self.numImg.image = imgtk

    def exit(self, path):
        blur = self.getNum(path)
        text = image_to_string(blur, lang='eng')
        exitTime = datetime.datetime.now()
        number = text.split()[0]

        if number not in self.information:
            return messagebox.showinfo(title='error', message='입차하지 않은 차량입니다.')

        entryTime = self.information[number]
        time = (exitTime - entryTime).seconds
        pay = time * 1  # 초당 1원
        self.exitLabel['text'] = f"최근 출차량\n{number} 차량의 주차금액: {pay}원"

        del self.information[number]
        self.count()
        print(f"주차정보 : {self.information}")