import cv2
import numpy as np
import argparse
import sys
import os
from parse_data import parse_cameras_data, parse_json


parser = argparse.ArgumentParser()
parser.add_argument('-vidname_l', type=str, help='name of the left source video (without format)')
parser.add_argument('-vidname_r', type=str, help='name of the right source video (without format)')
parser.add_argument('-jsons_l', type=str, help='keypoint jsons from the left camera', required=True)
parser.add_argument('-jsons_r', type=str, help='keypoint jsons from the right camera', required=True)
parser.add_argument(
    '-cameras_data', 
    type=str, 
    help='folder with calibration data (generated by start_calibrate.py)', 
    required=True)

args = parser.parse_args()

projMatrix1, projMatrix2 = parse_cameras_data(args.cameras_data)[-2:]

i = 0


prefix_l = args.vidname_l
file_l = '000000000000'
postfix_l = 'keypoints.json'

prefix_r = args.vidname_r
file_r = '000000000000'
postfix_r = 'keypoints.json'


current_file = 0
while True:

    file_index = file_l + str(current_file)
    file_index = file_index[len(str(current_file)):]

    keypoints_l, keypoints_l_full = parse_json('{}/{}_{}_{}'.format(args.jsons_l, prefix_l, file_index, postfix_l))
    keypoints_r, keypoints_r_full = parse_json('{}/{}_{}_{}'.format(args.jsons_r, prefix_r, file_index, postfix_r))

    points3D = cv2.triangulatePoints(
        projMatrix1,
        projMatrix2,
        keypoints_l,
        keypoints_r
    )

    points3D = np.array(points3D)[:,:-1]

    print(points3D)