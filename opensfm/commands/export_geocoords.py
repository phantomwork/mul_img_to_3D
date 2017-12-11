import logging

import numpy as np
import pyproj

from opensfm import dataset
from opensfm import geo

logger = logging.getLogger(__name__)


class Command:
    name = 'export_geocoords'
    help = "Export reconstructions in geographic coordinates"

    def add_arguments(self, parser):
        parser.add_argument('dataset', help='dataset to process')
        parser.add_argument('--proj',
                            help='PROJ.4 projection string',
                            required=True)

    def run(self, args):
        data = dataset.DataSet(args.dataset)
        reference = data.load_reference_lla()
        reconstructions = data.load_reconstruction()

        projection = pyproj.Proj(args.proj)
        transformation = self._get_transformation(reference, projection)

        for r in reconstructions:
            self._transform_reconstruction(r, transformation)
        data.save_reconstruction(reconstructions, 'reconstruction.geocoords.json')

        self._transform_dense_point_cloud(data, reference, transformation)

    def _get_transformation(self, reference, projection):
        """Get the linear transform from reconstruction coords to geocoords."""
        p = [[1, 0, 0],
             [0, 1, 0],
             [0, 0, 1],
             [0, 0, 0]]
        q = [self._transform(point, reference, projection) for point in p]

        transformation = np.array([
            [q[0][0] - q[3][0], q[1][0] - q[3][0], q[2][0] - q[3][0], q[3][0]],
            [q[0][1] - q[3][1], q[1][1] - q[3][1], q[2][1] - q[3][1], q[3][1]],
            [q[0][2] - q[3][2], q[1][2] - q[3][2], q[2][2] - q[3][2], q[3][2]],
            [0, 0, 0, 1]
        ])
        return transformation

    def _transform(self, point, reference, projection):
        lat, lon, altitude = geo.lla_from_topocentric(
            point[0], point[1], point[2],
            reference['latitude'], reference['longitude'], reference['altitude'])
        easting, northing = projection(lon, lat)
        return [easting, northing, altitude]

    def _transform_reconstruction(self, reconstruction, transformation):
        """Apply a transformation to a reconstruction in-place."""
        A, b = transformation[:3, :3], transformation[:3, 3]
        A1 = np.linalg.inv(A)
        b1 = -np.dot(A1, b)

        for shot in reconstruction.shots.values():
            R = shot.pose.get_rotation_matrix()
            t = shot.pose.translation
            shot.pose.set_rotation_matrix(np.dot(R, A1))
            shot.pose.translation = list(np.dot(R, b1) + t)

        for point in reconstruction.points.values():
            point.coordinates = list(np.dot(A, point.coordinates) + b)

    def _transform_dense_point_cloud(self, data, reference, transformation):
        A, b = transformation[:3, :3], transformation[:3, 3]
        input_path = data._depthmap_path() + '/merged.ply'
        output_path = data._depthmap_path() + '/merged.geocoords.ply'
        with open(input_path) as fin:
            with open(output_path, 'w') as fout:
                for i, line in enumerate(fin):
                    if i < 13:
                        fout.write(line)
                    else:
                        x, y, z, nx, ny, nz, red, green, blue = line.split()
                        x, y, z = np.dot(A, map(float, [x, y, z])) + b
                        nx, ny, nz = np.dot(A, map(float, [nx, ny, nz]))
                        fout.write(
                            "{} {} {} {} {} {} {} {} {}\n".format(
                                x, y, z, nx, ny, nz, red, green, blue))
