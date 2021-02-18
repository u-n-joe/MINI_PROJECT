import carparking_system.menu.selecter as selecter
import tkinter

def main():
    window = tkinter.Tk()
    title = "joe's parking system"
    geometry = ("1000x1000+100+100")
    app = selecter.AppWindow(window, title, geometry)
    app.mainloop()

main()