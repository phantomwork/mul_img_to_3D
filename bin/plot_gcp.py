"""Plot image crops around GCPs.
"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import argparse
import logging

import numpy as np
import matplotlib.pyplot as plt

from opensfm import features
from opensfm import io
from opensfm import dataset

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument(
        'dataset',
        help='dataset',
    )
    return parser.parse_args()


def pix_coords(x, image):
    return features.denormalized_image_coordinates(
        np.array([[x[0], x[1]]]), image.shape[1], image.shape[0])[0]


def gcp_to_ply(gcps):
    """Export GCP position as a PLY string."""
    vertices = []

    for gcp in gcps:
        p = gcp.coordinates
        c = 255, 0, 0
        s = "{} {} {} {} {} {}".format(
            p[0], p[1], p[2], int(c[0]), int(c[1]), int(c[2]))
        vertices.append(s)

    header = [
        "ply",
        "format ascii 1.0",
        "element vertex {}".format(len(vertices)),
        "property float x",
        "property float y",
        "property float z",
        "property uchar diffuse_red",
        "property uchar diffuse_green",
        "property uchar diffuse_blue",
        "end_header",
    ]

    return '\n'.join(header + vertices + [''])


def main():
    args = parse_args()
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.DEBUG)

    data = dataset.DataSetBase(args.dataset)
    reconstruction = data.load_reconstruction()[0]
    gcps = data.load_ground_control_points()

    with io.open_wt(data.data_path + '/gcp.ply') as fout:
        fout.write(gcp_to_ply(gcps))

    for gcp in gcps:
        for i, observation in enumerate(gcp.observations):
            image = data.load_image(observation.shot_id)
            shot = reconstruction.shots[observation.shot_id]

            reprojected = shot.project(gcp.coordinates)
            annotated = observation.projection
            rpixel = pix_coords(reprojected, image)
            apixel = pix_coords(annotated, image)

            n = (len(gcp.observations) + 3) / 4
            plt.subplot(n, 4, i + 1)
            plt.imshow(image)
            plt.scatter(rpixel[0], rpixel[1])
            plt.scatter(apixel[0], apixel[1])
        plt.show()


if __name__ == '__main__':
    main()
