#pragma once
#include <opencv2/core/mat.hpp>
namespace evision {
	/*
	 * 初始化:给出运行模式
	 * 调用set设置必要参数
	 * 调用solve求解
	 * 调用get获取中间结果
	 */
	#define SUCCESS 0
	#define FAILED  -1
	#define ERROR -2

	class kalibra
	{
	public:
		enum Model {
			single,  /* 单目标定 */
			stereo	 /* 双目标定 */
		};
		enum Pattern {
			CHESSBOARD,					/* 以国际象棋棋盘为标定图案 */
			CIRCLES_GRID,				/* 以圆点点阵为标定图案 */
			ASYMMETRIC_CIRCLES_GRID		/* 以   为标定图案 */
		};
		enum {
			DETECTION = 0, 
			CAPTURING = 1, 
			CALIBRATED = 2 
		};

		kalibra(Model solveModel, Pattern pattern);
		int init(const std::vector<std::string>* imagelist,
			const int boardSpecsHorizontal, const int boardSpecsVertical, const float boardMetric, const float aspectRatio, const int flags, const bool debug);
		int init(const std::vector<std::string>* imagelistL, const std::vector<std::string>* imagelistR,
			const int boardSpecsHorizontal, const int boardSpecsVertical, const float boardMetric, const float aspectRatio, const int flags, const bool debug);
		int solve();


		kalibra(std::vector<std::string>* imagelistL, std::vector<std::string>* imagelistR);
		~kalibra();
		void run()override;
		bool SaveCameraParamsToFile();

	private:
		Model solveModel_;
		Pattern boardPattern_;
		int boardSpecsHorizontal_ = 0;
		int boardSpecsVertical_ = 0;
		float boardMetric_ = 0;
		float aspectRatio_ = 0;
		int flags_ = 0;
		bool debug_ = false;

		const std::vector<std::string>* imagelist_;
		std::vector<cv::Mat> undistortedBoards_;
		std::vector<cv::Mat> checkedBoards_;
		cv::Size imageSize_;
		cv::Mat cameraMatrix_;
		cv::Mat distCoeffs_;

		const std::vector<std::string>* imagelistL_;
		const std::vector<std::string>* imagelistR_;
		std::vector<cv::Mat> undistortedBoardsL_;
		std::vector<cv::Mat> undistortedBoardsR_;
		std::vector<cv::Mat> checkedBoardsL_;
		std::vector<cv::Mat> checkedBoardsR_;
		cv::Mat cameraMatrixL_;
		cv::Mat cameraMatrixR_;
		cv::Mat distCoeffsL_;
		cv::Mat distCoeffsR_;
		cv::Mat R, T, E, F, R1, P1, R2, P2, Q;
		cv::Rect roi1, roi2;

		std::string cameraParamsFilename;
		bool ready_to_save = false;

		void initObjectPoints(const cv::Size& boardSize, const float squareSize, const Pattern& patternType, const int length, std::vector<std::vector<cv::Point3f>>& wcsPoints);

		bool KeyPointDetector(const cv::Size& boardSize, const cv::Mat& boardShot, const Pattern pattern, std::vector<cv::Point2f>& pointbuf);

		int Calib1D(const cv::Size boardSize, const float squareSize, const std::vector<std::string>& imageList,
			const float aspectRatio, const Pattern pattern, const int flags, const bool debug,
			cv::Mat& cameraMatrix, cv::Mat& distCoeffs, cv::Size& imageSize, std::vector<cv::Mat>& checkedBoards, std::vector<cv::Mat>& undistortedBoards);

		void DrawMsgOnImage(cv::Mat& viewL, std::string msg);

		int Calib2D(const cv::Size boardSize, const float squareSize, const std::vector<std::string>& imageListL, const std::vector<std::string>& imageListR,
			const float aspectRatio, const Pattern pattern, const int flags, const bool debug, const int maxScale,
			cv::Mat& cameraMatrix_L, cv::Mat& distCoeffs_L, cv::Mat& cameraMatrix_R, cv::Mat& distCoeffs_R,
			cv::Mat& R, cv::Mat& T, cv::Mat& E, cv::Mat& F, cv::Mat& R1, cv::Mat& P1, cv::Mat& R2, cv::Mat& P2, cv::Mat& Q,
			cv::Rect& roi1, cv::Rect& roi2);


		void StereoCalib(const std::vector<std::string>& imagelist,
			cv::Size boardSize,
			float squareSize,
			cv::Mat& cameraMatrix_L, cv::Mat& distCoeffs_L,
			cv::Mat& cameraMatrix_R, cv::Mat& distCoeffs_R,
			cv::Mat& R, cv::Mat& T, cv::Mat& E, cv::Mat& F, cv::Mat& R1, cv::Mat& P1, cv::Mat& R2, cv::Mat& P2, cv::Mat& Q,
			cv::Rect& roi1, cv::Rect& roi2,
			int flags,
			bool displayCorners = false,
			bool useCalibrated = true,
			bool showRectified = true);





		double computeReprojectionErrors(
			const std::vector<std::vector<cv::Point3f> >& objectPoints,
			const std::vector<std::vector<cv::Point2f> >& imagePoints,
			const std::vector<cv::Mat>& rvecs, const std::vector<cv::Mat>& tvecs,
			const cv::Mat& cameraMatrix, const cv::Mat& distCoeffs,
			std::vector<float>& perViewErrors);

		bool calibrate_1D_core(const std::vector<std::vector< cv::Point2f> >& imagePoints,
			cv::Size imageSize, cv::Size boardSize, float squareSize,
			float aspectRatio, int flags, cv::Mat& cameraMatrix,
			cv::Mat& distCoeffs);

		void StereoCalib(const std::vector<std::string>& imagelist,
			cv::Size boardSize,
			float squareSize,
			cv::Mat& cameraMatrix_L, cv::Mat& distCoeffs_L,
			cv::Mat& cameraMatrix_R, cv::Mat& distCoeffs_R,
			cv::Mat& R, cv::Mat& T, cv::Mat& E, cv::Mat& F, cv::Mat& R1, cv::Mat& P1, cv::Mat& R2, cv::Mat& P2, cv::Mat& Q,
			cv::Rect& roi1, cv::Rect& roi2,
			int flags,
			bool displayCorners = false,
			bool useCalibrated = true,
			bool showRectified = true);
		int getCalibrate1D_flags();
		int getCalibrate2D_flags();

	};
}
