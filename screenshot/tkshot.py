import os
import shutil
import tkinter as tk
# from tkinter import *
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageGrab, ImageTk
import ctypes, sys
from tkinter import filedialog

import conf
from mytools.logger import logger
from mytools.windows import GetMousePointWindow, GetWindowStatus
from screenshot.pic import GetText

def cut(editor):
    editor.event_generate("<<Cut>>")


def copy(editor):
    editor.event_generate("<<Copy>>")


def paste(editor):
    editor.event_generate('<<Paste>>')


def rightKey(widget, event, editor):
    """功能：cut copy paste"""
    menu_bar = tk.Menu(widget, tearoff=False)
    menu_bar.delete(0, tk.END)
    menu_bar.add_command(label='剪切', command=lambda: cut(editor))
    menu_bar.add_command(label='复制', command=lambda: copy(editor))
    menu_bar.add_command(label='粘贴', command=lambda: paste(editor))
    menu_bar.post(event.x_root, event.y_root)


def menuRK(root, widget):
    """部件添加右键功能<Button-3>"""
    widget.bind("<Button-3>", lambda x: rightKey(root, x, widget))


rectangleId = None
if sys.getwindowsversion().major == 10:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

TMP_FILE = os.path.join(conf.TMP_PATH,"tmp.png")

def AreaSel(show=True):
    def getPress(event):
        global press_x,press_y
        press_x,press_y = event.x,event.y
        print(press_x,press_y)

    def mouseMove(event):
        global press_x, press_y, rectangleId
        fullCanvas.delete(rectangleId)
        rectangleId = fullCanvas.create_rectangle(press_x,press_y,event.x,event.y,width=1)
        print(event.x,event.y)

    def getRelease(event):
        global press_x, press_y, rectangleId
        top.withdraw()
        img = ImageGrab.grab((press_x, press_y,event.x,event.y))
        if show:
            img.show()
        res = img.save(TMP_FILE)
        print(event.x,event.y)


        # fileName = filedialog.asksaveasfilename(title='保存截图', filetypes=[('image', '*.jpg *.png')])
        #
        # if fileName:
        #     img.save(fileName)
        # print(res)


    top = tk.Toplevel()
    top.state('zoomed')
    top.overrideredirect(1)
    fullCanvas = tk.Canvas(top)

    background = ImageTk.PhotoImage(ImageGrab.grab().convert("L"))
    # background = ImageTk.PhotoImage(ImageGrab.grab())
    fullCanvas.create_image(0,0,anchor="nw",image=background)

    fullCanvas.bind('<Button-1>',getPress)
    fullCanvas.bind('<B1-Motion>',mouseMove)
    fullCanvas.bind('<ButtonRelease-1>',getRelease)
    fullCanvas.pack(expand="YES",fill="both")
    fullCanvas.pack()
    top.mainloop()


def SavePIC():
    fileName = filedialog.asksaveasfilename(title='保存截图', filetypes=[('image', '*.jpg *.png')])
    if fileName:
        if fileName[-4:] not in ['.jpg',".png"]:
            fileName= "{}.jpg".format(fileName)
        shutil.copy(TMP_FILE,fileName)
    return fileName


def DictToStr(d):
    if not isinstance(d,dict):
        return str(d)
    l = [ "{}:{}".format(k,v) for k,v in d.items()]
    return "\n\n".join(l)

def Main():
    root = tk.Tk()
    root.title("截图工具")
    root.geometry('300x400')  # 窗口大小：宽*高
    root.resizable(width=False, height=False)  # 设置宽高不可变

    frame = tk.Frame(root,)

    scroll = tk.Scrollbar(frame)
    text = tk.Text(frame)
    scroll.pack(side=tk.RIGHT,fill=tk.Y)
    text.pack(side=tk.LEFT,fill=tk.Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    content = "111"
    text.insert("insert",content)
    text.config(state=tk.DISABLED)
    frame.pack()

    """ 截图按钮 """
    btn_ScreenShot = tk.Button(root, text="开始截图", command=AreaSel)
    btn_ScreenShot.place(width=90, height=30, x=40, y=350)

    """ 截图全图 """
    btn_ScreenAllShot = tk.Button(root, text="保存", command=SavePIC)
    btn_ScreenAllShot.place(width=90, height=30, x=170, y=350)

    def WindowStatus(event):
        hwnd = GetMousePointWindow()
        status = GetWindowStatus(hwnd)
        text.config(state=tk.NORMAL)
        text.delete("1.0","end")
        res = DictToStr(status)
        logger.info(status)
        text.insert("insert", res)
        text.config(state=tk.DISABLED)
        text.update()
    btn_window_status = tk.Button(root, text="获取鼠标选中窗体信息", cursor='circle')
    btn_window_status.bind("<ButtonRelease-1>",WindowStatus)
    btn_window_status.place(width=150, height=30,x=75, y=300)

    root.mainloop()


if __name__ == '__main__':
    Main()
    # AreaSel()
    # print(GetText(SavePIC(),True))

# root = tk.Tk()

# sel_btn = tk.Button(root, text='select area', width=20, command=AreaSel)
# sel_btn.pack()
# root.mainloop()