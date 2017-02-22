#!/usr/bin/env python3

from PIL import Image, ImageDraw
import numpy as np
import io
import os
from typing import Tuple, NewType

RGBA = NewType('RGBA', Tuple[int, int, int, int])

def getImg(filename: str, color: RGBA=(0,0,0,0)) -> Image:
    """prec: str filename of very specific datatype: eg. \n
    110101001001\\n \n
    00101001010100\\n \n
    0010101010100101\\n \n
    postc: returns PIL.Image"""

    def getHeight(height_file: io.TextIOWrapper) -> int:
        """prec: file object; postc: returns number of lines"""
        height = sum(1 for line in height_file)
        file.seek(0,0)
        return height

    def getWidth(width_file: io.TextIOWrapper) -> int:
        """prec: file object; postc: length of last line in file"""
        for line in width_file:
            pass
        last = line.replace('\n', '')
        width = len(line)
        file.seek(0, 0)
        return width

    def importFile(pad_file: io.TextIOWrapper, true_color: RGBA=(0,0,0,0), false_color: RGBA=(255,255,255,0)) -> np.ndarray:
        """prec: file object of specific format; postc: list of lists of ints"""
        file_padded = ['{line:0^{width}}'.format(line=line, width=width) for line in pad_file.readlines()]
        padded_list = [list(padded_line) for padded_line in file_padded]
        color_list = [[true_color if item == '1' else false_color for item in line] for line in padded_list]
        color_array = np.asarray(dtype=np.dtype('uint8'), a=color_list)
        return color_array


    file = open(filename, 'r')
    width = getWidth(file)
    height = getHeight(file)
    img_file = importFile(file, true_color=color)
    img = Image.fromarray(img_file, mode='RGBA')
    return img

RED = RGBA((255,0,0,255))
BLACK = RGBA((0,0,0,255))

for filename in os.listdir('genfilessmall'):
    if filename.endswith('.errors'):
        err_img = getImg('genfilessmall/'+filename, RED)
        row_img = getImg('genfilessmall/'+filename[:-7]+'.rows', BLACK)
        comp_img = Image.alpha_composite(row_img, err_img)
        comp_img.save('composites/'+filename[:-7]+'.png', 'png')

# row_img = getImg('genfilessmall/30.0.rows', BLACK)
# err_img = getImg('genfilessmall/30.0.errors', RED)
# comp_img = Image.alpha_composite(row_img, err_img)
#
# comp_img.show()
