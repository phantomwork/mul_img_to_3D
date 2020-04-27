#include <sfm/tracks_manager.h>

#include <unordered_set>

namespace {
int GetTracksFileVersion(std::ifstream& fstream) {
  const auto current_position = fstream.tellg();

  std::string line;
  std::getline(fstream, line);

  int version = 0;
  if (line.find(TracksManager::TRACKS_HEADER) == 0) {
    version = std::atoi(line.substr(TracksManager::TRACKS_HEADER.length() + 2).c_str());
  } else {
    fstream.seekg(current_position);
  }
  return version;
}

void WriteToFileCurrentVersion(std::ofstream& ostream,
                               const TracksManager& manager) {
  const auto shotsIDs = manager.GetShotIds();
  for (const auto& shotID : shotsIDs) {
    const auto observations = manager.GetObservationsOfShot(shotID);
    for (const auto& observation : observations) {
      ostream << shotID << "\t" << observation.first << "\t"
              << observation.second.id << "\t" << observation.second.point(0)
              << "\t" << observation.second.point(1) << "\t"
              << observation.second.scale << "\t" << observation.second.color(0)
              << "\t" << observation.second.color(1) << "\t"
              << observation.second.color(2) << std::endl;
    }
  }
}

Observation InstanciateObservation(double x, double y, double scale, int id,
                                   int r, int g, int b) {
  Observation observation;
  observation.point << x, y;
  observation.scale = scale;
  observation.id = id;
  observation.color << r, g, b;
  return observation;
}

TracksManager InstanciateFromFileV0(std::ifstream& fstream) {
  ShotId image = "";
  TrackId trackID = "";
  int featureID = -1;
  double x = -1.0, y = -1.0;
  int r = 0, g = 0, b = 0;

  TracksManager manager;
  while (fstream >> image >> trackID >> featureID >> x >> y >> r >> g >> b) {
    auto observation = InstanciateObservation(x, y, 0., featureID, r, g, b);
    manager.AddObservation(image, trackID, observation);
  }
  return manager;
}

TracksManager InstanciateFromFileV1(std::ifstream& fstream) {
  ShotId image = "";
  TrackId trackID = "";
  int featureID = -1;
  double x = -1.0, y = -1.0, scale = 0.;
  int r = 0, g = 0, b = 0;

  TracksManager manager;
  while (fstream >> image >> trackID >> featureID >> x >> y >> scale >> r >>
         g >> b) {
    auto observation = InstanciateObservation(x, y, scale, featureID, r, g, b);
    manager.AddObservation(image, trackID, observation);
  }
  return manager;
}
}  // namespace

void TracksManager::AddObservation(const ShotId& shot_id,
                                   const TrackId& track_id,
                                   const Observation& observation) {
  tracks_per_shot_[shot_id][track_id] = observation;
  shot_per_tracks_[track_id][shot_id] = observation;
}

void TracksManager::DeleteObservation(const ShotId& shot_id,
                                      const TrackId& track_id) {
  const auto findShot = tracks_per_shot_.find(shot_id);
  if (findShot == tracks_per_shot_.end()) {
    throw std::runtime_error("Accessing invalid shot ID");
  }
  const auto findPoint = shot_per_tracks_.find(track_id);
  if (findPoint == shot_per_tracks_.end()) {
    throw std::runtime_error("Accessing invalid point ID");
  }
  findShot->second.erase(track_id);
  findPoint->second.erase(shot_id);
}

int TracksManager::NumShots() const {
  return tracks_per_shot_.size();
}

int TracksManager::NumTracks() const {
  return shot_per_tracks_.size();
}

std::vector<ShotId> TracksManager::GetShotIds() const {
  std::vector<ShotId> shots;
  shots.reserve(tracks_per_shot_.size());
  for (const auto& it : tracks_per_shot_) {
    shots.push_back(it.first);
  }
  return shots;
}

std::vector<TrackId> TracksManager::GetTrackIds() const {
  std::vector<TrackId> tracks;
  tracks.reserve(shot_per_tracks_.size());
  for (const auto& it : shot_per_tracks_) {
    tracks.push_back(it.first);
  }
  return tracks;
}

Observation TracksManager::GetObservation(const ShotId& shot,
                                          const TrackId& point) const {
  const auto findShot = tracks_per_shot_.find(shot);
  if (findShot == tracks_per_shot_.end()) {
    throw std::runtime_error("Accessing invalid shot ID");
  }
  const auto findPoint = findShot->second.find(point);
  if (findPoint == findShot->second.end()) {
    throw std::runtime_error("Accessing invalid point ID");
  }
  return findPoint->second;
}

// Not sure if we use that
std::unordered_map<TrackId, Observation> TracksManager::GetObservationsOfShot(
    const ShotId& shot) const {
  const auto findShot = tracks_per_shot_.find(shot);
  if (findShot == tracks_per_shot_.end()) {
    throw std::runtime_error("Accessing invalid shot ID");
  }
  return findShot->second;
}

// For point triangulation
std::unordered_map<ShotId, Observation> TracksManager::GetObservationsOfPoint(
    const TrackId& point) const {
  const auto findPoint = shot_per_tracks_.find(point);
  if (findPoint == shot_per_tracks_.end()) {
    throw std::runtime_error("Accessing invalid point ID");
  }
  return findPoint->second;
}

TracksManager TracksManager::ConstructSubTracksManager(
    const std::vector<TrackId>& points,
    const std::vector<ShotId>& shots) const {
  std::unordered_set<TrackId> shotsTmp;
  for (const auto& id : shots) {
    shotsTmp.insert(id);
  }

  TracksManager subset;
  for (const auto& point_id : points) {
    const auto findPoint = shot_per_tracks_.find(point_id);
    if (findPoint == shot_per_tracks_.end()) {
      continue;
    }
    for (const auto& obs : findPoint->second) {
      const auto& shot_id = obs.first;
      if (shotsTmp.find(shot_id) == shotsTmp.end()) {
        continue;
      }
      subset.AddObservation(shot_id, point_id, obs.second);
    }
  }
  return subset;
}

std::vector<TracksManager::KeyPointTuple>
TracksManager::GetAllCommonObservations(const ShotId& shot1,
                                        const ShotId& shot2) const {
  auto findShot1 = tracks_per_shot_.find(shot1);
  auto findShot2 = tracks_per_shot_.find(shot2);
  if (findShot1 == tracks_per_shot_.end() ||
      findShot2 == tracks_per_shot_.end()) {
    throw std::runtime_error("Accessing invalid shot ID");
  }

  std::unordered_map<TrackId, std::vector<Observation>> per_track;
  for (const auto& p : findShot1->second) {
    per_track[p.first].push_back(p.second);
  }
  for (const auto& p : findShot2->second) {
    per_track[p.first].push_back(p.second);
  }

  std::vector<KeyPointTuple> tuples;
  for (const auto& p : per_track) {
    if (p.second.size() < 2) {
      continue;
    }
    tuples.push_back(std::make_tuple(p.first, p.second[0], p.second[1]));
  }
  return tuples;
}

std::unordered_map<TracksManager::ShotPair,
                   std::vector<TracksManager::KeyPointTuple>, HashPair>
TracksManager::GetAllCommonObservationsAllPairs() const {
  std::unordered_map<ShotPair, std::vector<KeyPointTuple>, HashPair>
      common_per_pair;
  for (const auto& track : shot_per_tracks_) {
    for (std::unordered_map<ShotId, Observation>::const_iterator it1 =
             track.second.begin();
         it1 != track.second.end(); ++it1) {
      const auto& shotID1 = it1->first;
      for (std::unordered_map<ShotId, Observation>::const_iterator it2 =
               track.second.begin();
           it2 != track.second.end(); ++it2) {
        const auto& shotID2 = it2->first;
        if (shotID1 == shotID2) {
          continue;
        }
        if (shotID1 > shotID2) {
          continue;
        }
        common_per_pair[std::make_pair(shotID1, shotID2)].push_back(
            std::make_tuple(track.first, it1->second, it2->second));
      }
    }
  }
  return common_per_pair;
}

TracksManager TracksManager::InstanciateFromFile(const std::string& filename) {
  std::ifstream istream(filename);
  if (istream.is_open()) {
    const auto version = GetTracksFileVersion(istream);
    switch (version) {
      case 0:
        return InstanciateFromFileV0(istream);
      case 1:
        return InstanciateFromFileV1(istream);
      default:
        throw std::runtime_error("Unknown tracks manager file version");
    }
  } else {
    throw std::runtime_error("Can't read tracks manager file");
  }
}

void TracksManager::WriteToFile(const std::string& filename) {
  std::ofstream ostream(filename);
  if (ostream.is_open()) {
    ostream << TRACKS_HEADER << "_v" << TRACKS_VERSION << std::endl;
    WriteToFileCurrentVersion(ostream, *this);
  } else {
    throw std::runtime_error("Can't write tracks manager file");
  }
}

std::string TracksManager::TRACKS_HEADER = "OPENSFM_TRACKS_VERSION";
int TracksManager::TRACKS_VERSION = 1;