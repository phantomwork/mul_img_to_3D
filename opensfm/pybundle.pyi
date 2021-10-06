from typing import overload, Any, Dict

import numpy
from opensfm.pygeometry import Camera

X: Any
XY: Any
XYZ: Any
Y: Any
Z: Any

class Point:
    def __init__(self) -> None: ...
    @property
    def id(self) -> str: ...
    @id.setter
    def id(self, val: str) -> None: ...
    @property
    def p(self) -> numpy.ndarray: ...
    @p.setter
    def p(self, val: numpy.ndarray) -> None: ...
    @property
    def reprojection_errors(self) -> Dict[str, numpy.ndarray]: ...
    @reprojection_errors.setter
    def reprojection_errors(self, val: Dict[str, numpy.ndarray]) -> None: ...

class Reconstruction:
    def __init__(self) -> None: ...
    def get_scale(self, arg0: str) -> float: ...
    def set_scale(self, arg0: str, arg1: float) -> None: ...
    @property
    def id(self) -> str: ...
    @id.setter
    def id(self, val: str) -> None: ...

class RelativeMotion:
    def __init__(
        self,
        arg0: str,
        arg1: str,
        arg2: str,
        arg3: str,
        arg4: numpy.ndarray,
        arg5: numpy.ndarray,
        arg6: float,
    ) -> None: ...
    def set_scale_matrix(self, arg0: numpy.ndarray) -> None: ...
    @property
    def r(self) -> numpy.ndarray: ...
    @r.setter
    def r(self, val: numpy.ndarray) -> None: ...
    @property
    def reconstruction_i(self) -> str: ...
    @reconstruction_i.setter
    def reconstruction_i(self, val: str) -> None: ...
    @property
    def reconstruction_j(self) -> str: ...
    @reconstruction_j.setter
    def reconstruction_j(self, val: str) -> None: ...
    @property
    def shot_i(self) -> str: ...
    @shot_i.setter
    def shot_i(self, val: str) -> None: ...
    @property
    def shot_j(self) -> str: ...
    @shot_j.setter
    def shot_j(self, val: str) -> None: ...
    @property
    def t(self) -> numpy.ndarray: ...
    @t.setter
    def t(self, val: numpy.ndarray) -> None: ...

class RelativeRotation:
    def __init__(self, arg0: str, arg1: str, arg2: numpy.ndarray) -> None: ...
    def set_scale_matrix(self, arg0: numpy.ndarray) -> None: ...
    @property
    def r(self) -> numpy.ndarray: ...
    @r.setter
    def r(self, val: numpy.ndarray) -> None: ...
    @property
    def shot_i(self) -> str: ...
    @shot_i.setter
    def shot_i(self, val: str) -> None: ...
    @property
    def shot_j(self) -> str: ...
    @shot_j.setter
    def shot_j(self, val: str) -> None: ...

class RelativeSimilarity:
    def __init__(
        self,
        arg0: str,
        arg1: str,
        arg2: str,
        arg3: str,
        arg4: numpy.ndarray,
        arg5: numpy.ndarray,
        arg6: float,
        arg7: float,
    ) -> None: ...
    def set_scale_matrix(self, arg0: numpy.ndarray) -> None: ...
    @property
    def scale(self) -> float: ...
    @scale.setter
    def scale(self, val: float) -> None: ...

class Shot:
    def __init__(self) -> None: ...
    def get_covariance_inv_param(self, arg0: int, arg1: int) -> float: ...
    @property
    def camera(self) -> str: ...
    @camera.setter
    def camera(self, val: str) -> None: ...
    @property
    def id(self) -> str: ...
    @id.setter
    def id(self, val: str) -> None: ...
    @property
    def r(self) -> numpy.ndarray: ...
    @property
    def t(self) -> numpy.ndarray: ...

class BundleAdjuster:
    def __init__(self) -> None: ...
    def add_absolute_pan(self, arg0: str, arg1: float, arg2: float) -> None: ...
    def add_absolute_position(
        self, arg0: str, arg1: numpy.ndarray, arg2: float, arg3: str
    ) -> None: ...
    def add_heatmap(
        self, arg0: str, arg1: numpy.ndarray, arg2: int, arg3: float
    ) -> None: ...
    def add_absolute_position_heatmap(
        self, arg0: str, arg1: str, arg2: float, arg3: float, arg4: float
    ) -> None: ...
    def add_absolute_roll(self, arg0: str, arg1: float, arg2: float) -> None: ...
    def add_absolute_tilt(self, arg0: str, arg1: float, arg2: float) -> None: ...
    def add_absolute_up_vector(
        self, arg0: str, arg1: numpy.ndarray, arg2: float
    ) -> None: ...
    def add_camera(self, arg0: str, arg1: Camera, arg2: Camera, arg3: bool) -> None: ...
    def add_common_position(
        self, arg0: str, arg1: str, arg2: float, arg3: float
    ) -> None: ...
    def add_linear_motion(
        self, arg0: str, arg1: str, arg2: str, arg3: float, arg4: float, arg5: float
    ) -> None: ...
    def add_point(self, arg0: str, arg1: numpy.ndarray, arg2: bool) -> None: ...
    def add_point_position_prior(
        self, arg0: str, arg1: float, arg2: float, arg3: float, arg4: float
    ) -> None: ...
    def add_point_position_shot(
        self,
        arg0: str,
        arg1: str,
        arg2: str,
        arg3: numpy.ndarray,
        arg4: float,
        arg5: PositionConstraintType,
    ) -> None: ...
    def add_point_position_world(
        self,
        arg0: str,
        arg1: numpy.ndarray,
        arg2: float,
        arg3: float,
        arg4: PositionConstraintType,
    ) -> None: ...
    def add_point_projection_observation(self, arg0: str, arg1: str, arg2: float, arg3: numpy.ndarray) -> None: ...
    def add_position_prior(
        self, arg0: str, arg1: float, arg2: float, arg3: float, arg4: float
    ) -> None: ...
    def add_reconstruction(self, arg0: str, arg1: bool) -> None: ...
    def add_reconstruction_shot(self, arg0: str, arg1: float, arg2: str) -> None: ...
    def add_relative_motion(self, arg0: RelativeMotion) -> None: ...
    def add_relative_rotation(self, arg0: RelativeRotation) -> None: ...
    def add_relative_similarity(self, arg0: RelativeSimilarity) -> None: ...
    def add_shot(
        self,
        arg0: str,
        arg1: str,
        arg2: numpy.ndarray,
        arg3: numpy.ndarray,
        arg4: bool,
    ) -> None: ...
    def brief_report(self) -> str: ...
    def full_report(self) -> str: ...
    def get_camera(self, arg0: str) -> Camera: ...
    def get_covariance_estimation_valid(self) -> bool: ...
    def get_point(self, arg0: str) -> Point: ...
    def get_reconstruction(self, arg0: str) -> Reconstruction: ...
    def get_shot(self, arg0: str) -> Shot: ...
    def run(self) -> None: ...
    def set_adjust_absolute_position_std(self, arg0: bool) -> None: ...
    def set_compute_covariances(self, arg0: bool) -> None: ...
    def set_compute_reprojection_errors(self, arg0: bool) -> None: ...
    def set_internal_parameters_prior_sd(
        self,
        arg0: float,
        arg1: float,
        arg2: float,
        arg3: float,
        arg4: float,
        arg5: float,
        arg6: float,
        arg7: float,
    ) -> None: ...
    def set_linear_solver_type(self, arg0: str) -> None: ...
    def set_max_num_iterations(self, arg0: int) -> None: ...
    def set_num_threads(self, arg0: int) -> None: ...
    def set_origin_shot(self, arg0: str) -> None: ...
    def set_point_projection_loss_function(self, arg0: str, arg1: float) -> None: ...
    def set_relative_motion_loss_function(self, arg0: str, arg1: float) -> None: ...
    def set_scale_sharing(self, arg0: str, arg1: bool) -> None: ...
    def set_unit_translation_shot(self, arg0: str) -> None: ...
    def set_use_analytic_derivatives(self, arg0: bool) -> None: ...

class PositionConstraintType:
    X: Any = ...
    XY: Any = ...
    XYZ: Any = ...
    Y: Any = ...
    Z: Any = ...
    def __init__(self, arg0: int) -> None: ...
    @overload
    def __eq__(self, arg0: PositionConstraintType) -> bool: ...
    @overload
    def __eq__(self, arg0: int) -> bool: ...
    @overload
    def __eq__(*args, **kwargs) -> Any: ...
    def __getstate__(self) -> tuple: ...
    def __hash__(self) -> int: ...
    def __int__(self) -> int: ...
    @overload
    def __ne__(self, arg0: PositionConstraintType) -> bool: ...
    @overload
    def __ne__(self, arg0: int) -> bool: ...
    @overload
    def __ne__(*args, **kwargs) -> Any: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def __members__(self) -> dict: ...

class RAReconstruction:
    def __init__(self) -> None: ...
    @property
    def id(self) -> str: ...
    @id.setter
    def id(self, val: str) -> None: ...
    @property
    def rx(self) -> float: ...
    @rx.setter
    def rx(self, val: float) -> None: ...
    @property
    def ry(self) -> float: ...
    @ry.setter
    def ry(self, val: float) -> None: ...
    @property
    def rz(self) -> float: ...
    @rz.setter
    def rz(self, val: float) -> None: ...
    @property
    def scale(self) -> float: ...
    @scale.setter
    def scale(self, val: float) -> None: ...
    @property
    def tx(self) -> float: ...
    @tx.setter
    def tx(self, val: float) -> None: ...
    @property
    def ty(self) -> float: ...
    @ty.setter
    def ty(self, val: float) -> None: ...
    @property
    def tz(self) -> float: ...
    @tz.setter
    def tz(self, val: float) -> None: ...

class RARelativeMotionConstraint:
    def __init__(
        self,
        arg0: str,
        arg1: str,
        arg2: float,
        arg3: float,
        arg4: float,
        arg5: float,
        arg6: float,
        arg7: float,
    ) -> None: ...
    def set_scale_matrix(self, arg0: int, arg1: int, arg2: float) -> None: ...
    @property
    def reconstruction(self) -> str: ...
    @reconstruction.setter
    def reconstruction(self, val: str) -> None: ...
    @property
    def rx(self) -> float: ...
    @rx.setter
    def rx(self, val: float) -> None: ...
    @property
    def ry(self) -> float: ...
    @ry.setter
    def ry(self, val: float) -> None: ...
    @property
    def rz(self) -> float: ...
    @rz.setter
    def rz(self, val: float) -> None: ...
    @property
    def shot(self) -> str: ...
    @shot.setter
    def shot(self, val: str) -> None: ...
    @property
    def tx(self) -> float: ...
    @tx.setter
    def tx(self, val: float) -> None: ...
    @property
    def ty(self) -> float: ...
    @ty.setter
    def ty(self, val: float) -> None: ...
    @property
    def tz(self) -> float: ...
    @tz.setter
    def tz(self, val: float) -> None: ...

class RAShot:
    def __init__(self) -> None: ...
    @property
    def id(self) -> str: ...
    @id.setter
    def id(self, val: str) -> None: ...
    @property
    def rx(self) -> float: ...
    @rx.setter
    def rx(self, val: float) -> None: ...
    @property
    def ry(self) -> float: ...
    @ry.setter
    def ry(self, val: float) -> None: ...
    @property
    def rz(self) -> float: ...
    @rz.setter
    def rz(self, val: float) -> None: ...
    @property
    def tx(self) -> float: ...
    @tx.setter
    def tx(self, val: float) -> None: ...
    @property
    def ty(self) -> float: ...
    @ty.setter
    def ty(self, val: float) -> None: ...
    @property
    def tz(self) -> float: ...
    @tz.setter
    def tz(self, val: float) -> None: ...

class ReconstructionAlignment:
    def __init__(self) -> None: ...
    def add_absolute_position_constraint(
        self, arg0: str, arg1: float, arg2: float, arg3: float, arg4: float
    ) -> None: ...
    def add_common_camera_constraint(
        self, arg0: str, arg1: str, arg2: str, arg3: str, arg4: float, arg5: float
    ) -> None: ...
    def add_common_point_constraint(
        self,
        arg0: str,
        arg1: float,
        arg2: float,
        arg3: float,
        arg4: str,
        arg5: float,
        arg6: float,
        arg7: float,
        arg8: float,
    ) -> None: ...
    def add_reconstruction(
        self,
        arg0: str,
        arg1: float,
        arg2: float,
        arg3: float,
        arg4: float,
        arg5: float,
        arg6: float,
        arg7: float,
        arg8: bool,
    ) -> None: ...
    def add_relative_absolute_position_constraint(
        self, arg0: str, arg1: str, arg2: float, arg3: float, arg4: float, arg5: float
    ) -> None: ...
    def add_relative_motion_constraint(
        self, arg0: RARelativeMotionConstraint
    ) -> None: ...
    def add_shot(
        self,
        arg0: str,
        arg1: float,
        arg2: float,
        arg3: float,
        arg4: float,
        arg5: float,
        arg6: float,
        arg7: bool,
    ) -> None: ...
    def brief_report(self) -> str: ...
    def full_report(self) -> str: ...
    def get_reconstruction(self, arg0: str) -> RAReconstruction: ...
    def get_shot(self, arg0: str) -> RAShot: ...
    def run(self) -> None: ...
