import numpy as np

def parse_json(json):

    json_file = open(json)

    for line in json_file:
        keypoints = eval(line)
        break
        
    kpoints_list = keypoints['people'][0]['pose_keypoints_2d']

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