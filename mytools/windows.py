# -*- coding:utf-8 -*-
import os
import time

import psutil as psutil
import win32api
import win32con
import win32gui
import win32process
import win32clipboard
import ctypes

from screenshot.pic import CutePic, MathPIC


def GetPointWindow(point):
    """
    获取给定坐标的窗口句柄
    :param point: (x,y)元组
    :return:
    """
    return win32gui.WindowFromPoint(point)


def GetMousePointWindow():
    """
    获取鼠标指向的窗口句柄
    :return:
    """
    point = win32api.GetCursorPos()
    return GetPointWindow(point)


def GetWindowClassName(hwnd):
    """
    获取窗口的类名
    :param hwnd:
    :return:
    """
    return win32gui.GetClassName(hwnd)


def ClientToScreen(hwnd, point):
    """
    把窗口坐标转换为屏幕坐标
    :param hwnd:
    :param point: (x,y)元组

    :return:
    """
    return win32gui.ClientToScreen(hwnd, point)


def GetWindowTitle(hwnd):
    """
    获取窗口的标题
    :param hwnd:
    :return:
    """
    title = win32gui.GetWindowText(hwnd)
    return title


def GetWindowState(hwnd, flag=0):
    pass


def GetWindowProcessId(hwnd):
    """
    获取指定窗口所在的进程ID
    :param hwnd:
    :return: 返回线程id和进程id
    """
    return win32process.GetWindowThreadProcessId(hwnd)


def GetWindowProcessName(hwnd):
    """
    获取指定窗口所在的进程名称
    :param hwnd:
    :return:
    """
    tid, pid = GetWindowProcessId(hwnd)
    return psutil.Process(pid).name()


def GetClientRect(hwnd=None):
    """
    获取窗口坐标
    :param hwnd:
    :return:
    flags One of the WPF_* constants
    showCmd Current state - one of the SW_* constants.
    minpos Specifies the coordinates of the window's upper-left corner when the window is minimized.
    maxpos Specifies the coordinates of the window's upper-left corner when the window is maximized.
    normalpos 窗口的坐标
    """
    size = win32gui.GetWindowPlacement(hwnd)
    if len(size) == 5:
        return size[4]


def GetClintSize(hwnd):
    size = GetClientRect(hwnd)
    if size:
        return (size[2] - size[0], size[3] - size[1])


def EnumWindow(hwnd=None):
    """
    枚举系统中的窗口
    :return:

    """
    HwndList = []

    def GetHWNDProp(hwnd, HwndList):
        if (
            win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)
        ):
            HwndList.append(
                {
                    "hwnd": hwnd,
                    "title": GetWindowTitle(hwnd),
                    "class_name": GetWindowClassName(hwnd),
                    "process_name": GetWindowProcessName(hwnd),
                    "process_id": GetWindowProcessId(hwnd)[1],
                }
            )

    win32gui.EnumWindows(GetHWNDProp, HwndList)
    return HwndList


def FindWindow(class_name=None, title=None):
    """
    查找符合类名或者标题名的顶层可见窗口
    :param class_name:
    :param title:
    :return:
    """
    return win32gui.FindWindow(class_name, title)


def FindWindowEx(parent=None, clild=None, class_name=None, title=None):
    """
    查找符合类名或者标题名的顶层可见窗口
    :param parent:
    :param clild:
    :param class_name:
    :param title:
    :return:
    """
    return win32gui.FindWindowEx(parent, clild, class_name, title)

def GetWindowStatus(hwnd):
    allwindows = EnumWindow()

    def ProcessName(p):
        if p["hwnd"] == hwnd:
            return p

    res = list(filter(ProcessName, allwindows))
    if len(res)>0:

        return res[0]
    return "ERROR: 此窗口不是主窗口!"

def FindWindowByProcessName(process_name=None, class_name=None, title=None):
    allwindows = EnumWindow()

    def ProcessName(p):
        if p["process_name"] == process_name:
            return p

    res = list(filter(ProcessName, allwindows))
    if len(res) > 0:
        return res[0]["hwnd"]
    return "ERROR: 没有找到对应窗口"


def GetFocus():
    """
    功能确定当前焦点位于哪个控件上
    :return:
    """
    return win32gui.GetFocus()


def GetForegroundWindow():
    """
    用户当前工作的窗口
    :return:
    """
    return win32gui.GetForegroundWindow()


def MoveWindow(hwnd, x, y, width, height, brepaint=1):

    return win32gui.MoveWindow(hwnd, x, y, width, height, brepaint)

def ShowWindow(hwnd, flag=1):
    # RestoreWindow()
    show = win32con.SW_SHOW
    if flag == 0:
        show = win32con.SW_HIDE
    SetWindowPos(hwnd, 2)


def SetWindowPos(hwnd, flag=0):
    """
    置顶窗口
    pos:
        HWND_BOTTOM：将窗口置于Z序的底部。如果参数hWnd标识了一个顶层窗口，则窗口失去顶级位置，并且被置在其他窗口的底部。
        HWND_DOTTOPMOST：将窗口置于所有非顶层窗口之上（即在所有顶层窗口之后）。如果窗口已经是非顶层窗口则该标志不起作用。
        HWND_TOP:将窗口置于Z序的顶部。
        HWND_TOPMOST:将窗口置于所有非顶层窗口之上。即使窗口未被激活窗口也将保持顶级位置。
    Flags:窗口尺寸和定位的标志。该参数可以是下列值的组合：
        SWP_ASYNCWINDOWPOS：如果调用进程不拥有窗口，系统会向拥有窗口的线程发出需求。这就防止调用线程在其他线程处理需求的时候发生死锁。
        SWP_DEFERERASE：防止产生WM_SYNCPAINT消息。
        SWP_DRAWFRAME：在窗口周围画一个边框（定义在窗口类描述中）。
        SWP_FRAMECHANGED：给窗口发送WM_NCCALCSIZE消息，即使窗口尺寸没有改变也会发送该消息。如果未指定这个标志，只有在改变了窗口尺寸时才发送WM_NCCALCSIZE。
        SWP_HIDEWINDOW;隐藏窗口。
        SWP_NOACTIVATE：不激活窗口。如果未设置标志，则窗口被激活，并被设置到其他最高级窗口或非最高级组的顶部（根据参数hWndlnsertAfter设置）。
        SWP_NOCOPYBITS：清除客户区的所有内容。如果未设置该标志，客户区的有效内容被保存并且在窗口尺寸更新和重定位后拷贝回客户区。
        SWP_NOMOVE：维持当前位置（忽略X和Y参数）。
        SWP_NOOWNERZORDER：不改变z序中的所有者窗口的位置。
        SWP_NOREDRAW: 不重画改变的内容。如果设置了这个标志，则不发生任何重画动作。适用于客户区和非客户区（包括标题栏和滚动条）和任何由于窗回移动而露出的父窗口的所有部分。如果设置了这个标志，应用程序必须明确地使窗口无效并区重画窗口的任何部分和父窗口需要重画的部分。
        SWP_NOREPOSITION；与SWP_NOOWNERZORDER标志相同。
        SWP_NOSENDCHANGING：防止窗口接收WM_WINDOWPOSCHANGING消息。
        SWP_NOSIZE：维持当前尺寸（忽略cx和Cy参数）。
        SWP_NOZORDER：维持当前Z序（忽略hWndlnsertAfter参数）。
        SWP_SHOWWINDOW：显示窗口
    :param hwnd:
    :param x:
    :param y:
    :param w:
    :param h:
    :param pos:
    :param flag:
    :return:
    """
    RestoreWindow(hwnd)
    SetForegroundWindow(hwnd)
    # 置顶
    flags = (
        win32con.SWP_NOSIZE
        | win32con.SWP_NOMOVE
        | win32con.SWP_SHOWWINDOW
        | win32con.SWP_ASYNCWINDOWPOS
    )
    if flag == 0:
        pos = win32con.HWND_TOPMOST
    # 取消置顶
    elif flag == 1:
        pos = win32con.HWND_NOTOPMOST
    # 窗口最前
    elif flag == 2:
        pos = win32con.HWND_TOP
    return win32gui.SetWindowPos(hwnd, pos, 0, 0, 0, 0, flags)

def SetForegroundWindow(hwnd):
    win32gui.SetForegroundWindow(hwnd)


def RestoreWindow(hwnd):
    """
    恢复最小化的窗口
    :param hwnd:
    :return:
    """
    win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)


def ActiveWindow(hwnd,flag = 2):
    """
    激活窗口,先恢复最小化状态,再窗口最前
    :param hwnd:
    :return:
    """
    RestoreWindow(hwnd)
    SetWindowPos(hwnd, flag)


def CloseWindow(hwnd):
    """
    关闭窗口,避免bug,休眠一下
    :param hwnd:
    :return:
    """
    time.sleep(0.001)
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def SetWindowTransparent(hwnd,transparency=255):
    """
    设置窗口透明度
    :param hwnd:
    :param transparency: 透明度最大255,不透明,0最小,完全透明
    :return:
    """
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), transparency, win32con.LWA_ALPHA)


def SendStr(hwnd,s):
    print(s)
    s = s.encode("gbk")
    print(s)
    for word in s:
        win32gui.SendMessage(hwnd, win32con.WM_CHAR, word, 0)

def GetScreenSize():
    x =win32api.GetSystemMetrics(win32con.SM_CXFULLSCREEN)
    y=win32api.GetSystemMetrics(win32con.SM_CYFULLSCREEN)
    return x,y


def FindPic(x,y,rx,ry,pic_name):
    screen_pic = CutePic([x,y,rx,ry],"full_screen")
    if os.path.isfile(pic_name):
        res = MathPIC(screen_pic,pic_name)
        return res
    return False

# res = EnumWindow()
if __name__ == "__main__":
    # print(GetWindowClassName(GetMousePointWindow()))
    # print(GetWindowClassName(FindWindowEx(parent=0,title="微信")))
    # print(GetCliᒈᏨntSize(FindWindowEx(parent=0,title="微信")))
    # hwnd = GetMousePointWindow()
    # ActiveWindow(hwnd,0)
    # SetCursorPos((700,700))
    # # LeftClick()
    # SendStr(hwnd,"蒋涛")
    # # SetWindowTransparent(hwnd)
    #
    # print()
    pass
    ActiveWindow(FindWindow("WeChatMainWndForPC"),2)
