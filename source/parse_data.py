import numpy as np
import cv2
from calibration import _generate_chess_points


def parse_json(json):

    json_file = open(json)

    for line in json_file:
        keypoints = eval(line)
        break
    try:    
        kpoints_list = keypoints['people'][0]['pose_keypoints_2d']

    except:
        return None, None

    parsed_kp = []
    parsed_kp_full = []

    for i in range(0, 75, 3):
        parsed_kp.append(
            [[kpoints_list[i+1], kpoints_list[i]]]
            )
        parsed_kp_full.append([
            [kpoints_list[i+1], kpoints_list[i], kpoints_list[i+2]]]
            )
        
    return np.array(parsed_kp), np.array(parsed_kp_full)


def parse_cameras_data(cameras_info_dir):
    
    camMatrix1 = np.loadtxt('{}/cameraMatrix_l.txt'.format(cameras_info_dir))
    camMatrix2 = np.loadtxt('{}/cameraMatrix_r.txt'.format(cameras_info_dir))
    distCoeffs1 = np.loadtxt('{}/distCoeffs_l.txt'.format(cameras_info_dir))
    distCoeffs2 = np.loadtxt('{}/distCoeffs_r.txt'.format(cameras_info_dir))
    projMat1 = np.loadtxt('{}/projMatrix_l.txt'.format(cameras_info_dir))
    projMat2 = np.loadtxt('{}/projMatrix_r.txt'.format(cameras_info_dir))

    return (
        camMatrix1,
        camMatrix2,
        distCoeffs1,
        distCoeffs2,
        projMat1,
        projMat2
    )


def get_projection_matrix(left_img, right_img, mtx_l, dist_l, mtx_r, dist_r, cols=9, rows=6):

    objp = np.zeros((cols*rows,3), np.float32)
    objp[:,:2] = np.mgrid[0:cols,0:rows].T.reshape(-1,2)
    
    img_l = cv2.imread(left_img, -1)
    img_r = cv2.imread(right_img, -1)

    size = img_l.shape[:-1]

    ret_l, corners_l = cv2.findChessboardCorners(img_l, (cols, rows,), flags=cv2.CALIB_CB_FILTER_QUADS)
    ret_r, corners_r = cv2.findChessboardCorners(img_r, (cols, rows,), flags=cv2.CALIB_CB_FILTER_QUADS)
    
    
    corner_points_l = np.array([corners_l])
    corner_points_r = np.array([corners_r])

    corner_points_l = corner_points_l/2
    corner_points_r = corner_points_r/2

    obj_points = [objp]

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(
        obj_points, 
        corner_points_l, 
        corner_points_r, 
        mtx_l, 
        dist_l, 
        mtx_r, 
        dist_r,
        size, 
        flags=cv2.CALIB_FIX_INTRINSIC
    )

    


    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(
        cameraMatrix1, 
        distCoeffs1, 
        cameraMatrix2, 
        distCoeffs2, 
        size, 
        R, 
        T, 
        None,
        None,
        None, 
        None
    )
    
    return P1, P2


