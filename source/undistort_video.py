import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-camera_matrix', type=str, help='camera matrix generated by start_calibration.py script', required=True)
parser.add_argument('-dst_coef', type=str, help='distortion coefficients generated by start_calibration.py script', required=True)
parser.add_argument('-video', type=str, help='path to input video', required=True)
parser.add_argument('-write_video', type='str', default='out.avi', help='output video (avi format)')

args = parser.parse_args()

video = cv2.VideoCapture(args.video)