# -*- coding:utf-8 -*-
from time import sleep

import conf
from mytools.keyboard_mouse import Combination, MouseClick, SendText,Sleep, LeftDobuleClick
from mytools.logger import logger
from mytools.windows import ActiveWindow, MoveWindow, FindWindow, GetScreenSize
from screenshot.pic import CutePic, MathPIC


def SendWX(to, message):
    """

    :param to:
    :param message:
    :return:
    """
    logger.info("start send message!!!")
    dm = GetWindow()
    hwnd = dm.GetHWND("WeChatMainWndForPC", "", 700,1000, 0, 0)
    res = FindNickName(to)

    if "ERROR" in res:
        logger.info("发送消息出错,")
        logger.info(res)
        return res
    MouseClick(600, 650)
    SendText(message)


def SetNickname(nick_name, open_id):
    """
    修改昵称为open_id
    :param nick_name:
    :param open_id:
    :return:
    """
    dm = GetWindow()
    hwnd = dm.GetHWND("WeChatMainWndForPC", "", 700, 1000, 0, 0)
    res = FindNickName(nick_name)
    if "ERROR" in res:
        logger.info("修改昵称出错,")
        logger.info(res)
        return res

    MouseClick(975, 45)
    Sleep(1)
    MouseClick(1100, 50)
    Sleep(0.5)
    MouseClick(1200, 195)
    Sleep()
    LeftDobuleClick()

    # chlid = GetMousePointWindow()
    SendText(open_id)
    MouseClick(600, 650)

    res = FindNickName(open_id)

    if "ERROR" in res:
        return "ERROR: 修改openid失败"
    return True





class GetWindow():
    def __init__(self):
        pass

    def GetHWND(self,classname, title, heigh=-1, width=-1, x=-1, y=-1):

        keys = ["ctrl","w"]
        Combination(keys)
        Sleep()
        if classname:
            self.hwnd = FindWindow(class_name=classname)
        else:
            self.hwnd = FindWindow(title=title)
        ActiveWindow(self.hwnd,0)
        if heigh >= 0 and width >= 0 and x >= 0 and y >= 0:
            MoveWindow(self.hwnd,x, y, width, heigh)

def FindNickName(name):
    MouseClick(28, 147)
    MouseClick(148, 40)
    Sleep()
    SendText(name,click=False)
    Sleep(1)
    full_screen_pic = CutePic([60, 60, 300, 180], "full_screen")
    if FindBasePic(full_screen_pic,"wxh"):
        return "ERROR: 没有找到对应联系人"
    x = FindBasePic(full_screen_pic)
    y = FindBasePic(full_screen_pic, "gd")
    z = FindBasePic(full_screen_pic, "lxr")
    if (x or y) and z:
        Combination(["enter"])
    else:
        return "ERROR: 没有找到对应联系人"
    return ""

def FindBasePic(full_screen_pic,pic="ql"):
    pic_path = "{}\\{}.jpg".format(conf.PIC_PATH, pic)
    a = MathPIC(full_screen_pic,pic_path)
    if isinstance(a,str):
        return False
    if a[0] < 0 and a[1] < 0 and a[2] < 2:
        return False
    return a

if __name__ == '__main__':
    # SendWX("马东飞","我是机器人")
    SetNickname("我是机器人","我是机器人1")

