# generated by fbsource/fbcode/mapillary/vision/buck_tools/stubgen.py

# Stubs for opensfm.pymap (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Tuple, List, Dict, Set, Iterator

from typing import overload

import numpy
from opensfm.pygeo import TopocentricConverter
from opensfm.pygeometry import Camera, Similarity
from opensfm.pymap import RigCamera, RigInstance, Landmark, Observation, TracksManager


class CameraView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Camera: ...
    def items(self) -> Iterator: ...
    def keys(self) -> Iterator: ...
    def values(self) -> Iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Camera: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...

class GroundControlPoint:
    def __init__(self) -> None: ...
    def add_observation(self, arg0: GroundControlPointObservation) -> None: ...
    @property
    def coordinates(self) -> Any: ...
    @coordinates.setter
    def coordinates(self, val: Any) -> None: ...
    @property
    def has_altitude(self) -> Any: ...
    @has_altitude.setter
    def has_altitude(self, val: Any) -> None: ...
    @property
    def id(self) -> Any: ...
    @id.setter
    def id(self, val: Any) -> None: ...
    @property
    def lla(self) -> Any: ...
    @lla.setter
    def lla(self, val: Any) -> None: ...
    @property
    def observations(self) -> Any: ...
    @observations.setter
    def observations(self, val: Any) -> None: ...

class GroundControlPointObservation:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: str, arg1: numpy.ndarray) -> None: ...
    @overload
    def __init__(*args, **kwargs) -> None: ...
    @property
    def projection(self) -> Any: ...
    @projection.setter
    def projection(self, val: Any) -> None: ...
    @property
    def shot_id(self) -> Any: ...
    @shot_id.setter
    def shot_id(self, val: Any) -> None: ...

class Landmark:
    def __init__(self, arg0: str, arg1: numpy.ndarray) -> None: ...
    def get_observations(self) -> Dict[Shot,int]: ...
    def number_of_observations(self) -> int: ...
    @property
    def color(self) -> Any: ...
    @color.setter
    def color(self, val: Any) -> None: ...
    @property
    def coordinates(self) -> Any: ...
    @coordinates.setter
    def coordinates(self, val: Any) -> None: ...
    @property
    def id(self) -> Any: ...
    @property
    def reprojection_errors(self) -> Any: ...
    @reprojection_errors.setter
    def reprojection_errors(self, val: Any) -> None: ...

class LandmarkView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Landmark: ...
    def items(self) -> Iterator: ...
    def keys(self) -> Iterator: ...
    def values(self) -> Iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Landmark: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...

class Map:
    def __init__(self) -> None: ...
    @overload
    def add_observation(self, shot, landmark, observation: Observation) -> None: ...
    @overload
    def add_observation(self, shot_Id: str, landmark_id: str, observation: Observation) -> None: ...
    @overload
    def add_observation(*args, **kwargs) -> Any: ...
    def clear_observations_and_landmarks(self) -> None: ...
    def clean_landmarks_below_min_observations(self, arg0: int) -> None: ...
    def compute_reprojection_errors(self, arg0: TracksManager, arg1: bool) -> Dict[str, Dict[str,numpy.ndarray]]: ...
    def create_camera(self, camera) -> Camera: ...
    def create_landmark(self, lm_id: str, global_position: numpy.ndarray) -> Landmark: ...
    @overload
    def create_pano_shot(self, arg0: str, arg1: str, arg2) -> Shot: ...
    @overload
    def create_pano_shot(self, arg0: str, arg1: str) -> Shot: ...
    @overload
    def create_pano_shot(*args, **kwargs) -> Any: ...
    def create_rig_instance(self, arg0: int, arg1: Dict[str,str]) -> RigInstance: ...
    def create_rig_camera(self, arg0) -> RigCamera: ...
    @overload
    def create_shot(self, shot_id: str, camera_id: str, pose) -> Shot: ...
    @overload
    def create_shot(self, shot_id: str, camera_id: str) -> Shot: ...
    @overload
    def create_shot(*args, **kwargs) -> Any: ...
    def get_camera(self, arg0: str) -> Camera: ...
    def get_camera_view(self) -> CameraView: ...
    def get_cameras(self) -> CameraView: ...
    def get_landmark(self, arg0: str) -> Landmark: ...
    def get_landmark_view(self) -> LandmarkView: ...
    def get_landmarks(self) -> LandmarkView: ...
    def get_pano_shot(self, arg0: str) -> Shot: ...
    def get_pano_shots(self) -> PanoShotView: ...
    def get_reference(self) -> TopocentricConverter: ...
    def get_shot(self, arg0: str) -> Shot: ...
    def get_shots(self) -> ShotView: ...
    def get_valid_observations(self, arg0: TracksManager) -> Dict[str, Dict[str,Observation]]: ...
    def get_bias(self) -> BiasView: ...
    def has_landmark(self, arg0: str) -> bool: ...
    @overload
    def remove_landmark(self, arg0: str) -> None: ...
    @overload
    def remove_landmark(*args, **kwargs) -> Any: ...
    def remove_observation(self, shot: str, landmark: str) -> None: ...
    def remove_pano_shot(self, arg0: str) -> None: ...
    def remove_shot(self, arg0: str) -> None: ...
    def set_reference(self, arg0: float, arg1: float, arg2: float) -> None: ...
    def set_bias(self, arg0: str, arg1: Similarity) -> None: ...
    def to_tracks_manager(self) -> TracksManager: ...
    def update_pano_shot(self, arg0) -> Shot: ...
    def update_rig_instance(self, arg0) -> RigInstance: ...
    def update_shot(self, arg0) -> Shot: ...

class ErrorType:
    Pixel: Any = ...
    Normalized: Any = ...
    Angular: Any = ...
    def __init__(self, arg0: int) -> None: ...
    def __eq__(self, arg0: ErrorType) -> bool: ...
    def __getstate__(self) -> tuple: ...
    def __hash__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, arg0: ErrorType) -> bool: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def __members__(self) -> dict: ...

class PanoShotView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Shot: ...
    def items(self) -> Iterator: ...
    def keys(self) -> Iterator: ...
    def values(self) -> Iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Shot: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...

class RigCamera:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0, arg1: str) -> None: ...
    @overload
    def __init__(*args, **kwargs) -> None: ...
    @property
    def id(self) -> Any: ...
    @id.setter
    def id(self, val: Any) -> None: ...
    @property
    def pose(self) -> Any: ...
    @pose.setter
    def pose(self, val: Any) -> None: ...

class RigInstance:
    def __init__(self, arg0: int) -> None: ...
    def add_shot(self, arg0: RigCamera, arg1: Shot) -> None: ...
    def keys(self) -> Set[str]: ...
    def update_instance_pose_with_shot(self, arg0: str, arg1) -> None: ...
    def update_rig_camera_pose(self, arg0: str, arg1) -> None: ...
    @property
    def camera_ids(self) -> Any: ...
    @property
    def id(self) -> Any: ...
    @id.setter
    def id(self, val: Any) -> None: ...
    @property
    def pose(self) -> Any: ...
    @pose.setter
    def pose(self, val: Any) -> None: ...
    @property
    def rig_cameras(self) -> Any: ...
    @property
    def shots(self) -> Any: ...

class RigInstanceView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: int) -> RigInstance: ...
    def items(self) -> Iterator: ...
    def keys(self) -> Iterator: ...
    def values(self) -> Iterator: ...
    def __contains__(self, arg0: int) -> bool: ...
    def __getitem__(self, arg0: int) -> RigInstance: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...

class RigCameraView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> RigCamera: ...
    def items(self) -> Iterator: ...
    def keys(self) -> Iterator: ...
    def values(self) -> Iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> RigCamera: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...

class BiasView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Similarity: ...
    def items(self) -> Iterator: ...
    def keys(self) -> Iterator: ...
    def values(self) -> Iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Similarity: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...

class Shot:
    def __init__(self, arg0: str, arg1, arg2) -> None: ...
    def bearing(self, arg0: numpy.ndarray) -> numpy.ndarray: ...
    def bearing_many(self, arg0: numpy.ndarray) -> numpy.ndarray: ...
    def get_landmark_observation(self, arg0) -> Observation: ...
    def get_observation(self, arg0: int) -> Observation: ...
    def get_valid_landmarks(self) -> List[Landmark]: ...
    def is_in_rig(self) -> bool: ...
    def project(self, arg0: numpy.ndarray) -> numpy.ndarray: ...
    def project_many(self, arg0: numpy.ndarray) -> numpy.ndarray: ...
    def remove_observation(self, arg0: int) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def camera(self) -> Any: ...
    @property
    def covariance(self) -> Any: ...
    @covariance.setter
    def covariance(self, val: Any) -> None: ...
    @property
    def id(self) -> Any: ...
    @property
    def merge_cc(self) -> Any: ...
    @merge_cc.setter
    def merge_cc(self, val: Any) -> None: ...
    @property
    def mesh(self) -> Any: ...
    @mesh.setter
    def mesh(self, val: Any) -> None: ...
    @property
    def metadata(self) -> Any: ...
    @metadata.setter
    def metadata(self, val: Any) -> None: ...
    @property
    def pose(self) -> Any: ...
    @pose.setter
    def pose(self, val: Any) -> None: ...
    @property
    def rig_camera_id(self) -> Any: ...
    @property
    def rig_instance_id(self) -> Any: ...
    @property
    def scale(self) -> Any: ...
    @scale.setter
    def scale(self, val: Any) -> None: ...

class ShotMeasurementDouble:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def has_value(self) -> Any: ...
    @property
    def value(self) -> Any: ...
    @value.setter
    def value(self, val: Any) -> None: ...

class ShotMeasurementInt:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def has_value(self) -> Any: ...
    @property
    def value(self) -> Any: ...
    @value.setter
    def value(self, val: Any) -> None: ...

class ShotMeasurementString:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def has_value(self) -> Any: ...
    @property
    def value(self) -> Any: ...
    @value.setter
    def value(self, val: Any) -> None: ...

class ShotMeasurementVec3d:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def has_value(self) -> Any: ...
    @property
    def value(self) -> Any: ...
    @value.setter
    def value(self, val: Any) -> None: ...

class ShotMeasurements:
    def __init__(self) -> None: ...
    def set(self, arg0: ShotMeasurements) -> None: ...
    def __copy__(self) -> ShotMeasurements: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def accelerometer(self) -> Any: ...
    @accelerometer.setter
    def accelerometer(self, val: Any) -> None: ...
    @property
    def capture_time(self) -> Any: ...
    @capture_time.setter
    def capture_time(self, val: Any) -> None: ...
    @property
    def compass_accuracy(self) -> Any: ...
    @compass_accuracy.setter
    def compass_accuracy(self, val: Any) -> None: ...
    @property
    def compass_angle(self) -> Any: ...
    @compass_angle.setter
    def compass_angle(self, val: Any) -> None: ...
    @property
    def gps_accuracy(self) -> Any: ...
    @gps_accuracy.setter
    def gps_accuracy(self, val: Any) -> None: ...
    @property
    def gps_position(self) -> Any: ...
    @gps_position.setter
    def gps_position(self, val: Any) -> None: ...
    @property
    def orientation(self) -> Any: ...
    @orientation.setter
    def orientation(self, val: Any) -> None: ...
    @property
    def sequence_key(self) -> Any: ...
    @sequence_key.setter
    def sequence_key(self, val: Any) -> None: ...

class ShotMesh:
    def __init__(*args, **kwargs) -> None: ...
    @property
    def faces(self) -> Any: ...
    @faces.setter
    def faces(self, val: Any) -> None: ...
    @property
    def vertices(self) -> Any: ...
    @vertices.setter
    def vertices(self, val: Any) -> None: ...

class ShotView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Shot: ...
    def items(self) -> Iterator: ...
    def keys(self) -> Iterator: ...
    def values(self) -> Iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Shot: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...

class Observation:
    def __init__(self, arg0: float, arg1: float, arg2: float, arg3: int, arg4: int, arg5: int, arg6: int) -> None: ...
    @property
    def color(self) -> numpy.ndarray: ...
    @color.setter
    def color(self, val: numpy.ndarray) -> None: ...
    @property
    def id(self) -> int: ...
    @id.setter
    def id(self, val: int) -> None: ...
    @property
    def point(self) -> numpy.ndarray: ...
    @point.setter
    def point(self, val: numpy.ndarray) -> None: ...
    @property
    def scale(self) -> float: ...
    @scale.setter
    def scale(self, val: float) -> None: ...
    @property
    def segmentation(self) -> int: ...
    @segmentation.setter
    def segmentation(self, val: int) -> None: ...
    @property
    def instance(self) -> int: ...
    @instance.setter
    def instance(self, val: int) -> None: ...

class TracksManager:
    def __init__(self) -> None: ...
    def add_observation(self, arg0: str, arg1: str, arg2: Observation) -> None: ...
    @staticmethod
    def merge_tracks_manager(self, arg0: List[TracksManager]) -> TracksManager: ...
    def as_string(self) -> str: ...
    def construct_sub_tracks_manager(self, arg0: List[str], arg1: List[str]) -> TracksManager: ...
    def get_all_common_observations(self, arg0: str, arg1: str) -> List[Tuple[str,Observation,Observation]]: ...
    def get_all_pairs_connectivity(self, shots: List[str] = ..., tracks: List[str] = ...) -> Dict[Tuple[str,str],int]: ...
    def get_observation(self, arg0: str, arg1: str) -> Observation: ...
    def get_shot_ids(self) -> List[str]: ...
    def get_shot_observations(self, arg0: str) -> Dict[str,Observation]: ...
    def get_track_ids(self) -> List[str]: ...
    def get_track_observations(self, arg0: str) -> Dict[str,Observation]: ...
    @staticmethod
    def instanciate_from_file(arg0: str) -> TracksManager: ...
    @staticmethod
    def instanciate_from_string(arg0: str) -> TracksManager: ...
    def num_shots(self) -> int: ...
    def num_tracks(self) -> int: ...
    def remove_observation(self, arg0: str, arg1: str) -> None: ...
    def write_to_file(self, arg0: str) -> None: ...
