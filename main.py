#!/usr/bin/env python3
"""Generate images (pngs) of CAs and their defect cones."""
import os
import sys
from io import TextIOWrapper
from typing import Tuple, NewType
from shutil import rmtree
from PIL import Image
from numpy import ndarray, asarray, dtype
from generatefiles import make_rand_files

RGBA = NewType('RGBA', Tuple[int, int, int, int])
RED = RGBA((255, 0, 0, 255))
BLACK = RGBA((0, 0, 0, 255))
WHITE = RGBA((255, 255, 255, 0))

def make_images(save_dir: str="generated", save_all: bool=False) -> None:
    """Generates CA images of defect cones. Saves all steps if save_all set."""

    def get_img(file_name: str, color: RGBA=BLACK) -> Image:
        """prec: str filename of very specific datatype: eg. \n
        110101001001\\n \n
        00101001010100\\n \n
        0010101010100101\\n \n
        postc: returns PIL.Image"""

        def get_width(width_file: TextIOWrapper) -> int:
            """prec: file object; postc: length of last line in file"""
            last_line = width_file.readlines()[-1].replace('\n', '')
            width = len(last_line)
            file.seek(0, 0)
            return width

        def import_file(pad_file: TextIOWrapper, true_color: RGBA=BLACK, false_color: RGBA=WHITE) -> ndarray:
            """prec: file object of specific format; postc: list of lists of ints"""
            file_padded = ['{line:0^{width}}'.format(
                line=line, width=width) for line in pad_file.readlines()]
            padded_list = [list(padded_line) for padded_line in file_padded]
            if padded_list[-1][-1] == '\n':
                padded_list[-1].pop()
            color_list = [[true_color if item == '1' else false_color for item in line]
                          for line in padded_list]
            color_array = asarray(dtype=dtype('uint8'), a=color_list)
            return color_array

        file = open(file_name, 'r')
        width = get_width(file)
        img_file = import_file(file, true_color=color)
        img = Image.fromarray(img_file, mode='RGBA')
        return img

    if os.path.isdir(save_dir):
        print("Please back up or remove '{}/' before proceeding.".format(save_dir))
        if input("Delete? (y/n): ") == 'y':
            rmtree(save_dir)
        else:
            sys.exit(0)

    os.mkdir(save_dir)
    os.chdir(save_dir)
    os.mkdir('.genfiles')

    os.chdir('.genfiles')
    make_rand_files(rules=(30, 90, 110), number_of_files=1,
                    len_first_row=500, number_of_rows=500)
    os.chdir('..')

    for filename in os.listdir('.genfiles'):
        if filename.endswith('.errors'):
            err_img = get_img('.genfiles/' + filename, RED)
            row_img = get_img('.genfiles/' + filename[:-7] + '.rows', BLACK)
            comp_img = Image.alpha_composite(row_img, err_img)
            comp_img.save(filename[:-7] + '.png', 'png')
            if save_all:
                row2_img = get_img('.genfiles/' + filename[:-7] + '.rows2', BLACK)
                err_img.save(filename[:-7] + '.errors.png', 'png')
                row_img.save(filename[:-7] + '.rows.png', 'png')
                row2_img.save(filename[:-7] + '.rows2.png', 'png')

    rmtree('.genfiles')
    print("Done generating images. Images are in the '{}/' directory.".format(save_dir))

if __name__ == "__main__":
    make_images()
