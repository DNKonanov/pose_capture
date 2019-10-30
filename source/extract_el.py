import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-timeline', type=str, required=True)
parser.add_argument('-coords', type=str, required=True, help='format is coord1:coord2 (for example 10000:20000)')
parser.add_argument('-out', type=str, default=None, help='out file path')

args = parser.parse_args()


if args.out is None:
    out = args.timeline + '.out.txt'
else:
    out = args.out


coords = [int(i) for i in args.coords.split(':')]
timeline = np.loadtxt(args.timeline)

np.savetxt(out, timeline[:,coords[0]:coords[1]])

