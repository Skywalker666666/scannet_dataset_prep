#!/usr/bin/python
#
# Convert to COCO-style panoptic segmentation format (http://cocodataset.org/#format-data).
#

# python imports
from __future__ import print_function, absolute_import, division, unicode_literals
import os
import glob
import sys
import argparse
import json
import numpy as np

# Image processing
from PIL import Image

EVAL_LABELS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 24, 28, 33, 34, 36, 39]
EVAL_LABEL_NAMES = ["wall", "floor", "cabinet", "bed", "chair", "sofa", "table", "door", "window", "bookshelf", "picture", "counter", "desk", "curtain", "refrigerator", "shower curtain", "toilet", "sink", "bathtub", "otherfurniture"]
EVAL_LABEL_CATS = ["indoor", "indoor", "furniture", "furniture", "furniture", "furniture", "furniture", "furniture", "furniture", "furniture", "furniture", "furniture", "furniture", "furniture", "appliance", "furniture", "furniture", "appliance", "furniture", "furniture"]
EVAL_LABEL_COLORS = [(174, 199, 232), (152, 223, 138), (31, 119, 180), (255, 187, 120), (188, 189, 34), (140, 86, 75), (255, 152, 150), (214, 39, 40), (197, 176, 213), (148, 103, 189), (196, 156, 148), (23, 190, 207), (247, 182, 210), (219, 219, 141), (255, 127, 14), (158, 218, 229), (44, 160, 44), (112, 128, 144), (227, 119, 194), (82, 84, 163)]

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

# The main method
def convert2rawimages(scannetPath, outputFolder=None):

    if outputFolder is None:
        outputFolder = scannetPath

    # find files
    search = os.path.join(scannetPath, "*", "color", "*.jpg")
    files = glob.glob(search)
    files.sort()
    # quit if we did not find anything
    if not files:
        print(
            "Did not find any files for using matching pattern {}. Please consult the README.".format(search)
        )
        sys.exit(-1)
    # a bit verbose
    print("Converting {} annotation files.".format(len(files)))

    outputBaseFile = "scannet_panoptic"
    panopticFolder = os.path.join(outputFolder, outputBaseFile)
    if not os.path.isdir(panopticFolder):
        print("Creating folder {} for panoptic segmentation JPGs".format(panopticFolder))
        os.mkdir(panopticFolder)
    print("Corresponding segmentations in .jpg format will be saved in {}".format(panopticFolder))

    for progress, f in enumerate(files):

        originalFormat = Image.open(f)
        
        parts = splitall(f)        
        fileName = parts[-1]
        sceneName = parts[-3]
        outputFileName = "{}__{}".format(sceneName, fileName)

        originalFormat.save(os.path.join(panopticFolder, outputFileName))

        print("\rProgress: {:>3.2f} %".format((progress + 1) * 100 / len(files)), end=' ')
        sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-folder",
                        dest="scannetPath",
                        help="path to the ScanNet data 'scannet_frames_25k' folder",
                        required=True,
                        type=str)
    parser.add_argument("--output-folder",
                        dest="outputFolder",
                        help="path to the output folder.",
                        default=None,
                        type=str)
    args = parser.parse_args()

    convert2rawimages(args.scannetPath, args.outputFolder)


# call the main
if __name__ == "__main__":
    main()
