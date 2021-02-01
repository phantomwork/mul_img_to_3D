from typing import List, Tuple

from typing import overload
import Dict[opensfm.pymap
import numpy

class BAHelpers:
    def __init__(self, *args, **kwargs) -> None: ...
    def bundle(self, arg0: Dict[str,Camera], arg1, arg2: dict) -> dict: ...
    def bundle_local(self, arg0: Dict[str,Camera], arg1, arg2: str, arg3: dict) -> tuple: ...
    def detect_alignment_constraints(self, arg0: dict, arg1) -> str: ...
    def shot_neighborhood_ids(self, arg0: str, arg1: int, arg2: int, arg3: int) -> Tuple[Set[str],Set[str]]: ...

class CameraView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Camera: ...
    def items(self) -> iterator: ...
    def keys(self) -> iterator: ...
    def values(self) -> iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Camera: ...
    def __iter__(self) -> iterator: ...
    def __len__(self) -> int: ...

class GroundControlPoint:
    def __init__(self) -> None: ...
    def add_observation(self, arg0: GroundControlPointObservation) -> None: ...
    @property
    def coordinates(self) -> opensfm.pymap.ShotMeasurementVec3d: ...
    @coordinates.setter
    def coordinates(self, val: opensfm.pymap.ShotMeasurementVec3d) -> None: ...
    @property
    def has_altitude(self) -> bool: ...
    @has_altitude.setter
    def has_altitude(self, val: bool) -> None: ...
    @property
    def id(self) -> str: ...
    @id.setter
    def id(self, val: str) -> None: ...
    @property
    def lla(self) -> Dict[str,float]: ...
    @lla.setter
    def lla(self, val: Dict[str,float]) -> None: ...
    @property
    def observations(self) -> List[opensfm.pymap.GroundControlPointObservation]: ...
    @observations.setter
    def observations(self, val: List[opensfm.pymap.GroundControlPointObservation]) -> None: ...

class GroundControlPointObservation:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: str, arg1: numpy.ndarray[float64[2,1]]) -> None: ...
    @overload
    def __init__(*args, **kwargs) -> Any: ...
    @property
    def projection(self) -> numpy.ndarray[float64[2,1]]: ...
    @projection.setter
    def projection(self, val: numpy.ndarray[float64[2,1]]) -> None: ...
    @property
    def shot_id(self) -> str: ...
    @shot_id.setter
    def shot_id(self, val: str) -> None: ...

class Landmark:
    def __init__(self, arg0: str, arg1: numpy.ndarray[float64[3,1]]) -> None: ...
    def add_observation(self, arg0: Shot, arg1: int) -> None: ...
    def get_global_pos(self) -> numpy.ndarray[float64[3,1]]: ...
    def get_observations(self) -> Dict[opensfm.pymap.Shot,int]: ...
    def has_observations(self) -> bool: ...
    def is_observed_in_shot(self, arg0: Shot) -> bool: ...
    def number_of_observations(self) -> int: ...
    def remove_observation(self, arg0: Shot) -> None: ...
    def remove_reprojection_error(self, arg0: str) -> None: ...
    def set_global_pos(self, arg0: numpy.ndarray[float64[3,1]]) -> None: ...
    @property
    def color(self) -> numpy.ndarray[int32[3,1]]: ...
    @color.setter
    def color(self, val: numpy.ndarray[int32[3,1]]) -> None: ...
    @property
    def coordinates(self) -> numpy.ndarray[float64[3,1]]: ...
    @coordinates.setter
    def coordinates(self, val: numpy.ndarray[float64[3,1]]) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def reprojection_errors(self) -> Dict[str,numpy.ndarray[float64[m,1]]]: ...
    @reprojection_errors.setter
    def reprojection_errors(self, val: Dict[str,numpy.ndarray[float64[m,1]]]) -> None: ...
    @property
    def unique_id(self) -> int: ...

class LandmarkView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Landmark: ...
    def items(self) -> iterator: ...
    def keys(self) -> iterator: ...
    def values(self) -> iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Landmark: ...
    def __iter__(self) -> iterator: ...
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
    @overload
    def create_camera(self, camera: Camera) -> Camera: ...
    @overload
    def create_camera(*args, **kwargs) -> Any: ...
    def create_landmark(self, *args, **kwargs) -> Any: ...
    def create_pano_shot(*args, **kwargs) -> Any: ...
    def create_shot(*args, **kwargs) -> Any: ...
    def get_cameras(self, *args, **kwargs) -> Any: ...
    def get_landmarks(self, *args, **kwargs) -> Any: ...
    def get_pano_shots(self, *args, **kwargs) -> Any: ...
    def get_shots(self, *args, **kwargs) -> Any: ...
    def get_camera(self, arg0: str) -> Camera: ...
    def get_camera_view(self, *args, **kwargs) -> Any: ...
    def get_landmark(self, *args, **kwargs) -> Any: ...
    def get_landmark_view(self, *args, **kwargs) -> Any: ...
    def get_pano_shot(self, *args, **kwargs) -> Any: ...
    def get_reference(self, *args, **kwargs) -> Any: ...
    def get_shot(self, *args, **kwargs) -> Any: ...
    def has_landmark(self, arg0: str) -> bool: ...
    def number_of_cameras(self) -> int: ...
    def number_of_landmarks(self) -> int: ...
    def number_of_pano_shots(self) -> int: ...
    def number_of_shots(self) -> int: ...
    @overload
    def remove_landmark(self, arg0) -> None: ...
    @overload
    def remove_landmark(self, arg0: str) -> None: ...
    @overload
    def remove_landmark(*args, **kwargs) -> Any: ...
    @overload
    def remove_observation(self, shot, landmark, feature_id: int) -> None: ...
    @overload
    def remove_observation(self, shot: str, landmark: str) -> None: ...
    @overload
    def remove_observation(*args, **kwargs) -> Any: ...
    def remove_pano_shot(self, arg0: str) -> None: ...
    def remove_shot(self, arg0: str) -> None: ...
    def set_reference(self, arg0: float, arg1: float, arg2: float) -> None: ...
    def update_pano_shot(self, *args, **kwargs) -> Any: ...
    def update_shot(self, *args, **kwargs) -> Any: ...

class PanoShotView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Shot: ...
    def items(self) -> iterator: ...
    def keys(self) -> iterator: ...
    def values(self) -> iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Shot: ...
    def __iter__(self) -> iterator: ...
    def __len__(self) -> int: ...

class Shot:
    def __init__(self, *args, **kwargs) -> None: ...
    def bearing(self, arg0: numpy.ndarray[float64[2,1]]) -> numpy.ndarray[float64[3,1]]: ...
    def bearing_many(self, arg0: numpy.ndarray[float64[m,2]]) -> numpy.ndarray[float64[m,3]]: ...
    def compute_num_valid_pts(self, min_obs_thr: int = ...) -> int: ...
    def create_observation(self, arg0, arg1: numpy.ndarray[float64[2,1]], arg2: float, arg3: numpy.ndarray[int32[3,1]], arg4: int) -> None: ...
    def get_camera_name(self) -> str: ...
    def get_camera_to_world(self) -> numpy.ndarray[float64[4,4]]: ...
    def get_landmark_observation(self, arg0) -> Observation: ...
    def get_observation(self, arg0: int) -> Observation: ...
    def get_pose(self, *args, **kwargs) -> Any: ...
    def get_valid_landmarks(self, *args, **kwargs) -> Any: ...
    def get_world_to_camera(self) -> numpy.ndarray[float64[4,4]]: ...
    def project(self, arg0: numpy.ndarray[float64[3,1]]) -> numpy.ndarray[float64[2,1]]: ...
    def project_many(self, arg0: numpy.ndarray[float64[m,3]]) -> numpy.ndarray[float64[m,2]]: ...
    def remove_observation(self, arg0: int) -> None: ...
    def scale_landmarks(self, arg0: float) -> None: ...
    def scale_pose(self, arg0: float) -> None: ...
    def set_pose(self, arg0) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def camera(self) -> Camera: ...
    @property
    def covariance(self) -> numpy.ndarray[float64[m,n]]: ...
    @covariance.setter
    def covariance(self, val: numpy.ndarray[float64[m,n]]) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def merge_cc(self) -> int: ...
    @merge_cc.setter
    def merge_cc(self, val: int) -> None: ...
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
    def scale(self) -> float: ...
    @scale.setter
    def scale(self, val: float) -> None: ...
    @property
    def unique_id(self) -> int: ...

class ShotMeasurementDouble:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def has_value(self) -> bool: ...
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, val: float) -> None: ...

class ShotMeasurementInt:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def has_value(self) -> bool: ...
    @property
    def value(self) -> int: ...
    @value.setter
    def value(self, val: int) -> None: ...

class ShotMeasurementString:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def has_value(self) -> bool: ...
    @property
    def value(self) -> str: ...
    @value.setter
    def value(self, val: str) -> None: ...

class ShotMeasurementVec3d:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def has_value(self) -> bool: ...
    @property
    def value(self) -> numpy.ndarray[float64[3,1]]: ...
    @value.setter
    def value(self, val: numpy.ndarray[float64[3,1]]) -> None: ...

class ShotMeasurements:
    def __init__(self) -> None: ...
    def set(self, arg0: ShotMeasurements) -> None: ...
    def __copy__(self) -> ShotMeasurements: ...
    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def accelerometer(self) -> opensfm.pymap.ShotMeasurementVec3d: ...
    @accelerometer.setter
    def accelerometer(self, val: opensfm.pymap.ShotMeasurementVec3d) -> None: ...
    @property
    def capture_time(self) -> opensfm.pymap.ShotMeasurementDouble: ...
    @capture_time.setter
    def capture_time(self, val: opensfm.pymap.ShotMeasurementDouble) -> None: ...
    @property
    def compass_accuracy(self) -> opensfm.pymap.ShotMeasurementDouble: ...
    @compass_accuracy.setter
    def compass_accuracy(self, val: opensfm.pymap.ShotMeasurementDouble) -> None: ...
    @property
    def compass_angle(self) -> opensfm.pymap.ShotMeasurementDouble: ...
    @compass_angle.setter
    def compass_angle(self, val: opensfm.pymap.ShotMeasurementDouble) -> None: ...
    @property
    def gps_accuracy(self) -> opensfm.pymap.ShotMeasurementDouble: ...
    @gps_accuracy.setter
    def gps_accuracy(self, val: opensfm.pymap.ShotMeasurementDouble) -> None: ...
    @property
    def gps_position(self) -> opensfm.pymap.ShotMeasurementVec3d: ...
    @gps_position.setter
    def gps_position(self, val: opensfm.pymap.ShotMeasurementVec3d) -> None: ...
    @property
    def orientation(self) -> opensfm.pymap.ShotMeasurementInt: ...
    @orientation.setter
    def orientation(self, val: opensfm.pymap.ShotMeasurementInt) -> None: ...
    @property
    def sequence_key(self) -> opensfm.pymap.ShotMeasurementString: ...
    @sequence_key.setter
    def sequence_key(self, val: opensfm.pymap.ShotMeasurementString) -> None: ...

class ShotMesh:
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def faces(self) -> numpy.ndarray[float64[m,n]]: ...
    @faces.setter
    def faces(self, val: numpy.ndarray[float64[m,n]]) -> None: ...
    @property
    def vertices(self) -> numpy.ndarray[float64[m,n]]: ...
    @vertices.setter
    def vertices(self, val: numpy.ndarray[float64[m,n]]) -> None: ...

class ShotView:
    def __init__(self, arg0: Map) -> None: ...
    def get(self, arg0: str) -> Shot: ...
    def items(self) -> iterator: ...
    def keys(self) -> iterator: ...
    def values(self) -> iterator: ...
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: str) -> Shot: ...
    def __iter__(self) -> iterator: ...
    def __len__(self) -> int: ...

class TopocentricConverter:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None: ...
    @overload
    def __init__(*args, **kwargs) -> Any: ...
    @property
    def alt(self) -> float: ...
    @property
    def lat(self) -> float: ...
    @property
    def lon(self) -> float: ...
