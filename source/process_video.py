import cv2
import numpy as np
import argparse
import sys
import os
from scipy.signal import medfilt

from parse_data import parse_cameras_data, parse_json, get_projection_matrix
from calibration import points2angle, interpolate_3d

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from points_config import points_25_connectivity, angles

parser = argparse.ArgumentParser()
parser.add_argument('-jsons_l', type=str, help='keypoint jsons from the left camera', required=True)
parser.add_argument('-jsons_r', type=str, help='keypoint jsons from the right camera', required=True)
parser.add_argument(
    '-cameras_data', 
    type=str, 
    help='folder with calibration data (generated by start_calibrate.py)', 
    required=True)
parser.add_argument('-CBl', type=str, help='path to the image with chessboard from left camera', required=True)
parser.add_argument('-CBr', type=str, help='path to the image with chessboard from right camera', required=True)
parser.add_argument('-out' , type=str, help='outfile', default='out.txt')

args = parser.parse_args()

mtx_l, mtx_r, dst_l, dst_r, projMatrix_l, projMatrix_r = parse_cameras_data(args.cameras_data)

projMatrix1, projMatrix2 = get_projection_matrix(
    args.CBl, args.CBr, mtx_l, dst_l, mtx_r, dst_r,
)


keypoints_files_l = os.listdir(args.jsons_l)
keypoints_files_r = os.listdir(args.jsons_r)

print(len(keypoints_files_l), len(keypoints_files_r))

image = []
angles = []
points = []

edges = (8, 15)

print('Trinagulation...')

for i in range(min(len(keypoints_files_l), len(keypoints_files_r))):

    print(i, end='')
    keypoints_l, keypoints_l_full = parse_json(args.jsons_l + '/' + keypoints_files_l[i])
    keypoints_r, keypoints_r_full = parse_json(args.jsons_r + '/' + keypoints_files_r[i])

    angles.append([])

    if keypoints_l is None or keypoints_r is None:
        for i in points_25_connectivity:
            angles[-1].append(
                points2angle(
                    np.array([0,0,0,]),
                    np.array([0,0,0,]),
                    np.array([0,0,0,]),
                    
                )
            )

        points.append(None)

        continue


    points3D = np.array(cv2.triangulatePoints(
        projMatrix1,
        projMatrix2,
        keypoints_l,
        keypoints_r,
    ))
    points.append(points3D)
    

    for i in points_25_connectivity:
        angles[-1].append(
            points2angle(
                np.array([
                    points3D[0][points_25_connectivity[i][0]],
                    points3D[1][points_25_connectivity[i][0]],
                    points3D[2][points_25_connectivity[i][0]],]
                ),
                np.array([
                    points3D[0][points_25_connectivity[i][1]],
                    points3D[1][points_25_connectivity[i][1]],
                    points3D[2][points_25_connectivity[i][1]],]
                ),
                np.array([
                    points3D[0][points_25_connectivity[i][2]],
                    points3D[1][points_25_connectivity[i][2]],
                    points3D[2][points_25_connectivity[i][2]],]
                ) 
            )
        )
    print('\r', end='')

print()


print('Interpolation...')
found = False
firsthit = 0
while not found:
    if points[firsthit] is not None:
        found == True
        break
    firsthit += 1


new_points = []


for p in range(firsthit, len(points)):

    print(p, end='')
    if points[p] is not None:
        new_points.append(points[p])
        continue
    
    i = 1
    cycleOut = False
    while True:
        try:
            points[p + i]
        except:
            cycleOut = True
            break
        if points[p + i] is not None:
            up = i
            up_point = points[p + i].T
            break
        i += 1
    
    if cycleOut == True:
        break
    
    i = 1

    while True:
        if points[p - i] is not None:
            down = i
            down_point = points[p - i].T
            break
        i += 1    
    

    new_points.append([])
    for i in range(len(down_point)):

        point = interpolate_3d(
            list(down_point[i][:-1]) + [p - down], 
            list(up_point[i][:-1]) + [p + up], 
            t=p
        )
        new_points[-1].append(point)
    
    
    new_points[-1] = np.array(new_points[-1]).T
    print('\r', end='')

new_angles = []

for j in range(len(new_points)):

    if new_points[j] is None:
        continue
    new_angles.append([])
    for i in points_25_connectivity:
        new_angles[-1].append(
            points2angle(
                np.array([
                    new_points[j][0][points_25_connectivity[i][0]],
                    new_points[j][1][points_25_connectivity[i][0]],
                    new_points[j][2][points_25_connectivity[i][0]],]
                ),
                np.array([
                    new_points[j][0][points_25_connectivity[i][1]],
                    new_points[j][1][points_25_connectivity[i][1]],
                    new_points[j][2][points_25_connectivity[i][1]],]
                ),
                np.array([
                    new_points[j][0][points_25_connectivity[i][2]],
                    new_points[j][1][points_25_connectivity[i][2]],
                    new_points[j][2][points_25_connectivity[i][2]],]
                ) 
            )
        )


angles = np.array(angles)


short_angles = np.array([new_angles[i] for i in range(len(new_angles))]).T

np.savetxt(args.out, short_angles)
print('Complete!')