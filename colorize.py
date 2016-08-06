#!/usr/bin/python

import os

os.environ['GLOG_minloglevel'] = '2'
import time
import numpy as np
import caffe
import skimage.color as color
import scipy
import scipy.ndimage.interpolation as sni
from os import listdir
from os.path import isfile, join
import sys, getopt

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colorizeFile(input, output):
    caffemodel = 'colorization_release_v0.caffemodel'
    prototxt = 'colorization_deploy_v0.prototxt'

    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    (H_in, W_in) = net.blobs['data_l'].data.shape[2:]  # get input shape
    (H_out, W_out) = net.blobs['class8_ab'].data.shape[2:]  # get output shape
    net.blobs['Trecip'].data[...] = 6 / np.log(10)  # 1/T, set annealing temperature
    # (We found that we had introduced a factor of log(10). We will update the arXiv shortly.)
    # load the original image
    img_rgb = caffe.io.load_image(input)

    img_lab = color.rgb2lab(img_rgb)  # convert image to lab color space
    img_l = img_lab[:, :, 0]  # pull out L channel
    (H_orig, W_orig) = img_rgb.shape[:2]  # original image size

    # resize image to network input size
    img_rs = caffe.io.resize_image(img_rgb, (H_in, W_in))  # resize image to network input size
    img_lab_rs = color.rgb2lab(img_rs)
    img_l_rs = img_lab_rs[:, :, 0]

    net.blobs['data_l'].data[0, 0, :, :] = img_l_rs - 50  # subtract 50 for mean-centering
    net.forward()  # run network

    ab_dec = net.blobs['class8_ab'].data[0, :, :, :].transpose((1, 2, 0))  # this is our result
    ab_dec_us = sni.zoom(ab_dec,
                         (1. * H_orig / H_out, 1. * W_orig / W_out, 1))  # upsample to match size of original image L

    img_lab_out = np.concatenate((img_l[:, :, np.newaxis], ab_dec_us), axis=2)  # concatenate with original image L
    img_rgb_out = np.clip(color.lab2rgb(img_lab_out), 0, 1)  # convert back to rgb

    scipy.misc.imsave(output, img_rgb_out)

    return;


def colorizeDir(inputDir, outputDir):
    imagefiles = [f for f in listdir(inputDir) if isfile(join(inputDir, f))]

    for image in imagefiles:
        (imageName, imageExt) = os.path.splitext(os.path.basename(image))

        input = inputDir + image
        output = outputDir + imageName + '_color' + imageExt

        print "Processing file:"
        print "input =" + input
        print "output =" + output

        start = time.time()

        colorizeFile(input, output)

        end = time.time()

        print "Duration: %.0f" % (end - start)

def printColor(message, color):
    print color + message + bcolors.ENDC

def printGreen(message):
    printColor(message, bcolors.OKGREEN)

def printError(message):
    printColor(message, bcolors.FAIL)

def usage():
    printGreen('Usage:')
    printGreen('colorize.py -i <inputdirectory> -o <outputdirectory>')
    return;

def main(argv):
    inputDir = ''
    outputDir = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["idir=", "odir="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputDir = arg
        elif opt in ("-o", "--odir"):
            outputDir = arg

    if (inputDir == '' or outputDir == ''):
        usage()
        sys.exit(2)

    if(not os.path.isdir(inputDir)):
        printError ('Can not locate input directory "' + inputDir + '"')
        sys.exit(3)

    if(not os.path.isdir(outputDir)):
        printError('Can not locate output directory "' + outputDir + '"')
        sys.exit(3)

    if(not os.access(outputDir, os.R_OK)):
        printError('The intput directory "' + outputDir + '" is not readable')
        sys.exit(4)

    if(not os.access(outputDir, os.W_OK)):
        printError('The output directory "' + outputDir + '" is not writeable')
        sys.exit(4)

    colorizeDir(inputDir,outputDir)
    return;

if __name__ == "__main__":
    main(sys.argv[1:])
