import numpy as np

def interpolate_3d(left_point, right_point, time=None):


    lx, ly, lz, lt = *left_point
    rx, ry, rz, rt = *right_point

    if lt == rt or time in [lt, rt]:
        return None

    
    if time == None:
        T = -1
    
    else:
        T = (t - lt)/(t - rt)

    return np.array([
        (T*rx - lx)/(T - 1),
        (T*ry - ly)/(T - 1),
        (T*rz - lz)/(T - 1),
    ])

