#!/usr/bin/env python

import numpy as np
import argparse
import dataset
import features
import networkx as nx
from networkx.algorithms import bipartite

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def square_aspect_ratio(ax):
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    zmin, zmax = ax.get_zlim()
    rmin = min(xmin, ymin, zmin)
    rmax = max(xmax, ymax, zmax)
    r = rmax - rmin
    xm = (r - xmax + xmin) / 2
    ym = (r - ymax + ymin) / 2
    zm = (r - zmax + zmin) / 2
    ax.auto_scale_xyz([xmin - xm, xmax + xm],
                      [ymin - ym, ymax + ym],
                      [zmin - zm, zmax + zm])


def roundness(X):
    '''Compute a roundness coeficient that is 1 for points in a
    sphere and 0 for points in a plane'''
    s = np.linalg.svd(np.array(X), False, False)
    return s[-1] / s[0]



parser = argparse.ArgumentParser(description='Compute reconstructions for every pair of images with enough common tracks')
parser.add_argument('dataset',
                    help='path to the dataset to be processed')
parser.add_argument('-v', '--visual', action='store_true',
                    help='plot results during the process')
args = parser.parse_args()


data = dataset.DataSet(args.dataset)
images = data.images()


# Build a biparted graph connecting images and tracks.
g = data.tracks_graph()

# Get the image connectivity graph.
track_nodes, image_nodes = bipartite.sets(g)
image_graph = bipartite.weighted_projected_graph(g, image_nodes)


# Iterate over neighboring images.
for im1, im2 in image_graph.edges():
    print 'Matching image', im1, 'with image', im2
    d1 = data.exif_data(im1)
    d2 = data.exif_data(im2)

    t1 = g[im1]
    t2 = g[im2]
    p1 = []
    p2 = []
    for track in t1:
        if track in t2:
            p1.append(t1[track]['feature'])
            p2.append(t2[track]['feature'])
    p1 = np.array(p1)
    p2 = np.array(p2)
    if len(p1) > 20:
        R, t, inliers, Xs = features.two_view_reconstruction(p1, p2, d1, d2)
        print R, t
        print len(p1), len(inliers)

        if len(inliers) > 20:

            print 'roundness:', roundness(Xs)
            # TODO(pau): get a quality score for the reconstruction and keep only the best.
            #            a nice score might be to use SVD to find a measure of roundness of the reconstructed points.

            if args.visual:
                fig = plt.figure()
                ax = fig.add_subplot(211, projection='3d')
                X = np.array(Xs)
                ax.scatter(X[:, 0], X[:, 1], X[:, 2], c='b')
                ax.scatter([0], [0], [0], zdir='y', c='r')
                O = - np.dot(R, t)
                ax.scatter(O[0], O[1], O[2], c='g')

                square_aspect_ratio(ax)

                fig.add_subplot(212)
                features.plot_matches(data.image_as_array(im1),
                                      data.image_as_array(im2),
                                      p1[inliers],
                                      p2[inliers])



