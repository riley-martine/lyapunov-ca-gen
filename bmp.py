#!/usr/bin/env python3

from PIL import Image, ImageDraw
import numpy as np
import io
from typing import Tuple

def getImg(filename: str) -> Image:
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

    RGB = Tuple[int, int, int]
    def importFile(pad_file: io.TextIOWrapper, true_color: RGB=(0,0,0), false_color: RGB=(255,255,255)) -> np.ndarray:
        """prec: file object of specific format; postc: list of lists of ints"""
        file_padded = ['{line:0^{width}}'.format(line=line, width=width) for line in pad_file.readlines()]
        padded_list = [list(padded_line) for padded_line in file_padded]
        color_list = [[true_color if item == '1' else false_color for item in line] for line in padded_list]
        color_array = np.asarray(dtype=np.dtype('uint8'), a=color_list)
        return color_array


    file = open(filename, 'r')
    width = getWidth(file)
    height = getHeight(file)
    img_file = importFile(file, true_color=(255,0,0))
    img = Image.fromarray(img_file, mode='RGB')
    return img

img = getImg('genfilessmall/30.0.errors')
img.show()
