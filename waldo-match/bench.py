#!/usr/bin/env python3
import glob
import time
import math
import os
import numpy as np
import cv2 as cv
from match import METHODS, read_images, resize

REFERENCE_POINT = (1000, 1000)  # where test images are cropped
MATCH_TRESHOLD = 0.95  # minimal treshold to consider a match
SCALE_FACTOR = 2  # downscale to make matching faster


def dist2d(x, y):
    'Euclidean distance between two 2d points'
    return math.sqrt(pow(x[0] - y[0], 2) + pow(x[1] - y[1], 2))


if __name__ == "__main__":
    REFERENCE_POINT = [x/SCALE_FACTOR for x in REFERENCE_POINT]
    os.chdir('test_data')
    cropped = glob.glob('crop_*.jpg')
    originals = [f[len('crop_'):] for f in cropped]
    # compare speed and accuracy
    for meth in METHODS:
        start = time.time()
        n = 0
        error = 0
        for f in zip(originals, cropped):
            img1, img2 = read_images(f[0], f[1])
            img1 = resize(img1, SCALE_FACTOR)
            img2 = resize(img2, SCALE_FACTOR)
            res = cv.matchTemplate(img1, img2, eval(meth))
            _, _, min_loc, max_loc = cv.minMaxLoc(res)
            if meth in ['cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']:
                top_left = min_loc
            else:
                top_left = max_loc
            n += 1
            error += dist2d(top_left, REFERENCE_POINT)
        if n == 0:
            raise Exception("No *.jpg files found")
        elapsed = time.time() - start
        print("{}: avg_time={}, avg_err={}".format(meth, elapsed/n, error/n))
    # compare false positives rate
    for meth in filter(lambda x: x.endswith('NORMED'), METHODS):
        n = 0
        errors = 0
        for f in zip(originals, reversed(cropped)):
            if f[1].endswith(f[0]):
                continue
            img1, img2 = read_images(f[0], f[1])
            img1 = resize(img1, SCALE_FACTOR)
            img2 = resize(img2, SCALE_FACTOR)
            res = cv.matchTemplate(img1, img2, eval(meth))
            if meth in ['cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']:
                loc = np.where(res <= 1 - MATCH_TRESHOLD)
            else:
                loc = np.where(res >= MATCH_TRESHOLD)

            if len(list(zip(*loc[::-1]))) > 0:
                errors += 1
            n += 1
        if n == 0:
            raise Exception("No *.jpg files found")
        print("{}: {}% false positives".format(meth, (errors/n)*100))
