import argparse
from calibration import calibrate
import os

parser = argparse.ArgumentParser()

parser.add_argument('-imdir1', type=str, help='folder with camera1 images', required=True)
parser.add_argument('-imdir2', type=str, help='folder with camera2 images', required=True)
parser.add_argument('-cols', type=int, default=9, help='num of cols')
parser.add_argument('-rows', type=int, default=6, help='num of rows')
parser.add_argument('-outdir', type=str, default='out', help='directory to save camera matrix and distortion coeffs')

args = parser.parse_args()

try:
    os.mkdir(args.outdir)
except FileExistsError:
    pass


P1, P2, Q = calibrate(
    args.imdir1, 
    args.imdir2, 
    cols=args.cols, 
    rows=args.rows, 
    out=args.outdir
)

print()
print('-------------PROJECTION MATRICES-------------')

print('\n\tFIRST CAMERA\n', P1)
print('\n\tSECOND CAMERA\n', P2)
print()
print('Cameras are calibrated!')