#include <foundation/types.h>
#include <glog/logging.h>
#include <map/TestView.h>
#include <map/dataviews.h>
#include <map/defines.h>
#include <map/landmark.h>
#include <map/map.h>
#include <map/pose.h>
#include <map/pybind_utils.h>
#include <map/shot.h>
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
// PYBIND11_MAKE_OPAQUE(std::unordered_map<std::string, map::TestShot>)
PYBIND11_MODULE(pymap, m) {
  py::class_<map::Pose>(m, "Pose")
      .def(py::init())
      .def("get_cam_to_world", &map::Pose::CameraToWorld)
      .def("get_world_to_cam", &map::Pose::WorldToCamera)
      // C++11
      .def("set_from_world_to_cam",
           (void (map::Pose::*)(const Eigen::Matrix4d &)) &
               map::Pose::SetFromWorldToCamera)
      .def("set_from_world_to_cam",
           (void (map::Pose::*)(const Eigen::Matrix3d &,
                                const Eigen::Vector3d &)) &
               map::Pose::SetFromWorldToCamera)
      .def("set_from_world_to_cam",
           (void (map::Pose::*)(const Eigen::Vector3d &,
                                const Eigen::Vector3d &)) &
               map::Pose::SetFromWorldToCamera)
      .def("set_from_cam_to_world",
           (void (map::Pose::*)(const Eigen::Matrix4d &)) &
               map::Pose::SetFromCameraToWorld)
      .def("set_from_cam_to_world",
           (void (map::Pose::*)(const Eigen::Matrix3d &,
                                const Eigen::Vector3d &)) &
               map::Pose::SetFromCameraToWorld)
      .def("set_from_cam_to_world",
           (void (map::Pose::*)(const Eigen::Vector3d &,
                                const Eigen::Vector3d &)) &
               map::Pose::SetFromCameraToWorld)
      // .def("set_from_world_to_cam", py::overload_cast<const Eigen::Matrix4d
      // &>(
      //                                   &map::Pose::SetFromWorldToCamera))
      // .def("set_from_world_to_cam",
      //      py::overload_cast<const Eigen::Matrix3d &, const Eigen::Vector3d
      //      &>(
      //          &map::Pose::SetFromWorldToCamera))
      // .def("set_from_world_to_cam",
      //      py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d
      //      &>(
      //          &map::Pose::SetFromWorldToCamera))
      // C++14 overload_cast
      //  .def("set_from_cam_to_world", py::overload_cast<const Eigen::Matrix4d
      //  &>(
      //                                    &map::Pose::SetFromCameraToWorld))
      //  .def("set_from_cam_to_world",
      //       py::overload_cast<const Eigen::Matrix3d &, const Eigen::Vector3d
      //       &>(
      //           &map::Pose::SetFromCameraToWorld))
      //  .def("set_from_cam_to_world",
      //       py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d
      //       &>(
      //           &map::Pose::SetFromCameraToWorld))
      //  .def("set_from_world_to_cam", py::overload_cast<const Eigen::Matrix4d
      //  &>(
      //                                    &map::Pose::SetFromWorldToCamera))
      //  .def("set_from_world_to_cam",
      //       py::overload_cast<const Eigen::Matrix3d &, const Eigen::Vector3d
      //       &>(
      //           &map::Pose::SetFromWorldToCamera))
      //  .def("set_from_world_to_cam",
      //       py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d
      //       &>(
      //           &map::Pose::SetFromWorldToCamera))

      .def("get_origin", &map::Pose::GetOrigin)
      .def("get_R_cam_to_world", &map::Pose::RotationCameraToWorld)
      .def("get_rotation_matrix", &map::Pose::RotationWorldToCamera)
      .def("get_R_world_to_cam", &map::Pose::RotationWorldToCamera)
      .def("get_R_cam_to_world_min", &map::Pose::RotationCameraToWorldMin)
      .def("get_R_world_to_cam_min", &map::Pose::RotationWorldToCameraMin)
      .def("get_t_cam_to_world", &map::Pose::TranslationCameraToWorld)
      .def("get_t_world_to_cam", &map::Pose::TranslationWorldToCamera)
      .def_property("rotation", &map::Pose::RotationWorldToCameraMin,
                    &map::Pose::SetWorldToCamRotation)
      .def_property("translation", &map::Pose::TranslationWorldToCamera,
                    &map::Pose::SetWorldToCamTranslation)
      .def("set_rotation_matrix", &map::Pose::SetWorldToCamRotationMatrix)
      .def("transform", &map::Pose::TransformWorldToCamera)
      .def("transform_inverse", &map::Pose::TransformCameraToWorld)
      .def("relative_to", &map::Pose::RelativeTo);

  py::class_<map::Map>(m, "Map")
      .def(py::init())
      .def("number_of_shots", &map::Map::NumberOfShots,
           "Returns the number of shots")
      .def("number_of_landmarks", &map::Map::NumberOfLandmarks)
      .def("number_of_cameras", &map::Map::NumberOfCameras)
      .def("create_camera", &map::Map::CreateCamera, py::arg("camera"),
           py::return_value_policy::reference_internal)
      //  .def("remove_shot_camera", &map::Map::RemoveShotCamera)
      // Landmark
      .def("create_landmark", &map::Map::CreateLandmark, py::arg("lm_id"),
           py::arg("global_position"),
           py::return_value_policy::reference_internal)
      //  .def("update_landmark", &map::Map::UpdateLandmark)
      .def("remove_landmark", (void (map::Map::*)(const map::Landmark *const)) &
                                  map::Map::RemoveLandmark)
      .def("remove_landmark", (void (map::Map::*)(const map::LandmarkId &)) &
                                  map::Map::RemoveLandmark)
      // C++14
      // .def("remove_landmark", py::overload_cast<const map::Landmark *const>(
      //                             &map::Map::RemoveLandmark))
      // .def("remove_landmark",
      //      py::overload_cast<const
      //      map::LandmarkId>(&map::Map::RemoveLandmark))

      // Shot
      // C++11
      .def(
          "create_shot",
          (map::Shot * (map::Map::*)(const map::ShotId &, const map::CameraId &,
                                     const map::Pose &)) &
              map::Map::CreateShot,
          py::arg("shot_id"), py::arg("camera_id"),
          py::arg("pose") = map::Pose(),
          py::return_value_policy::reference_internal)
      //  .def("create_shot",
      //       (map::Shot * (map::Map::*)(const map::ShotId&, const Camera &,
      //                                  const map::Pose &)) &
      //           map::Map::CreateShot,
      //       py::arg("shot_id"), py::arg("camera"), py::arg("pose") =
      //       map::Pose(), py::return_value_policy::reference_internal)
      // C++14
      // .def("create_shot",
      //      py::overload_cast<const map::ShotId&, const map::CameraId&,
      //                        const map::Pose &>(&map::Map::CreateShot),
      //      py::arg("shot_id"), py::arg("camera_id"),
      //      py::arg("pose") = map::Pose(),
      //      py::return_value_policy::reference_internal)
      // .def("create_shot",
      //      py::overload_cast<const map::ShotId&, const map::Camera &,
      //                        const map::Pose &>(&map::Map::CreateShot),
      //      py::arg("shot_id"), py::arg("camera"),
      //      py::arg("pose") = map::Pose(),
      //      py::return_value_policy::reference_internal)
      // .def("create_shot",
      //      py::overload_cast<const map::ShotId&, const std::string &,
      //                        const map::Pose &>(&map::Map::CreateShot),
      //      py::arg("shot_id"), py::arg("shot_cam"),
      //      py::arg("pose") = map::Pose(),
      //      py::return_value_policy::reference_internal)
      //  .def("update_shot_pose", &map::Map::UpdateShotPose)
      .def("remove_shot", &map::Map::RemoveShot)
      .def("get_shot", &map::Map::GetShot,
           py::return_value_policy::reference_internal)
      .def("add_observation",
           (void (map::Map::*)(map::Shot *const, map::Landmark *const,
                               const map::FeatureId)) &
               map::Map::AddObservation,
           py::arg("shot"), py::arg("landmark"), py::arg("feature_id"))
      .def("add_observation",
           (void (map::Map::*)(map::Shot *const, map::Landmark *const,
                               const Observation &)) &
               map::Map::AddObservation,
           py::arg("shot"), py::arg("landmark"), py::arg("observation"))
      .def("add_observation",
           (void (map::Map::*)(const map::ShotId &, const map::LandmarkId &,
                               const Observation &)) &
               map::Map::AddObservation,
           py::arg("shot_Id"), py::arg("landmark_id"), py::arg("observation"))

      // void AddObservation(const ShotId& shot_id, const LandmarkId& lm_id,
      // const Observation& obs);)

      // C++14
      //       .def("add_observation",
      //           py::overload_cast<map::Shot *const, map::Landmark *const,
      //                              const
      //                              map::FeatureId>(&map::Map::AddObservation),
      //            py::arg("shot"), py::arg("landmark"), py::arg("feature_id"))
      //            py::arg("shot"), py::arg("landmark"),
      //            py::arg("observation"))
      //       .def("add_observation",
      //            py::overload_cast<map::Shot *const, map::Landmark *const,
      //                              const Observation
      //                              &>(&map::Map::AddObservation),
      //            py::arg("shot"), py::arg("landmark"),
      //            py::arg("observation"))
      .def("remove_observation",
           (void (map::Map::*)(map::Shot *const, map::Landmark *const,
                               const map::FeatureId)) &
               map::Map::RemoveObservation,
           py::arg("shot"), py::arg("landmark"), py::arg("feature_id"))
      .def("remove_observation",
           (void (map::Map::*)(const map::ShotId &, const map::LandmarkId &)) &
               map::Map::RemoveObservation,
           py::arg("shot"), py::arg("landmark"))

     //  .def("get_all_shots", &map::Map::GetAllShotPointers,
     //       py::return_value_policy::reference_internal)
      .def("get_all_shots", &map::Map::GetShotView)
      .def("get_shot_view", &map::Map::GetShotView)
     //  ,
          //  py::return_value_policy::reference_internal)
      .def("get_all_cameras", &map::Map::GetCameraView)
      .def("get_camera_view", &map::Map::GetCameraView)
     //  ,
          //  py::return_value_policy::reference_internal)
      .def("get_all_landmarks", &map::Map::GetLandmarkView)
      .def("get_landmark_view", &map::Map::GetLandmarkView)
     //  ,
          //  py::return_value_policy::reference_internal)
      .def("set_reference", &map::Map::SetTopoCentricConverter)
      .def("get_reference", &map::Map::GetTopoCentricConverter)
      .def("create_camera", &map::Map::CreateCamera,
           py::return_value_policy::reference_internal)
      .def("has_landmark", &map::Map::HasLandmark)
      .def("get_landmark", &map::Map::GetLandmark,
           py::return_value_policy::reference_internal)
      .def("clear_observations_and_landmarks",
           &map::Map::ClearObservationsAndLandmarks)
      .def("get_cameras", &map::Map::GetCameras,
           py::return_value_policy::reference_internal)
      .def("get_camera", &map::Map::GetCamera,
           py::return_value_policy::reference_internal)

      ;

  py::class_<map::TopoCentricConverter>(m, "TopoCentriConverter")
      .def(py::init<>())
      .def(py::init<const double, const double, const double>())
      .def_readonly("lat", &map::TopoCentricConverter::lat_)
      .def_readonly("lon", &map::TopoCentricConverter::long_)
      .def_readonly("alt", &map::TopoCentricConverter::lat_);

  py::class_<map::Shot>(m, "Shot")
      .def(py::init<const map::ShotId &, const Camera *const,
                    const map::Pose &>())
      .def_readonly("id", &map::Shot::id_)
      .def_readonly("unique_id", &map::Shot::unique_id_)
      .def_readonly("slam_data", &map::Shot::slam_data_,
                    py::return_value_policy::reference_internal)
      .def_readwrite("mesh", &map::Shot::mesh)
      .def("get_observation", &map::Shot::GetObservation,
           py::return_value_policy::reference_internal)
      .def("get_keypoints", &map::Shot::GetKeyPoints,
           py::return_value_policy::reference_internal)
      .def("compute_num_valid_pts", &map::Shot::ComputeNumValidLandmarks,
           py::arg("min_obs_thr") = 1)
      .def("get_valid_landmarks", &map::Shot::ComputeValidLandmarks,
           py::return_value_policy::reference_internal)
      .def("init_and_take_datastructures",
           &map::Shot::InitAndTakeDatastructures)
      .def("init_keypts_and_descriptors", &map::Shot::InitKeyptsAndDescriptors)
      .def("set_pose", &map::Shot::SetPose)
      .def("get_pose", &map::Shot::GetPose,
           py::return_value_policy::reference_internal)
      .def("compute_median_depth", &map::Shot::ComputeMedianDepthOfLandmarks)
      .def("scale_landmarks", &map::Shot::ScaleLandmarks)
      .def("scale_pose", &map::Shot::ScalePose)
      .def("remove_observation", &map::Shot::RemoveLandmarkObservation)
      .def("get_camera_to_world", &map::Shot::GetCamToWorld)
      .def("get_world_to_camera", &map::Shot::GetWorldToCam)
      // TODO: Move completely away from opencv
      .def("get_obs_by_idx", &map::Shot::GetKeyPointEigen)
      .def("get_camera_name", &map::Shot::GetCameraName)
      .def_readwrite("shot_measurement", &map::Shot::shot_measurements_)
      .def_readwrite("metadata", &map::Shot::shot_measurements_)
      .def_property("pose", &map::Shot::GetPose, &map::Shot::SetPose)
      .def_property_readonly("camera", &map::Shot::GetCamera,
                             py::return_value_policy::reference_internal)
      .def("create_observation", &map::Shot::CreateObservation)
      .def("get_landmark_observation", &map::Shot::GetLandmarkObservation,
           py::return_value_policy::reference_internal)
      .def("project", &map::Shot::Project)
      .def("project_many", &map::Shot::ProjectMany)
      .def("bearing", &map::Shot::Bearing)
      .def("bearing_many", &map::Shot::BearingMany)
      // pickle support
      .def(py::pickle(
          [](const map::Shot &s) {
            auto c = s.GetCamera();
            return py::make_tuple(
                s.id_, s.unique_id_, s.GetPose().CameraToWorld(),
                py::make_tuple(c->GetProjectionParams(), c->GetDistortion(),
                               c->GetFocal(), c->GetPrincipalPoint(),
                               c->GetAspectRatio(), c->GetProjectionType(),
                               c->width, c->height, c->id));
          },
          [](py::tuple s) {
            // tuple
            auto pose = map::Pose();
            pose.SetFromCameraToWorld(s[2].cast<Mat4d>());
            auto t = s[3].cast<py::tuple>();
            // Create camera
            const auto projection_params = t[0].cast<Eigen::VectorXd>();
            const auto distortion = t[1].cast<Eigen::VectorXd>();
            const auto focal = t[2].cast<double>();
            const auto principal_point = t[3].cast<Eigen::Vector2d>();
            const auto aspect_ratio = t[4].cast<double>();
            const auto type = t[5].cast<ProjectionType>();
            const auto width = t[6].cast<int>();
            const auto height = t[7].cast<int>();
            const auto id = t[8].cast<std::string>();
            Camera camera = Camera::CreatePerspectiveCamera(0, 0, 0);
            switch (type) {
              case ProjectionType::PERSPECTIVE:
                camera = Camera::CreatePerspectiveCamera(focal, distortion[0],
                                                         distortion[1]);
                break;
              case ProjectionType::BROWN:
                camera = Camera::CreateBrownCamera(focal, aspect_ratio,
                                                   principal_point, distortion);
                break;
              case ProjectionType::FISHEYE:
                camera = Camera::CreateFisheyeCamera(focal, distortion[0],
                                                     distortion[1]);
                break;
              case ProjectionType::DUAL:
                camera = Camera::CreateDualCamera(projection_params[0], focal,
                                                  distortion[0], distortion[1]);
                break;
              case ProjectionType::SPHERICAL:
                camera = Camera::CreateSphericalCamera();
                break;
            }
            camera.width = width;
            camera.height = height;
            camera.id = id;

            // create unique_ptr
            auto cam_ptr = std::unique_ptr<Camera>(new Camera(camera));
            auto shot =
                map::Shot(t[0].cast<map::ShotId>(), std::move(cam_ptr), pose);
            shot.unique_id_ = t[1].cast<map::ShotUniqueId>();
            // shot.TransferCameraOwnership(std::move(cam));

            return shot;
          }));

  py::class_<map::SLAMShotData>(m, "SlamShotData")
      .def_readonly("undist_keypts", &map::SLAMShotData::undist_keypts_,
                    py::return_value_policy::reference_internal);

  py::class_<map::SLAMLandmarkData>(m, "SlamLandmarkData")
      .def("get_observed_ratio", &map::SLAMLandmarkData::GetObservedRatio);

  py::class_<map::ShotMeasurements>(m, "ShotMeasurements")
      .def_readwrite("gps_dop", &map::ShotMeasurements::gps_dop_)
      //  .def_readwrite("gps_pos", &map::ShotMeasurements::gps_position_)
      .def_readwrite("gps_position", &map::ShotMeasurements::gps_position_)
      .def_readwrite("orientation", &map::ShotMeasurements::orientation_)
      .def_readwrite("capture_time", &map::ShotMeasurements::capture_time_)
      .def_readwrite("accelerometer", &map::ShotMeasurements::accelerometer)
      .def_readwrite("compass", &map::ShotMeasurements::compass)
      .def_readwrite("skey", &map::ShotMeasurements::skey);

  py::class_<map::ShotMesh>(m, "ShotMesh")
      .def_property("faces", &map::ShotMesh::GetFaces, &map::ShotMesh::SetFaces)
      .def_property("vertices", &map::ShotMesh::GetVertices,
                    &map::ShotMesh::SetVertices);

  py::class_<map::Landmark>(m, "Landmark")
      .def(py::init<const map::LandmarkId &, const Eigen::Vector3d &>())
      .def_readonly("id", &map::Landmark::id_)
      .def_readonly("unique_id", &map::Landmark::unique_id_)
      .def_readwrite("slam_data", &map::Landmark::slam_data_)
      .def("get_global_pos", &map::Landmark::GetGlobalPos)
      .def_property("coordinates", &map::Landmark::GetGlobalPos,
                    &map::Landmark::SetGlobalPos)
      .def("set_global_pos", &map::Landmark::SetGlobalPos)
      .def("is_observed_in_shot", &map::Landmark::IsObservedInShot)
      .def("add_observation", &map::Landmark::AddObservation)
      .def("remove_observation", &map::Landmark::RemoveObservation)
      .def("has_observations", &map::Landmark::HasObservations)
      .def("get_observations", &map::Landmark::GetObservations,
           py::return_value_policy::reference_internal)
      .def("number_of_observations", &map::Landmark::NumberOfObservations)
      .def("get_ref_shot", &map::Landmark::GetRefShot,
           py::return_value_policy::reference_internal)
      .def("set_ref_shot", &map::Landmark::SetRefShot)
      .def("get_obs_in_shot", &map::Landmark::GetObservationInShot)
      .def_property("reprojection_errors",
                    &map::Landmark::GetReprojectionErrors,
                    &map::Landmark::SetReprojectionErrors)
      .def("remove_reprojection_error", &map::Landmark::RemoveReprojectionError)
      .def_property("color", &map::Landmark::GetColor,
                    &map::Landmark::SetColor);

  //   py::class_<map::TestView>(m, "TestView")
  //       .def(py::init<>())
  //       .def("__len__",
  //            [](const map::TestView &t) { return t.test_vector.size(); })
  //       .def("__iter__",
  //            [](const map::TestView &t) {
  //              return py::make_key_iterator(t.test_map.begin(),
  //              t.test_map.end());
  //            })
  //       .def("items", [](const map::TestView &t) {
  //         return py::make_iterator(t.test_map.begin(), t.test_map.end());
  //       });

  //   py::class_<map::TestShot>(m, "TestShot")
  //       .def_readonly("shot_id", &map::TestShot::shot_id);

  py::class_<map::ShotView>(m, "ShotView")
      .def(py::init<map::Map &>())
      .def("__len__", &map::ShotView::NumberOfShots)
      .def(
          "items",
          [](const map::ShotView &sv) {
            const auto &shots = sv.GetShots();
            return py::make_unique_ptr_iterator(shots.begin(), shots.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "values",
          [](const map::ShotView &sv) {
            const auto &shots = sv.GetShots();
            return py::make_unique_ptr_value_iterator(shots.begin(),
                                                      shots.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "__iter__",
          [](const map::ShotView &sv) {
            const auto &shots = sv.GetShots();
            return py::make_key_iterator(shots.begin(), shots.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "keys",
          [](const map::ShotView &sv) {
            const auto &shots = sv.GetShots();
            return py::make_key_iterator(shots.begin(), shots.end());
          },
          py::return_value_policy::reference_internal)
      .def("get", &map::ShotView::GetShot,
           py::return_value_policy::reference_internal)
      .def("__getitem__", &map::ShotView::GetShot,
           py::return_value_policy::reference_internal)
      .def("__contains__", &map::ShotView::HasShot);
  py::class_<map::LandmarkView>(m, "LandmarkView")
      .def(py::init<map::Map &>())
      .def("__len__", &map::LandmarkView::NumberOfLandmarks)
      .def(
          "items",
          [](const map::LandmarkView &sv) {
            const auto &lms = sv.GetLandmarks();
            return py::make_unique_ptr_iterator(lms.begin(), lms.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "values",
          [](const map::LandmarkView &sv) {
            const auto &lms = sv.GetLandmarks();
            return py::make_unique_ptr_value_iterator(lms.begin(), lms.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "__iter__",
          [](const map::LandmarkView &sv) {
            const auto &lms = sv.GetLandmarks();
            return py::make_key_iterator(lms.begin(), lms.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "keys",
          [](const map::LandmarkView &sv) {
            const auto &lms = sv.GetLandmarks();
            return py::make_key_iterator(lms.begin(), lms.end());
          },
          py::return_value_policy::reference_internal)
      .def("get", &map::LandmarkView::GetLandmark,
           py::return_value_policy::reference_internal)
      .def("__getitem__", &map::LandmarkView::GetLandmark,
           py::return_value_policy::reference_internal)
      .def("__contains__", &map::LandmarkView::HasLandmark);
  py::class_<map::CameraView>(m, "CameraView")
      .def(py::init<map::Map &>())
      .def("__len__", &map::CameraView::NumberOfCameras)
      .def(
          "items",
          [](const map::CameraView &sv) {
            const auto &cams = sv.GetCameras();
            return py::make_iterator(cams.begin(), cams.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "values",
          [](const map::CameraView &sv) {
            const auto &cams = sv.GetCameras();
            return py::make_value_iterator(cams.begin(), cams.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "__iter__",
          [](const map::CameraView &sv) {
            const auto &cams = sv.GetCameras();
            return py::make_key_iterator(cams.begin(), cams.end());
          },
          py::return_value_policy::reference_internal)
      .def(
          "keys",
          [](const map::CameraView &sv) {
            const auto &cams = sv.GetCameras();
            return py::make_key_iterator(cams.begin(), cams.end());
          },
          py::return_value_policy::reference_internal)
      .def("get", &map::CameraView::GetCamera,
           py::return_value_policy::reference_internal)
      .def("__getitem__", &map::CameraView::GetCamera,
           py::return_value_policy::reference_internal)
      .def("__contains__", &map::CameraView::HasCamera);
}