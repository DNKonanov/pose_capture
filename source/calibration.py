import cv2
import os
import numpy as np
import sys


def _generate_chess_points(im_dir, cols, rows):

    objp = np.zeros((cols*rows,3), np.float32)
    objp[:,:2] = np.mgrid[0:cols,0:rows].T.reshape(-1,2)

    corner_points = []
    obj_points = []

    print('Images directory: {}'.format(im_dir))
    print('input images: ', end='')
    print(os.listdir(im_dir))

    for file in os.listdir(im_dir):
        img = cv2.imread('{}/{}'.format(im_dir, file), -1)

        size = img.shape[:-1]

        ret, corners = cv2.findChessboardCorners(img, (cols, rows,))
        corner_points.append(corners)
        obj_points.append(objp)

    return corner_points, obj_points, size


def _write_camera_parameters(camMat1, distCoef1, camMat2, distCoef2, out):

    np.savetxt('{}/cameraMatrix_l.txt'.format(out), np.array(camMat1))
    np.savetxt('{}/distCoeffs_l.txt'.format(out), np.array(distCoef1))

    np.savetxt('{}/cameraMatrix_r.txt'.format(out), np.array(camMat2))
    np.savetxt('{}/distCoeffs_r.txt'.format(out), np.array(distCoef2))

def calibrate(img_dir1, img_dir2, cols=9, rows=6, out='out'):

    ChessPoints1, ObjPoints1, size1 = _generate_chess_points(img_dir1, cols, rows)
    ChessPoints2, ObjPoints2, size2 = _generate_chess_points(img_dir2, cols, rows)

    if size1 != size2:
        sys.exit()


    ret1, mtx1, dist1, rvecs1, tvecs1 = cv2.calibrateCamera(
        ObjPoints1, 
        ChessPoints1, 
        size1,
        None, 
        None, 
        None, 
        None)

    ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(
        ObjPoints2, 
        ChessPoints2, 
        size1,
        None,
        None,
        None,
        None)

    _write_camera_parameters(mtx1, dist1, mtx2, dist2, out)

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(
        ObjPoints1, 
        ChessPoints1, 
        ChessPoints2, 
        mtx1, 
        dist1, 
        mtx2, 
        dist2,
        size1, 
        flags=cv2.CALIB_USE_INTRINSIC_GUESS
    )

    


    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(
        cameraMatrix1, 
        distCoeffs1, 
        cameraMatrix2, 
        distCoeffs2, 
        size1, 
        R, 
        T, 
        None,
        None,
        None, 
        None
    )

    np.savetxt('{}/projMatrix_l.txt'.format(out), P1)
    np.savetxt('{}/projMatrix_r.txt'.format(out), P2)
    
    return P1, P2, Q

