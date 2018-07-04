import sys
import imutils
import cv2 as cv
import numpy as np

SCALE_FACTOR = 2  # downscale to make matching faster
MATCH_TRESHOLD = 0.99  # minimal treshold to consider a match

USAGE_TEXT = '''Usage:
    match file1.jpg file2.jpg [method]
method can be one of:
    cv.TM_CCOEFF
    cv.TM_CCOEFF_NORMED
    cv.TM_CCORR
    cv.TM_CCORR_NORMED
    cv.TM_SQDIFF
    cv.TM_SQDIFF_NORMED
'''

METHODS = ['cv.TM_CCOEFF',
           'cv.TM_CCOEFF_NORMED',
           'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED',
           'cv.TM_SQDIFF',
           'cv.TM_SQDIFF_NORMED']


def read_flags():
    "Get command arguments. Print usage on error."
    if len(sys.argv) < 3:
        sys.stderr.write(USAGE_TEXT)
        sys.exit(1)
    method = 'cv.TM_CCOEFF_NORMED'
    if len(sys.argv) == 4:
        method = sys.argv[3]
        if method not in METHODS:
            sys.stderr.write(USAGE_TEXT)
            sys.exit(1)
    return (sys.argv[1], sys.argv[2], method)


def read_images(fname1, fname2):
    "read images with cv.imread"
    img1 = cv.imread(fname1, cv.IMREAD_UNCHANGED)
    if img1 is None:
        raise Exception("Failed to read {}".format(img1))
    img2 = cv.imread(fname2, cv.IMREAD_UNCHANGED)
    if img2 is None:
        raise Exception("Failed to read {}".format(img2))
    return (img1, img2)


def resize(img, scale_factor):
    "downscale image"
    if scale_factor == 0:
        raise ValueError("scale_factor should not be zero")
    return imutils.resize(img, width=int(img.shape[1] / scale_factor))


if __name__ == "__main__":
    fname1, fname2, meth = read_flags()
    img1, img2 = read_images(fname1, fname2)
    img1 = resize(img1, SCALE_FACTOR)
    img2 = resize(img2, SCALE_FACTOR)

    # swap images so bigger one comes first
    if (img1.shape[0] < img2.shape[0]) or (img1.shape[1] < img2.shape[1]):
        img1, img2 = img2, img1
        fname1, fname2 = fname2, fname1

    res = cv.matchTemplate(img1, img2, eval(meth))
    if meth in ['cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']:
        loc = np.where(res <= 1 - MATCH_TRESHOLD)
    else:
        loc = np.where(res >= MATCH_TRESHOLD)
    matches = list(zip(*loc[::-1]))
    if len(matches) == 0:
        print("No match found")
        sys.exit(0)
    scaled_match = (matches[0][0]*SCALE_FACTOR, matches[0][1]*SCALE_FACTOR)
    print("{} is a crop of {} with offset {}".format(
        fname2, fname1, scaled_match))
