# coding=utf-8
from ctypes import windll, Structure, c_int, c_uint, c_void_p, POINTER, cast, CFUNCTYPE, c_long
from ctypes import wintypes
import win32con




class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [
        ('vkCode',c_int),
        ('scanCode', c_int),
        ('flags', c_int),
        ('time', c_int),
        ('dwExtraInfo', c_uint),
        ('',c_void_p)
    ]


class POINT(Structure):
    _fields_ = [
        ('x',c_long),
        ('y',c_long)
    ]


class MSLLHOOKSTRUCT(Structure):
    _fields_ = [
        ('pt',POINT),
        ('hwnd',c_int),
        ('wHitTestCode',c_uint),
        ('dwExtraInfo',c_uint),
    ]

class HookApi():
    def __init__(self):

        self.SetWindowsHookEx=windll.user32.SetWindowsHookExA
        self.UnhookWindowsHookEx=windll.user32.UnhookWindowsHookEx
        self.CallNextHookEx=windll.user32.CallNextHookEx
        self.GetMessage=windll.user32.GetMessageA
        self.GetModuleHandle=windll.kernel32.GetModuleHandleW
        #保存键盘钩子函数句柄
        self.keyboard_hd = None
        #保存鼠标钩子函数句柄
        self.mouse_hd = None

    def WaitForMSG(self):
        msg = wintypes.MSG()
        self.GetMessage(msg, 0, 0, 0)


    def KeyboardPro(self,nCode, wParam, lParam):
        """
        函数功能：键盘钩子函数，当有按键按下时此函数被回调
        """
        if nCode == win32con.HC_ACTION:
            KBDLLHOOKSTRUCT_p = POINTER(KBDLLHOOKSTRUCT)
            param=cast(lParam,KBDLLHOOKSTRUCT_p)
            print(param.contents.vkCode)
        return self.CallNextHookEx(self.keyboard_hd, nCode, wParam, lParam)


    def StartKeyboardHook(self):
        """
        函数功能：启动键盘监听
        """
        HOOKPROTYPE = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        pointer = HOOKPROTYPE(self.KeyboardPro)
        self.keyboard_hd = self.SetWindowsHookEx(
            win32con.WH_KEYBOARD_LL,
            pointer,
            self.GetModuleHandle(None),
            0)
        self.WaitForMSG()


    def StopKeyboardHook(self):
        """
        函数功能：停止键盘监听
        """
        self.UnhookWindowsHookEx(self.keyboard_hd)


    def MousePro(self,nCode, wParam, lParam):
        """
        函数功能：鼠标钩子函数，当有鼠标事件，此函数被回调
        """
        if nCode == win32con.HC_ACTION:
            MSLLHOOKSTRUCT_p = POINTER(MSLLHOOKSTRUCT)
            param=cast(lParam,MSLLHOOKSTRUCT_p)
            #鼠标左键点击
            if wParam == win32con.WM_LBUTTONDOWN:
                print("左键点击，坐标：x:%d,y:%d" % (param.contents.pt.x,param.contents.pt.y))
            elif wParam == win32con.WM_LBUTTONUP:
                self.StopMouseHook()
                print("左键抬起，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
            elif wParam == win32con.WM_MOUSEMOVE:
                print("鼠标移动，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
            elif wParam == win32con.WM_RBUTTONDOWN:
                print("右键点击，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
            elif wParam == win32con.WM_RBUTTONUP:
                print("右键抬起，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
        return self.CallNextHookEx(self.mouse_hd, nCode, wParam, lParam)


    def StartMouseHook(self):
        """
        函数功能：启动鼠标监听
        """
        HOOKPROTYPE = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        pointer = HOOKPROTYPE(self.MousePro)
        self.mouse_hd = self.SetWindowsHookEx(
            win32con.WH_MOUSE_LL,
            pointer,
            self.GetModuleHandle(None),
            0)
        self.WaitForMSG()


    def StopMouseHook(self):
        """
        函数功能：停止鼠标监听
        """
        self.UnhookWindowsHookEx(self.mouse_hd)

if __name__ == '__main__':
    HookApi().StartMouseHook()