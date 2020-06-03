import networkx as nx

from opensfm import types
from opensfm import reconstruction
from opensfm import pygeometry
from opensfm import pysfm


def _add_shot(rec, shot_id, cam):
    shot = types.Shot()
    shot.id = shot_id
    shot.camera = cam
    rec.add_shot(shot)


def _add_point(rec, point_id, observations):
    point = types.Point()
    point.id = point_id
    rec.add_point(point)
    for shot_id in observations:
        obs = pysfm.Observation(100, 200, 0.5, 255, 0, 0, int(point_id))
        rec.add_observation(shot_id, point_id, obs)


def test_shot_neighborhood_linear_graph():
    rec = types.Reconstruction()
    cam = pygeometry.Camera.create_perspective(0.5, 0, 0)
    cam.id = "cam1"
    rec.add_camera(cam)
    _add_shot(rec, 'im0', cam)
    for i in range(1, 4):
        p, n = 'im' + str(i - 1), 'im' + str(i)
        _add_shot(rec, n, cam)
        _add_point(rec, str(i), [p, n])

    interior, boundary = reconstruction.shot_neighborhood(
        rec, 'im2',
        radius=1, min_common_points=1, max_interior_size=10)
    assert interior == set(['im2'])
    assert boundary == set(['im1', 'im3'])

    interior, boundary = reconstruction.shot_neighborhood(
        rec, 'im2',
        radius=2, min_common_points=1, max_interior_size=10)
    assert interior == set(['im1', 'im2', 'im3'])
    assert boundary == set(['im0'])

    interior, boundary = reconstruction.shot_neighborhood(
        rec, 'im2',
        radius=3, min_common_points=1, max_interior_size=10)
    assert interior == set(['im0', 'im1', 'im2', 'im3'])
    assert boundary == set()

    interior, boundary = reconstruction.shot_neighborhood(
        rec, 'im2',
        radius=3, min_common_points=1, max_interior_size=3)
    assert interior == set(['im1', 'im2', 'im3'])
    assert boundary == set(['im0'])


def test_shot_neighborhood_complete_graph():
    rec = types.Reconstruction()
    cam = pygeometry.Camera.create_perspective(0.5, 0, 0)
    cam.id = "cam1"
    rec.add_camera(cam)
    for i in range(4):
        _add_shot(rec, 'im' + str(i), cam)
    _add_point(rec, '1', rec.shots.keys())

    interior, boundary = reconstruction.\
        shot_neighborhood(rec, 'im2',
                          radius=2, min_common_points=1, max_interior_size=10)
    assert interior == set(['im0', 'im1', 'im2', 'im3'])
    assert boundary == set()


def test_shot_neighborhood_sorted_results():
    rec = types.Reconstruction()
    cam = pygeometry.Camera.create_perspective(0.5, 0, 0)
    cam.id = "cam1"
    rec.add_camera(cam)
    _add_shot(rec, 'im0', cam)
    _add_shot(rec, 'im1', cam)
    _add_shot(rec, 'im2', cam)
    _add_point(rec, '1', ['im0', 'im1'])
    _add_point(rec, '2', ['im0', 'im1'])
    _add_point(rec, '3', ['im0', 'im2'])

    interior, boundary = reconstruction.shot_neighborhood(
        rec, 'im0',
        radius=2, min_common_points=1, max_interior_size=2)
    assert interior == set(['im0', 'im1'])
    assert boundary == set(['im2'])

    _add_point(rec, '4', ['im0', 'im2'])
    _add_point(rec, '5', ['im0', 'im2'])

    interior, boundary = reconstruction.shot_neighborhood(
        rec, 'im0',
        radius=2, min_common_points=1, max_interior_size=2)
    assert interior == set(['im0', 'im2'])
    assert boundary == set(['im1'])
