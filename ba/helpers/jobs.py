# -*- coding: utf-8 -*-
import os
from datetime import datetime
from ba.helpers.logic import LogicHelper
from PIL import Image, ImageDraw, ImageFont
import math

from PIL import Image, ImageDraw, ImageFont

def add_watermark_fun1(img_pil, text):
    (w, h) = img_pil.size

    img_rgba = img_pil.convert("RGBA")

    text_img = Image.new("RGBA", img_rgba.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_img)

    font = ImageFont.truetype('simhei.ttf', 30)  # 字体及字体大小
    
    text_position = (w/2,h-80)
    text_position_2 = (w/2+2,h-78)
    # print("org size:", w, h)
    # print("position:", text_position)
    # print("text:",text)
    # text = u"广州流溪河@水滴精灵2020"
    # 文本位置, 颜色, 透明度
    draw.text(text_position_2, text, font=font, fill=(255, 255, 255, 100))
    draw.text(text_position, text, font=font, fill=(0, 0, 0, 100))
    # print("done...")

    # 合成水印图片
    img_with_watermark = Image.alpha_composite(img_rgba, text_img)
    
    # 显示加水印后的图片
    # img_with_watermark.show()

    return img_with_watermark.convert("RGB")


def add_watermark_fun2(img_pil, text):
    print("[INFO]PIL image info: ", img_pil.size)
    width, height = img_pil.width, img_pil.height

    #
    new_img = Image.new('RGBA', (width * 3, height * 3), (0, 0, 0, 0))
    new_img.paste(img_pil, (width, height))
    img_rgba = new_img.convert('RGBA')

    #
    text_img = Image.new('RGBA', img_rgba.size, (100, 100, 255, 0))
    draw = ImageDraw.Draw(text_img)

    # 添加水印
    # 文本位置, 颜色, 透明度
    font = ImageFont.truetype('simhei.ttf', 30)
    for i in range(0, img_rgba.size[0], len(text) * 20 + 80):
        for j in range(0, img_rgba.size[1], 200):
            draw.text((i, j), text, font=font, fill=(0, 0, 0, 50))

    # 旋转文字 45 度
    text_img = text_img.rotate(-45)

    # 合成水印图片
    img_with_watermark = Image.alpha_composite(img_rgba, text_img)

    # 原始图片尺寸
    img_with_watermark = img_with_watermark.crop((width, height, width * 2, height * 2))

    img_with_watermark.show()
    
    return img_with_watermark.convert("RGB")

# compress the file and add water mark
def CompressAndAddWaterMark(fileName, text):

    root_path = "/Users/sicon/working/108_DXSW/BenethosAdmin/Images/"
    target_size = 80000.00
    handle_size = 99999.00
    img_path = root_path + fileName
    
    if os.path.exists(img_path):

        img = Image.open(img_path)
        (x,y) = img.size 
        
        tmpp = root_path+'tmp.jpg'
        img.thumbnail((x/1, y/1))
        img.save(tmpp)
        org_size = os.path.getsize(tmpp)

        rate = 1
        if org_size > handle_size:
            rate = math.sqrt(target_size / float(org_size))
        
        tmpp = root_path+fileName.replace(".JPG","-sw.JPG")
        img.thumbnail((rate*x, rate*y))
        #"广州流溪河@水滴精灵"
        # print("org:",x,y,rate)
        rImg = add_watermark_fun1(img, text)

        rImg.save(tmpp)
        return True
    else:
        print(img_path + " image doesn't exists...")
        return False

def water_mark_handler():
    hlp = LogicHelper()
    r = hlp.getAllImages()
    for item in r:
        picName = item["BADict_Value"]
        teamName = item["Name"]
        sampleId = item["id"]

        print("Start to compress & watermark " + picName)
        hs = CompressAndAddWaterMark(picName, teamName+u"@水底精灵")
        if hs == True:
            hlp.updateImageHandleStatus(sampleId, 1)
            print("Image " + picName + " proceed successfully." )
        else:
            hlp.updateImageHandleStatus(sampleId, 99)
            print("Image " + picName + " proceed failed, pls see the log for detail." )
