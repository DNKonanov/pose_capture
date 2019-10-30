from scipy.stats import spearmanr, linregress
import argparse
from fastdtw import fastdtw
import numpy as np
import os

parser = argparse.ArgumentParser()

parser.add_argument('-ref', type=str, required=True, help='reference element matrix')
parser.add_argument('-timeline', type=str, required=True, help='6-dim timeline matrix in txt or directory with a number of matrices')
parser.add_argument('-timeconfig', type=str, required=True, help='frames coordinates')

args = parser.parse_args()

def align(ref, el, radius=5):

    distance, profile = fastdtw(ref, el, radius=5)

    new_ref = []
    new_el = []

    

    for p in profile:
        new_ref.append(ref[p[0]])
        new_el.append(el[p[1]])

    return distance, np.array(new_ref), np.array(new_el)

def compute_stat(aligned_ref, aligned_el):

    S = []
    for i in aligned_ref.T:
        S += list(i)
    aligned_ref = np.array(S)


    S = []
    for i in aligned_el.T:
        S += list(i)
    aligned_el = np.array(S)



    spearman_statistics = spearmanr(aligned_ref, aligned_el)
    linregress_statistics = linregress(aligned_ref, aligned_el)

    return spearman_statistics, linregress_statistics



def unpack_el(timeline, edges):
    return timeline[:,edges[0]:edges[1]]


coordsMatrix = np.loadtxt(args.timeconfig, dtype=np.int)
timeline = np.loadtxt(args.timeline, dtype=np.float64)


refs = []
try:
    inputdir = os.listdir(args.ref)
    inputdir.sort()
    
    for file in inputdir:
        refs.append(np.loadtxt('{}/{}'.format(args.ref, file), dtype=np.float64))


except NotADirectoryError:
    refs.append(np.loadtxt(args.ref))



for line in timeline:
    for i in range(len(line)):
        
        if np.isnan(line[i]):
            try:
                line[i] = (line[i-1] + line[i+1])/2
            except IndexError:
                pass
        if np.isnan(line[i]):
            line[i] = line[i-1]
        if np.isnan(line[i]):
            try:
                line[i] = line[i+1]
            except IndexError:
                line[i] = 0


template = 1
for ref in refs:
    print()
    print('-----------Template {}-------------'.format(template))
    template += 1
    for line in ref:
        for i in range(len(line)):
            
            if np.isnan(line[i]):
                try:
                    line[i] = (line[i-1] + line[i+1])/2
                except IndexError:
                    pass
            if np.isnan(line[i]):
                line[i] = line[i-1]
            if np.isnan(line[i]):
                try:
                    line[i] = line[i+1]
                except IndexError:
                    line[i] = 0


    stats = []

    for edges in coordsMatrix:

        el = unpack_el(timeline, edges)
        distance, aligned_ref, aligned_el = align(ref.T, el.T)

        stats.append(compute_stat(aligned_ref, aligned_el))

    print('Spearman', 'Pval', 'Linregress', 'Pval')
    for s in stats:
        print(s[0][0], s[0][1], s[1][2], s[1][3])

        


    