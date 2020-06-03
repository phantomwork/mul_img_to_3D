#pragma once

#include <Eigen/Core>
#include <unordered_map>
#include <map>
#include <memory>

#include <map/defines.h>
#include <map/pose.h>
#include <map/geo.h>
#include <map/shot.h>
#include <map/landmark.h>
#include <map/defines.h>
#include <map/dataviews.h>
#include <sfm/tracks_manager.h>
#include <geometry/camera.h>
namespace map
{
// class Shot;
// class Landmark;

class Map 
{
public:
  EIGEN_MAKE_ALIGNED_OPERATOR_NEW
// Camera Methods
  // TODO: Removing a camera might be problematic while shots are still using it.
  // void RemoveCamera(const CameraId cam_id);
  std::vector<Camera*> GetCameras();
  Camera* GetCamera(const CameraId& cam_id);
  Camera* CreateCamera(const Camera& cam);
  const std::unordered_map<CameraId, Camera>& GetAllCameras() const { return cameras_; };
  CameraView GetCameraView() { return CameraView(*this);}
  bool HasCamera(const CameraId& cam_id) const {
    return cameras_.count(cam_id) > 0;
  }

  // Shot Methods
  Shot* CreateShot(const ShotId& shot_id, const CameraId& camera_id, const Pose& pose = Pose());
  Shot* CreateShot(const ShotId& shot_id, const Camera* const cam, const Pose& pose = Pose());
  Shot* GetShot(const ShotId& shot_id);
  void RemoveShot(const ShotId& shot_id);
  bool HasLandmark(const LandmarkId& lm_id) const { return landmarks_.count(lm_id) > 0; }
  bool HasShot(const ShotId& shot_id) const { return shots_.find(shot_id) != shots_.end(); }
  const std::unordered_map<ShotId, std::unique_ptr<Shot>>& GetAllShots() const { return shots_; }
  ShotView GetShotView() { return ShotView(*this); }

  // Landmark
  Landmark* CreateLandmark(const LandmarkId& lm_id, const Vec3d& global_pos);
  Landmark* GetLandmark(const LandmarkId& lm_id);
  void RemoveLandmark(const Landmark* const lm);
  void RemoveLandmark(const LandmarkId& lm_id);
  void ReplaceLandmark(Landmark* old_lm, Landmark* new_lm);
  const std::unordered_map<LandmarkId, std::unique_ptr<Landmark>>& GetAllLandmarks() const { return landmarks_; };
  LandmarkView GetLandmarkView() { return LandmarkView(*this); }

  //Observation methods
  void AddObservation(Shot *const shot,  Landmark *const lm, const FeatureId feat_id);
  void AddObservation(const ShotId& shot_id, const LandmarkId& lm_id, const FeatureId feat_id);
  void AddObservation(Shot *const shot,  Landmark *const lm, const Observation& obs);
  void AddObservation(const ShotId& shot_id, const LandmarkId& lm_id, const Observation& obs);
  void RemoveObservation(Shot *const shot,  Landmark *const lm, const FeatureId feat_id);
  void RemoveObservation(const ShotId& shot_id, const LandmarkId& lm_id);
  void ClearObservationsAndLandmarks();

  // Map information and access methods
  size_t NumberOfShots() const { return shots_.size(); }
  size_t NumberOfLandmarks() const { return landmarks_.size(); }
  size_t NumberOfCameras() const { return cameras_.size(); }
  std::map<Landmark*, FeatureId> GetObservationsOfShot(const Shot* shot);
  std::map<Shot*, FeatureId> GetObservationsOfPoint(const Landmark* point);

  // TopoCentriConverter
  const TopoCentricConverter& GetTopoCentricConverter() const {
    return topo_conv_;
  }

  void SetTopoCentricConverter(const double lat, const double longitude,
                               const double alt) {
    topo_conv_.lat_ = lat;
    topo_conv_.long_ = longitude;
    topo_conv_.alt_ = alt;
  }

private:
  std::unordered_map<CameraId, Camera> cameras_;
  // TODO: Think about switching to objects instead of unique_ptrs
  std::unordered_map<ShotId, std::unique_ptr<Shot>> shots_;
  std::unordered_map<LandmarkId, std::unique_ptr<Landmark>> landmarks_;
  TopoCentricConverter topo_conv_;

  LandmarkUniqueId landmark_unique_id_ = 0;
  ShotUniqueId shot_unique_id_ = 0;
};

} // namespace map