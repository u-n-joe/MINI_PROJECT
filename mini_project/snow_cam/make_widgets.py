import tkinter as tk
import cv2
from tkinter import messagebox
import os
import sys
import time

c_serv = None  # 서비스 객체
path = 'img/'

def btn0_clicked():  # 카메라열기
    c_serv.preview()

def btn1_clicked(app):  # 사진찍기
    name = app.ent.get()
    fname = name + '.jpg'
    if fname[-4:] != '.jpg':
        messagebox.showinfo(title='error', message='확장자를 .jpg로 써주세요.')
        return
    elif fname in os.listdir(path):
        messagebox.showinfo(title='중복', message='다른 이름으로 사진을 지정해주세요.')
        return
    else:
        c_serv.capture(fname)
        messagebox.showinfo(title='저장', message='사진이 저장 되었습니다.')

def btn7_clicked(app):  # 사진보기
    flist = os.listdir('img')
    name = app.ent.get()
    fname = name + '.jpg'
    if fname not in flist:
        messagebox.showinfo(title='error', message='없는 사진입니다.')
        return
    c_serv.view_img(fname)

def btn2_clicked(app):  # 동영상찍기
    name = app.ent.get()
    fname = name + '.avi'
    if fname[-4:] != '.avi':
        messagebox.showinfo(title='error', message='확장자를 .avi로 써주세요.')
        return
    c_serv.videoStart(fname)

def btn3_clicked():
    print('영상저장완료')
    c_serv.stop()


def btn4_clicked(app):
    flist = os.listdir('video')
    name = app.ent.get()
    fname = name + '.avi'
    if fname not in flist:
        messagebox.showinfo(title='error', message='없는 동영상입니다.')
        return
    c_serv.view_video(fname)

def btn5_clicked(app):
    c_serv.slideOn()

def btn6_clicked():
    print('슬라이드 종료')
    c_serv.stop()

def bt_exit():
    print('프로그램 종료')
    cv2.destroyAllWindows()
    sys.exit(0)

def bt_snow_crown(app):
    effect = 'crown'
    c_serv.eff(effect)

def bt_snow_glasses(app):
    effect = 'glasses'
    c_serv.eff(effect)

def make(app, service):
    global c_serv
    c_serv = service
    app.ent = tk.Entry(app.sub_fr, width=60)
    app.btn0 = tk.Button(app.sub_fr, width=10, font=60, text='Preview')
    app.btn1 = tk.Button(app.sub_fr, width=10, font=60, text='사진촬영')
    app.btn7 = tk.Button(app.sub_fr, width=10, font=60, text='사진보기')
    app.btn2 = tk.Button(app.sub_fr, width=10, font=60, text='영상촬영')
    app.btn3 = tk.Button(app.sub_fr, width=10, font=60, text='영상종료')
    app.btn4 = tk.Button(app.sub_fr, width=10, font=60, text='동영상보기')
    app.btn5 = tk.Button(app.sub_fr, width=20, font=60, text='사진슬라이드시작')
    app.btn6 = tk.Button(app.sub_fr, width=20, font=60, text='사진슬라이드종료')
    app.btn_exit = tk.Button(app.sub_fr, width=20, font=60, text='프로그램 종료')
    app.btn_snow_crown = tk.Button(app.sub_fr, width=20, font=60, text='왕관 입히기')
    app.btn_snow_glasses = tk.Button(app.sub_fr, width=20, font=60, text='선글라스 입히기')

    app.ent.grid(row=0, column=0, columnspan=3)
    app.btn0.grid(row=1, column=0)
    app.btn1.grid(row=1, column=1)
    app.btn7.grid(row=1, column=2)
    app.btn2.grid(row=2, column=0)
    app.btn3.grid(row=2, column=1)
    app.btn4.grid(row=2, column=2)
    app.btn5.grid(row=3, column=0)
    app.btn6.grid(row=3, column=1)
    app.btn_exit.grid(row=3, column=2)
    app.btn_snow_crown.grid(row=4, column=0)
    app.btn_snow_glasses.grid(row=4, column=2)

    app.btn0['command'] = lambda: btn0_clicked()
    app.btn1['command'] = lambda: btn1_clicked(app)
    app.btn7['command'] = lambda: btn7_clicked(app)

    app.btn2['command'] = lambda: btn2_clicked(app)
    app.btn3['command'] = btn3_clicked

    app.btn4['command'] = lambda: btn4_clicked(app)
    app.btn5['command'] = lambda: btn5_clicked(app)
    app.btn6['command'] = btn6_clicked
    app.btn_exit['command'] = bt_exit

    app.btn_snow_crown['command'] = lambda: bt_snow_crown(app)
    app.btn_snow_glasses['command'] = lambda: bt_snow_glasses(app)