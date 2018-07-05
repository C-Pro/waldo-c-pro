# waldo-match

[![Build Status](https://travis-ci.org/C-Pro/waldo-c-pro.svg?branch=master)](https://travis-ci.org/C-Pro/waldo-c-pro)

Script [match.py](waldo-match/match.py) finds cropped areas in pairs of images. It uses OpenCV `matchTemplate` function for template matching.
It accepts two file names as arguments and if one image is a crop of another it returns which one is source, and which is a crop and coordinates of top-left corner of cropped area. Otherwise it prints "No match found".

## Installation

Script requires python>=3.6.

```
make install
```

## Usage

```
match file1.jpg file2.jpg [method]
```

Where optional method can be one of:
* `cv.TM_CCOEFF`
* `cv.TM_CCOEFF_NORMED`
* `cv.TM_CCORR`
* `cv.TM_CCORR_NORMED`
* `cv.TM_SQDIFF`
* `cv.TM_SQDIFF_NORMED`


By default it uses `cv.TM_CCOEFF_NORMED` as it proved the best one on my simple test set.

## Examples

```
$ match.py test_data/20180701_0001.jpg test_data/crop_20180701_0001.jpg
test_data/crop_20180701_0001.jpg is a crop of test_data/20180701_0001.jpg with offset (1000, 1000)
```

Reverse order of parameters:
```
$ match.py test_data/crop_20180701_0001.jpg test_data/20180701_0001.jpg
test_data/crop_20180701_0001.jpg is a crop of test_data/20180701_0001.jpg with offset (1000, 1000)
```

No match:
```
$ match.py test_data/crop_20180701_0001.jpg test_data/20180701_0014.jpg
No match found
````


## How I tested
I grabbed some images from my DSLR camera and cropped 100x100 square from each with [this script](waldo-match/test_data/images_crop.sh).
Then I wrote [small benchmark](waldo-match/bench.py) that compares speed, accuracy and false positives rate for each of methods (I also used it to find acceptable constant values - match treshold, downscale factor, grayscale or color images, etc.).

`cv.TM_CCOEFF_NORMED` was the winner on my test set with no errors and somewhat tolerable speed.

Here is output of `bench.py` run:

```
cv.TM_CCOEFF: avg_time=0.3788928985595703, avg_err=461.37533590391615
cv.TM_CCOEFF_NORMED: avg_time=0.4314530849456787, avg_err=0.0
cv.TM_CCORR: avg_time=0.33414306640625, avg_err=821.2177699953379
cv.TM_CCORR_NORMED: avg_time=0.4176189422607422, avg_err=0.0
cv.TM_SQDIFF: avg_time=0.4067682266235352, avg_err=0.0
cv.TM_SQDIFF_NORMED: avg_time=0.42618322372436523, avg_err=0.0
cv.TM_CCOEFF_NORMED: 0.0% false positives
cv.TM_CCORR_NORMED: 75.0% false positives
cv.TM_SQDIFF_NORMED: 25.0% false positives
```

## Limitations

OpenCV `matchTemplate` function can be used to find exact crops with some noise tolerance, but rotation and scaling will fool it. It is possible to substitute it for one of more advanced algorithms like SURF, FAST, etc.
With full size photos containing big and relatively flat areas (grass, sky, sea) random crops containing no edges sometimes fail to detect if using grayscale, downsampling or high match threshold is set. But decreasing treshold can lead to false positives, so parameters should be tuned for particular use case.
