import tkinter as tk
import snow_cam.main_ui as win
import snow_cam.make_widgets as mkw
import snow_cam.camera_service as cs

def main():
    img_path = 'img/a.jpg'
    root = tk.Tk()

    app = win.AppWindow(root, '840x700+100+100', img_path)
    service = cs.CameraService(app)
    mkw.make(app, service)
    app.mainloop()

main()
