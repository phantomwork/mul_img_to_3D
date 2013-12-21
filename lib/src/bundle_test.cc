
#include "gflags/gflags.h"
#include "gtest/gtest.h"
#include <glog/logging.h>
#include "bundle.h"


TEST(BALProblem, LoadJson) {
  BALProblem bal_problem;
  bool w = bal_problem.LoadJson("../../labmv/test/tracks.csv",
                                "../../labmv/test/reconstruction.json");
  EXPECT_TRUE(w);
  EXPECT_EQ(bal_problem.num_observations(), 148);

  int outliers = 0;
  for (int i = 0; i < bal_problem.num_observations(); ++i) {
    const double* observation = &bal_problem.observations()[2 * i];
    const double* camera = bal_problem.mutable_camera_for_observation(i);
    const double* point = bal_problem.mutable_point_for_observation(i);

    SnavelyReprojectionError re(observation[0],
                                observation[1]);
    double residuals[2];
    re(camera, point, residuals);
    if (fabs(residuals[0]) > 2.0 || fabs(residuals[1]) > 2.0) {
      outliers++;
    }
  }
  EXPECT_LE(outliers, bal_problem.num_observations() / 2);
}


DEFINE_string(test_tmpdir, "/tmp", "Dir to use for temp files");

int main(int argc, char **argv) {
  testing::InitGoogleTest(&argc, argv);
  google::ParseCommandLineFlags(&argc, &argv, true);
  google::InitGoogleLogging(argv[0]);

  return RUN_ALL_TESTS();
}

