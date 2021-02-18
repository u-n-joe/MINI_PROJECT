#이 함수 안에 기능을 구현하시오
#기능구현 클래스를 따로 만들고 그 객체를 생성하여 실행하는 코드를 넣으면 ok
import tkinter as tk
import cv2
from PIL import Image
from PIL import ImageTk

class Service():
    def __init__(self,app):
        self.app = app

    def service(self):
        img = self.app.label.image
        print(img)
