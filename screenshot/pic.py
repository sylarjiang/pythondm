# -*- coding:utf-8 -*-
import os
import cv2
from paddleocr import PaddleOCR, draw_ocr
from PIL import ImageGrab,Image
import conf
import aircv as ac

def CutePic(size = None,pic_name="test"):
    """
    截图
    :return:
    """
    if not size:
        size = [0, 0, 310, 700]
    if not os.path.exists(os.path.dirname(pic_name)):
        path=os.path.join(conf.PIC_PATH,"{}.jpg".format(pic_name))
    else:
        path = pic_name
    img =ImageGrab.grab(bbox=size)
    img.save(path)
    return path


def GetText(path=None,result_pic=False):
    """
    文字识别
    :param path:图片路径
    :return:
    """
    if not path:
        path = "F:/git/wxbot/dm/pic/222.png"
    # ocr = PaddleOCR(use_gpu=False,det_model_dir="./inference/ch_det_mv3_db/",rec_model_dir="./inference/ch_det_mv3_db/") # need to run only once to download and load model into memory
    ocr = PaddleOCR(gpu=False, det_model_dir="./inference/ch_det_r50_vd_db",
                    rec_model_dir="./inference/ch_rec_r34_vd_crnn_infer")  # need to run only once to download and load model into memory
    result = ocr.ocr(path)
    txts = [line[1][0] for line in result]

    # 展示图片
    if result_pic:
        image = Image.open(path).convert('RGB')
        boxes = [line[0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores)
        im_show = Image.fromarray(im_show)

        TMP_FILE = os.path.join(conf.TMP_PATH, "result.png")
        im_show.save(TMP_FILE)

    # print(txts)
    return txts

def MathPIC(Fpic,Cpic,confidence=0.95):
    """
    对比图片,默认相似度95%,则认为是同一图片
    :param Fpic:需要查找的图片
    :param Cpic:目标图片
    :param confidence:相似度
    :return: 找到的坐标点,和匹配后相似度
    """
    im_fpic = ac.imread(Fpic)
    im_cpic = ac.imread(Cpic)
    match_result = ac.find_template(im_fpic,im_cpic,confidence)
    if match_result and 'confidence' in match_result and match_result["confidence"]>=confidence:
        start= list(match_result["rectangle"][0])
        end = list(match_result["rectangle"][-1])
        # 展示匹配区域
        # tmp = cv2.rectangle(im_fpic, match_result["rectangle"][0], match_result["rectangle"][-1], (0, 0, 225), 2)
        # cv2.imshow("",tmp)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        start.extend(end)

        return [*start,match_result["confidence"]]

    return "ERROR: 没有匹配到图片标志"

if __name__ == '__main__':
    # pic1 = CutePic([100,100,500,500],"pic1")
    # pic2 = CutePic([0,0,600,600],"pic2")


    # pic1 = os.path.join(conf.PIC_PATH, "ql.jpg")
    # pic2 = os.path.join(conf.PIC_PATH, "full_screen.jpg")
    # # print(GetText(pic1))
    # print(MathPIC(pic2,pic1))
    for i in GetText(result_pic=True):
        print(i)

