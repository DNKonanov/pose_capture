import cv2
import os
import numpy as np
import sys
import matplotlib.pyplot as plt


def interpolate_3d(left_point, right_point, t=None):


    lx, ly, lz, lt = left_point
    rx, ry, rz, rt = right_point

    if lt == rt or t in [lt, rt]:
        return None

    
    if t == None:
        T = -1
    
    else:
        T = (t - lt)/(t - rt)

    return np.array([
        (T*rx - lx)/(T - 1),
        (T*ry - ly)/(T - 1),
        (T*rz - lz)/(T - 1),
        1,
    ])




def _generate_chess_points(im_dir, cols, rows):

    print(cols, rows)

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

        img = cv2.drawChessboardCorners(img, (cols,rows), corners, ret)
        cv2.imshow('img',img)
        cv2.waitKey(0)



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
        None,
    )

    print(dist1)
    


    for file in os.listdir(img_dir1):
        img = cv2.imread('{}/{}'.format(img_dir1, file))

        cv2.imshow('input', img)
        cv2.waitKey(0)

        h,  w = img.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx1, dist1, (w,h), 1, (w,h))

        print(roi)

        x,y,w,h = roi

        dst = cv2.undistort(img, mtx1, dist1, None, newcameramtx)
        
        dst = dst[y:y+h, x:x+w]
        cv2.imshow('res', dst)
        cv2.waitKey(0)

    ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(
        ObjPoints2, 
        ChessPoints2, 
        size2,
        None,
        None,
        None,
        None,
        )

    print(dist2)
    for file in os.listdir(img_dir2):
        img = cv2.imread('{}/{}'.format(img_dir2, file))

        cv2.imshow('input', img)
        cv2.waitKey(0)

        h,  w = img.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx1, dist1, (w,h), 1, (w,h))

        print(roi)

        dst = cv2.undistort(img, mtx1, dist1, None, newcameramtx)

        x,y,w,h = roi

        dst = dst[y:y+h, x:x+w]
        cv2.imshow('res', dst)
        cv2.waitKey(0)

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


def points2angle(center, point1, point2) -> float:

    b = np.array(center)
    a = np.array(point1)
    c = np.array(point2)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)