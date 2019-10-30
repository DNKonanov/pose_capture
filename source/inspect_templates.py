import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def inspect_video(source):


    print('Inspecting {}...'.format(source))
    
    video = cv2.VideoCapture(source)

    T_edges = []
    i = 0

    left = None
    right = None

    while True:

        ret, cap = video.read()
        i+=1

        print(i, end='')

        colorMax = np.max(cap)

        if (colorMax == 0) and (left is not None):
            right = i
            T_edges.append(
                (left, right)
            )
            left = None
            right = None
        elif colorMax != 0 and (right is None) and (left is None):
            left = i

        elif (ret == False) and (left is not None):
            T_edges.append(
                (left, i)
            )

        print('\r', end='')
        if ret == False:
            break
            print()
    print('Complete!')
    return T_edges


def _write_data(T_edges, outfile):

    out = open(outfile, 'w')

    for edge in T_edges:
        out.write('{}\t{}\n'.format(edge[0], edge[1]))

    

videos = [file for file in os.listdir('/home/dmitry/') if '.mp4' in file and 'KS_ZEV' in file]

for vid in videos:
    outs = inspect_video('/home/dmitry/{}'.format(vid))
    print(outs)
    _write_data(outs, '/home/dmitry/{}.txt'.format(vid))
