import cv2
import numpy as np

from opensfm import csfm


def compute_depthmap(data, reconstruction, shot_id):
    neighbors = find_neighboring_images(shot_id, reconstruction)
    print shot_id, neighbors
    de = csfm.DepthmapEstimator()
    images = {}
    for sid in neighbors:
        shot = reconstruction.shots[sid]
        assert shot.camera.projection_type == 'perspective'
        color_image = data.image_as_array(shot_id)
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)
        original_height, original_width = gray_image.shape
        width = 320
        height = 320 * original_height / original_width
        images[sid] = cv2.resize(gray_image, (width, height))
        K = shot.camera.get_K_in_pixel_coordinates(width, height)
        R = shot.pose.get_rotation_matrix()
        t = shot.pose.translation
        de.add_view(K, R, t, images[sid])
    depth, score = de.compute()

    import matplotlib.pyplot as pl
    pl.imshow(depth)
    pl.show()

    print depth


def find_neighboring_images(shot_id, reconstruction, num_neighbors=5):
    """Find closest images."""
    shot = reconstruction.shots[shot_id]
    others = reconstruction.shots.values()
    distances = [distance_between_shots(shot, other) for other in others]
    pairs = sorted(zip(distances, others))
    return [s.id for d, s in pairs[:num_neighbors]]


def distance_between_shots(shot, other):
    o1 = shot.pose.get_origin()
    o2 = other.pose.get_origin()
    l = o2 - o1
    return np.sqrt(np.sum(l**2))
