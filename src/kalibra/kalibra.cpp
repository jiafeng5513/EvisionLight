#include "kalibra.h"
#include <opencv2/opencv.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <iostream>


namespace evision {


	kalibra::kalibra(std::vector<std::string>* imagelistL, std::vector<std::string>* imagelistR, QObject* parent)
	{
		m_entity = CalibrateParamEntity::getInstance();
		this->imagelistL = imagelistL;
		this->imagelistR = imagelistR;

		QFileInfo* _fileInfo = new QFileInfo(QString::fromStdString(imagelistL->at(0)));
		this->cameraParamsFilename = _fileInfo->absolutePath().toStdString().append("/cameraParams.yml");
	}

	/// <summary>
	/// ��ʼ�� 1
	/// </summary>
	/// <param name="imagelist">�궨ͼƬ�ļ����б�</param>
	/// <param name="boardSpecsHorizontal">�궨����:ˮƽ</param>
	/// <param name="boardSpecsVertical">�궨����:��ֱ</param>
	/// <param name="boardMetric">�궨�����ֵ</param>
	/// <param name="aspectRatio">����ϵ��</param>
	/// <param name="flags">flags</param>
	/// <param name="showUndistorted">�Ƿ�Ա궨ͼƬ���н���</param>
	/// <returns></returns>
	int kalibra::init(const std::vector<std::string>* imagelist, 
		const int boardSpecsHorizontal, const int boardSpecsVertical, const float boardMetric, const float aspectRatio, const int flags, const bool debug)
	{
		/// TODO:���в�������У��
		this->imagelist_ = imagelist;
		this->boardSpecsHorizontal_ = boardSpecsHorizontal;
		this->boardSpecsVertical_ = boardSpecsVertical;
		this->boardMetric_ = boardMetric;
		this->aspectRatio_ = aspectRatio;
		this->flags_ = flags;
		this->debug_ = debug;
		return 0;
	}
	/// <summary>
	/// ��ʼ�� 2
	/// </summary>
	/// <param name="imagelistL"></param>
	/// <param name="imagelistR"></param>
	/// <param name="boardSpecsHorizontal"></param>
	/// <param name="boardSpecsVertical"></param>
	/// <param name="boardMetric"></param>
	/// <param name="aspectRatio"></param>
	/// <param name="flags"></param>
	/// <param name="showUndistorted"></param>
	/// <returns></returns>
	int kalibra::init(const std::vector<std::string>* imagelistL, const std::vector<std::string>* imagelistR, 
		const int boardSpecsHorizontal, const int boardSpecsVertical, const float boardMetric, const float aspectRatio, const int flags, const bool debug)
	{
		/// TODO:���в�������У��
		this->imagelistL_ = imagelistL;
		this->imagelistR_ = imagelistR;
		this->boardSpecsHorizontal_ = boardSpecsHorizontal;
		this->boardSpecsVertical_ = boardSpecsVertical;
		this->boardMetric_ = boardMetric;
		this->aspectRatio_ = aspectRatio;
		this->flags_ = flags;
		this->debug_ = debug;
		return 0;
	}
	/// <summary>
	/// �����
	/// </summary>
	/// <returns>�ɹ�:����0,ʧ�ܻ��������:��������</returns>
	int kalibra::solve()
	{
		cv::Size boardSize(this->boardSpecsHorizontal_, this->boardSpecsVertical_);

		if (solveModel_ == single)
		{
			Calib1D(boardSize, boardMetric_, *imagelist_,aspectRatio_, boardPattern_, flags_, debug_,
				cameraMatrix_, distCoeffs_, imageSize_, checkedBoards_, undistortedBoards_);
		}
		else
		{
			int flags_2D = getCalibrate2D_flags();
			std::vector<std::string>* imagelist_double = new std::vector<std::string>();
			for (int i = 0; i < imagelistL_->size(); ++i)
			{
				imagelist_double->push_back(imagelistL_->at(i));
				imagelist_double->push_back(imagelistR_->at(i));
			}

			Calib1D(boardSize, boardMetric_, *imagelist_, aspectRatio_, boardPattern_, flags_, debug_,
				cameraMatrix_L, distCoeffs_L, imageSize_, checkedBoards_, undistortedBoards_);
			Calib1D(boardSize, boardMetric_, *imagelist_, aspectRatio_, boardPattern_, flags_, debug_,
				cameraMatrix_R, distCoeffs_R, imageSize_, checkedBoards_, undistortedBoards_);

			StereoCalib(*imagelist_double, boardSize, boardMetric_, cameraMatrix_L, distCoeffs_L, cameraMatrix_R, distCoeffs_R,
				R, T, E, F, R1, P1, R2, P2, Q, roi1, roi2, flags_, false, true, debug_);

		}
		return 0;
	}

	kalibra::~kalibra()
	{

	}
	/*
	 * �̷߳���
	 */
	void kalibra::run()
	{
		ready_to_save = false;
		if (imagelistL->size() != imagelistR->size())//ͼƬ���ɶ�
		{
			emit openMessageBox(QStringLiteral("����"), QStringLiteral("ͼƬ���ɶ�!"));
			return;
		}

		try
		{
			cv::Size boardSize(m_entity->getBoardWidth(), m_entity->getBoardHeight());
			float squareSize = m_entity->getSquareSize();
			int flags_1D = getCalibrate1D_flags();
			int flags_2D = getCalibrate2D_flags();


			bool showRectified = true;
			float  aspectRatio = 1;
			Pattern pattern = CHESSBOARD;
			bool showUndistorted = true;


			std::vector<std::string>* imagelist_double = new std::vector<std::string>();
			for (int i = 0; i < imagelistL->size(); ++i)
			{
				imagelist_double->push_back(imagelistL->at(i));
				imagelist_double->push_back(imagelistR->at(i));
			}

			std::cout << "�궨�����" << std::endl;
			Calib1D(boardSize, squareSize, *imagelistL, cameraMatrix_L, distCoeffs_L, aspectRatio, pattern, flags_1D, showUndistorted);
			std::cout << "�궨�����" << std::endl;
			Calib1D(boardSize, squareSize, *imagelistR, cameraMatrix_R, distCoeffs_R, aspectRatio, pattern, flags_1D, showUndistorted);
			std::cout << "�궨˫Ŀϵͳ" << std::endl;
			StereoCalib(*imagelist_double, boardSize, squareSize, cameraMatrix_L, distCoeffs_L, cameraMatrix_R, distCoeffs_R,
				R, T, E, F, R1, P1, R2, P2, Q, roi1, roi2, flags_2D, false, true, showRectified);
			ready_to_save = true;
		}
		catch (std::exception e)
		{
			std::cout << "�궨�������ش���!" << e.what() << std::endl;

		}
	}
	/*
	 * �ѱ궨�����Ĳ������浽�ļ�
	 */
	bool kalibra::SaveCameraParamsToFile()
	{
		if (ready_to_save == false)
		{
			std::cout << "û��׼���ñ������!" << std::endl;
			return false;
		}
		else
		{
			// �������
			bool flag = EvisionUtils::write_AllCameraParams(cameraParamsFilename, cameraMatrix_L, distCoeffs_L,
				cameraMatrix_R, distCoeffs_R, R, T, imageSize, R1, P1, R2, P2, Q, roi1, roi2);
			std::cout << "�����Ѿ����浽:" << cameraParamsFilename << std::endl;
			if (!flag)
			{
				emit openMessageBox(QStringLiteral("�ļ����ʴ���"), QStringLiteral("�޷�д��:cameraParams.yml"));
				return false;
			}
		}
		return true;
	}

	/*
	 * ������ͶӰ���
	 */
	double kalibra::computeReprojectionErrors(const std::vector<std::vector<cv::Point3f>>& objectPoints,
		const std::vector<std::vector<cv::Point2f>>& imagePoints, const std::vector<cv::Mat>& rvecs,
		const std::vector<cv::Mat>& tvecs, const cv::Mat& cameraMatrix, const cv::Mat& distCoeffs,
		std::vector<float>& perViewErrors)
	{
		std::vector<cv::Point2f> imagePoints2;
		int i, totalPoints = 0;
		double totalErr = 0, err;
		perViewErrors.resize(objectPoints.size());

		for (i = 0; i < (int)objectPoints.size(); i++)
		{
			projectPoints(cv::Mat(objectPoints[i]), rvecs[i], tvecs[i],
				cameraMatrix, distCoeffs, imagePoints2);
			err = norm(cv::Mat(imagePoints[i]), cv::Mat(imagePoints2), cv::NORM_L2);
			int n = (int)objectPoints[i].size();
			perViewErrors[i] = (float)std::sqrt(err * err / n);
			totalErr += err * err;
			totalPoints += n;
		}

		return std::sqrt(totalErr / totalPoints);
	}

	/// @brief ��ʼ���궨������
	/// @param boardSize		[i]		�궨����������
	/// @param squareSize		[i]		�궨�����������
	/// @param patternType		[i]		�궨������
	/// @param length			[i]		�궨ͼƬ����
	/// @param wcsPoints		[o]		����궨������������
	void kalibra::initObjectPoints(const cv::Size& boardSize, const float squareSize, const Pattern& patternType, const int length, 
		std::vector<std::vector<cv::Point3f>>& wcsPoints)
	{

		int h = boardSize.height;
		int w = boardSize.width;
		wcsPoints[0].resize(h * w);
		wcsPoints.resize(length, wcsPoints[0]);
		switch (patternType)
		{
		case CHESSBOARD:
		case CIRCLES_GRID:
			for (int i = 0; i < h; i++) {
				int s = i * h;
				for (int j = 0; j < w; j++) {
					wcsPoints[0][s + j] = cv::Point3f(float(j * squareSize), float(i * squareSize), 0);
				}
			}
			break;
		case ASYMMETRIC_CIRCLES_GRID:
			for (int i = 0; i < h; i++) {
				int s = i * h;
				for (int j = 0; j < w; j++) {
					wcsPoints[0][s + j] = cv::Point3f(float((2 * j + i % 2) * squareSize),float(i * squareSize), 0);
				}
			}
			break;
		}
		std::fill(wcsPoints.begin()+1, wcsPoints.end(), wcsPoints[0]);
	}


	/// @brief ���궨�ؼ���
	/// @param boardSize		[i]			�궨����(�����������������)
	/// @param boardShot		[i]			�궨����Ƭ
	/// @param pattern			[i]			�궨������
	/// @param pointbuf			[o]			������
	/// @return 
	bool kalibra::KeyPointDetector(const cv::Size& boardSize, const cv::Mat& boardShot, const Pattern pattern, std::vector<cv::Point2f>& pointbuf) 
	{
		bool found = false;
		switch (pattern)
		{
		case CHESSBOARD:
			found = findChessboardCorners(boardShot, boardSize, pointbuf,
				cv::CALIB_CB_ADAPTIVE_THRESH | cv::CALIB_CB_FAST_CHECK | cv::CALIB_CB_NORMALIZE_IMAGE);
			if (found)
			{
				cv::Mat viewGray;
				cvtColor(boardShot, viewGray, cv::COLOR_BGR2GRAY);
				cv::cornerSubPix(viewGray, pointbuf, cv::Size(11, 11), cv::Size(-1, -1),
					cv::TermCriteria(cv::TermCriteria::EPS + cv::TermCriteria::COUNT, 30, 0.1));
			}
			break;
		case CIRCLES_GRID:
			found = findCirclesGrid(boardShot, boardSize, pointbuf);
			break;
		case ASYMMETRIC_CIRCLES_GRID:
			found = findCirclesGrid(boardShot, boardSize, pointbuf, cv::CALIB_CB_ASYMMETRIC_GRID);
			break;
		}
		return found;
	}
	/// @brief ��Ŀ�궨
	/// @param boardSize		 [i]		�궨����(�����������������)
	/// @param squareSize		 [i]		�궨�����(��������ʵ����)
	/// @param imageList		 [i]		�궨ͼƬ���ļ����б�
	/// @param aspectRatio		 [i]		�ݺ��,ֻ�е�flag��ָ��CALIB_FIX_ASPECT_RATIOʱ��������
	/// @param pattern			 [i]		�궨��ģʽ:CHESSBOARD������,CIRCLES_GRIDԲ������,ASYMMETRIC_CIRCLES_GRID�ǶԳ�Բ������
	/// @param flags			 [i]		����ѡ��
	/// @param debug			 [i]		����debug�ᱣ������������м���,�����ñ궨����Ա궨ͼƬ���н���
	/// @param cameraMatrix		 [o]		�ڲξ���
	/// @param distCoeffs		 [o]		�������
	/// @param imageSize		 [o]		�궨ͼ��ķֱ���
	/// @param checkedBoards     [o]		�궨����debug���
	/// @param undistortedBoards [o]		�궨ͼƬ��������debug���
	/// @return
	int kalibra::Calib1D(const cv::Size boardSize, const float squareSize, const std::vector<std::string>& imageList,
		const float aspectRatio, const Pattern pattern, const int flags, const bool debug, 
		cv::Mat& cameraMatrix, cv::Mat& distCoeffs, cv::Size &imageSize, std::vector<cv::Mat> &checkedBoards, std::vector<cv::Mat> &undistortedBoards)
	{
		std::vector<std::vector<cv::Point2f> > imagePoints;
		for each (std::string imageFileName in imageList)
		{
			cv::Mat view = cv::imread(imageFileName);
			if (view.empty()) {
				continue;
			}
			imageSize = view.size();
			std::vector<cv::Point2f> pointbuf;
			
			if (KeyPointDetector(boardSize, view, pattern, pointbuf))
			{
				imagePoints.push_back(pointbuf);
				if (debug) {
					undistortedBoards_.push_back(view);

					drawChessboardCorners(view, boardSize, cv::Mat(pointbuf),true);

					std::string msg = "100/100";
					int baseLine = 0;
					cv::Size textSize = cv::getTextSize(msg, 1, 1, 1, &baseLine);
					cv::Point textOrigin(view.cols - 2 * textSize.width - 10, view.rows - 2 * baseLine - 10);
					msg = cv::format("%d/%d", imagePoints.size(), imageList.size());
					putText(view, msg, textOrigin, 1, 1, cv::Scalar(0, 0, 255));
					checkedBoards.push_back(view);
				}
			}

		}

		std::vector<std::vector<cv::Point3f> > wcsPoints;
		initObjectPoints(boardSize, squareSize, pattern, imagePoints.size(), wcsPoints);

		cameraMatrix = cv::Mat::eye(3, 3, CV_64F);
		if (flags & cv::CALIB_FIX_ASPECT_RATIO)
			cameraMatrix.at<double>(0, 0) = aspectRatio;
        distCoeffs = cv::Mat::zeros(8, 1, CV_64F);
		std::vector<cv::Mat> rvecs, tvecs;
		double rms = cv::calibrateCamera(wcsPoints, imagePoints, imageSize, cameraMatrix, distCoeffs, rvecs, tvecs, flags);// cv::CALIB_FIX_K3 |

		printf("RMS error reported by calibrateCamera: %g\n", rms);

		bool ok = cv::checkRange(cameraMatrix) && cv::checkRange(distCoeffs);

		std::vector<float> reprojErrs;
		double totalAvgErr = computeReprojectionErrors(wcsPoints, imagePoints, rvecs, tvecs, cameraMatrix, distCoeffs, reprojErrs);

		printf("%s. avg reprojection error = %.2f\n", ok ? "Calibration succeeded" : "Calibration failed", totalAvgErr);

		if (debug)
		{
			cv::Mat map1, map2;
			cv::initUndistortRectifyMap(cameraMatrix, distCoeffs, cv::Mat(),
				getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, imageSize, 1, imageSize, 0),
				imageSize, CV_16SC2, map1, map2);

			for (size_t i = 0; i < undistortedBoards.size(); i++)
			{
				cv::Mat origin = undistortedBoards[i].clone();
				remap(origin, undistortedBoards[i], map1, map2, cv::INTER_LINEAR);
			}
		}
		return 0;
	}


	void kalibra::DrawMsgOnImage(cv::Mat& viewL, std::string msg)
	{
		cv::Point textOrigin(0, 0);
		putText(viewL, cv::format("%s", msg), textOrigin, 1, 1, cv::Scalar(0, 0, 255));
	}

	int kalibra::Calib2D(const cv::Size boardSize, const float squareSize, const std::vector<std::string>& imageListL, const std::vector<std::string>& imageListR,
		const float aspectRatio, const Pattern pattern, const int flags, const bool debug, const int maxScale,
		cv::Mat& cameraMatrix_L, cv::Mat& distCoeffs_L,cv::Mat& cameraMatrix_R, cv::Mat& distCoeffs_R,
		cv::Mat& R, cv::Mat& T, cv::Mat& E, cv::Mat& F, cv::Mat& R1, cv::Mat& P1, cv::Mat& R2, cv::Mat& P2, cv::Mat& Q, cv::Rect& roi1, cv::Rect& roi2) 
	{
		if (imageListL.size() != imageListR.size())
		{
			std::cout << "Error: the image list contains odd (non-even) number of elements\n";
			return -1;
		}
		size_t imageNum = imageListL.size();
		std::vector<std::vector<cv::Point2f> > imagePointsL;
		std::vector<std::vector<cv::Point2f> > imagePointsR;

		cv::Size imageSize;
		int checkedImageNum = 0;
		for (size_t i = 0; i < imageNum; i++)
		{
			cv::Mat viewL = cv::imread(imageListL[i]);
			cv::Mat viewR = cv::imread(imageListR[i]);
			// ���ǵ�Ĭ�������ͼƬ,imageListL[i]��imageListR[i]��ͬʱ�����,��Ϊ�������ܱ�֤������̬�Լ������
			// ���,ֻ��˫ĿͼƬ��ͬʱ��,��size��ͬʱ���б�Ҫ��������
			if ((viewL.empty()|| viewR.empty()) || (viewL.size()!= viewR.size())) {
				continue;
			}
			if (imageSize.empty()) {
				imageSize = viewL.size();
			}
			else
			{
				if ((imageSize != viewL.size()) || (imageSize != viewR.size()))
				{
					continue;
				}
			}
			std::vector<cv::Point2f> pointbufL;
			std::vector<cv::Point2f> pointbufR;

			if (KeyPointDetector(boardSize, viewL, pattern, pointbufL) && KeyPointDetector(boardSize, viewR, pattern, pointbufR))
			{
				imagePointsL.push_back(pointbufL);
				imagePointsR.push_back(pointbufR);
				checkedImageNum++;
				if (debug) {
					undistortedBoardsL_.push_back(viewL); // ������ԭͼ
					undistortedBoardsR_.push_back(viewR); // ������ԭͼ

					drawChessboardCorners(viewL, boardSize, cv::Mat(pointbufL), true);
					drawChessboardCorners(viewL, boardSize, cv::Mat(pointbufL), true);

					DrawMsgOnImage(viewL, imageListL[i]);
					DrawMsgOnImage(viewR, imageListR[i]);

					checkedBoardsL_.push_back(viewL);
					checkedBoardsR_.push_back(viewR);
				}
			}
		}

		std::vector<std::vector<cv::Point3f> > wcsPoints;
		initObjectPoints(boardSize, squareSize, pattern, checkedImageNum, wcsPoints);

		cameraMatrixL_ = cv::Mat::eye(3, 3, CV_64F);
		cameraMatrixR_ = cv::Mat::eye(3, 3, CV_64F);
		if (flags & cv::CALIB_FIX_ASPECT_RATIO) {
			cameraMatrixL_.at<double>(0, 0) = aspectRatio;
			cameraMatrixR_.at<double>(0, 0) = aspectRatio;
		}
		
		distCoeffsL_ = cv::Mat::zeros(8, 1, CV_64F);
		distCoeffsR_ = cv::Mat::zeros(8, 1, CV_64F);

		std::vector<cv::Mat> rvecs, tvecs;

		double rmsL = cv::calibrateCamera(wcsPoints, imagePointsL, imageSize, cameraMatrixL_, distCoeffsL_, rvecs, tvecs, flags);
		double rmsR = cv::calibrateCamera(wcsPoints, imagePointsR, imageSize, cameraMatrixR_, distCoeffsR_, rvecs, tvecs, flags);

		double rms = stereoCalibrate(wcsPoints, imagePointsL, imagePointsR, cameraMatrixL_, distCoeffsL_,cameraMatrixR_, distCoeffsR_,
			imageSize, R, T, E, F,flags,cv::TermCriteria(cv::TermCriteria::COUNT + cv::TermCriteria::EPS, 100, 1e-5));

		bool ok = cv::checkRange(cameraMatrixL_) && cv::checkRange(distCoeffsL_);
		ok = ok && cv::checkRange(cameraMatrixR_) && cv::checkRange(distCoeffsR_);
		ok = ok && cv::checkRange(R) && cv::checkRange(T) && cv::checkRange(E) && cv::checkRange(F);

	}
	/*
	 * ˫Ŀ�궨
	 */
	void kalibra::StereoCalib(
		const std::vector<std::string>& imagelist,
		cv::Size boardSize,
		float squareSize,
		cv::Mat& cameraMatrix_L, cv::Mat& distCoeffs_L,
		cv::Mat& cameraMatrix_R, cv::Mat& distCoeffs_R,
		cv::Mat& R, cv::Mat& T, cv::Mat& E, cv::Mat& F, cv::Mat& R1, cv::Mat& P1, cv::Mat& R2, cv::Mat& P2, cv::Mat& Q,
		cv::Rect& roi1, cv::Rect& roi2,
		int flags,
		bool displayCorners, bool useCalibrated, bool showRectified)
	{
		try
		{
			if (imagelist.size() % 2 != 0)
			{
				std::cout << "Error: the image list contains odd (non-even) number of elements\n";
				return;
			}

			const int maxScale = 2;
			// ARRAY AND VECTOR STORAGE:

			std::vector<std::vector<cv::Point2f> > imagePoints[2];
			std::vector<std::vector<cv::Point3f> > objectPoints;
			cv::Size imageSize;

			int i, j, k, nimages = (int)imagelist.size() / 2;

			imagePoints[0].resize(nimages);
			imagePoints[1].resize(nimages);
			std::vector<std::string> goodImageList;

			for (i = j = 0; i < nimages; i++)
			{
				for (k = 0; k < 2; k++)
				{
					const std::string& filename = imagelist[i * 2 + k];
					cv::Mat img = cv::imread(filename, 0);
					if (img.empty())
						break;
					if (imageSize == cv::Size())
						imageSize = img.size();
					else if (img.size() != imageSize)
					{
						std::cout << "The image " << filename << " has the size different from the first image size. Skipping the pair\n";
						break;
					}
					bool found = false;
					std::vector<cv::Point2f>& corners = imagePoints[k][j];
					for (int scale = 1; scale <= maxScale; scale++)
					{
						cv::Mat timg;
						if (scale == 1)
							timg = img;
						else
							resize(img, timg, cv::Size(), scale, scale, cv::INTER_LINEAR_EXACT);
						found = findChessboardCorners(timg, boardSize, corners, cv::CALIB_CB_ADAPTIVE_THRESH | cv::CALIB_CB_NORMALIZE_IMAGE);
						if (found)
						{
							if (scale > 1)
							{
								cv::Mat cornersMat(corners);
								cornersMat *= 1. / scale;
							}
							break;
						}
					}
					if (displayCorners)
					{
						std::cout << filename << std::endl;
						cv::Mat cimg, cimg1;
						cvtColor(img, cimg, cv::COLOR_GRAY2BGR);
						drawChessboardCorners(cimg, boardSize, corners, found);
						double sf = 640. / MAX(img.rows, img.cols);
						resize(cimg, cimg1, cv::Size(), sf, sf, cv::INTER_LINEAR_EXACT);
						cv::imshow("corners", cimg1);
						char c = (char)cv::waitKey(500);
						if (c == 27 || c == 'q' || c == 'Q') //Allow ESC to quit
							exit(-1);
					}
					else
						putchar('.');
					if (!found)
						break;
					cv::cornerSubPix(img, corners, cv::Size(11, 11), cv::Size(-1, -1),
						cv::TermCriteria(cv::TermCriteria::COUNT + cv::TermCriteria::EPS,
							30, 0.01));
				}
				if (k == 2)
				{
					goodImageList.push_back(imagelist[i * 2]);
					goodImageList.push_back(imagelist[i * 2 + 1]);
					j++;
				}
			}
			std::cout << j << " pairs have been successfully detected.\n";
			nimages = j;
			if (nimages < 2)
			{
				std::cout << "Error: too little pairs to run the calibration\n";
				return;
			}

			imagePoints[0].resize(nimages);
			imagePoints[1].resize(nimages);
			objectPoints.resize(nimages);

			for (i = 0; i < nimages; i++)
			{
				for (j = 0; j < boardSize.height; j++)
					for (k = 0; k < boardSize.width; k++)
						objectPoints[i].push_back(cv::Point3f(k * squareSize, j * squareSize, 0));
			}

			std::cout << "Running stereo calibration ...\n";

			//Mat cameraMatrix[2], distCoeffs[2];
			//cameraMatrix[0] = initCameraMatrix2D(objectPoints, imagePoints[0], imageSize, 0);
			//cameraMatrix[1] = initCameraMatrix2D(objectPoints, imagePoints[1], imageSize, 0);

			/*
			 *CALIB_FIX_ASPECT_RATIO
			 *CALIB_ZERO_TANGENT_DIST
			 *CALIB_USE_INTRINSIC_GUESS
			 *CALIB_SAME_FOCAL_LENGTH
			 *CALIB_RATIONAL_MODEL
			 *CALIB_FIX_INTRINSIC
			 *CALIB_FIX_K3
			 *CALIB_FIX_K4
			 *CALIB_FIX_K5
			 */


			double rms = stereoCalibrate(objectPoints, imagePoints[0], imagePoints[1],
				cameraMatrix_L, distCoeffs_L,
				cameraMatrix_R, distCoeffs_R,
				imageSize, R, T, E, F,
				flags,
				cv::TermCriteria(cv::TermCriteria::COUNT + cv::TermCriteria::EPS, 100, 1e-5));
			std::cout << "done with RMS error=" << rms << std::endl;

			// CALIBRATION QUALITY CHECK
			// because the output fundamental matrix implicitly
			// includes all the output information,
			// we can check the quality of calibration using the
			// epipolar geometry constraint: m2^t*F*m1=0
			double err = 0;
			int npoints = 0;
			std::vector<cv::Vec3f> lines[2];
			for (i = 0; i < nimages; i++)
			{
				int npt = (int)imagePoints[0][i].size();
				cv::Mat imgpt[2];

				imgpt[0] = cv::Mat(imagePoints[0][i]);
				undistortPoints(imgpt[0], imgpt[0], cameraMatrix_L, distCoeffs_L, cv::Mat(), cameraMatrix_L);
				computeCorrespondEpilines(imgpt[0], 0 + 1, F, lines[0]);

				imgpt[1] = cv::Mat(imagePoints[1][i]);
				undistortPoints(imgpt[1], imgpt[1], cameraMatrix_R, distCoeffs_R, cv::Mat(), cameraMatrix_R);
				computeCorrespondEpilines(imgpt[1], 1 + 1, F, lines[1]);

				for (j = 0; j < npt; j++)
				{
					double errij = fabs(imagePoints[0][i][j].x * lines[1][j][0] +
						imagePoints[0][i][j].y * lines[1][j][1] + lines[1][j][2]) +
						fabs(imagePoints[1][i][j].x * lines[0][j][0] +
							imagePoints[1][i][j].y * lines[0][j][1] + lines[0][j][2]);
					err += errij;
				}
				npoints += npt;
			}
			std::cout << "average epipolar err = " << err / npoints << std::endl;

			// save intrinsic parameters
			//cv::FileStorage fs("intrinsics.yml", cv::FileStorage::WRITE);
			//if (fs.isOpened())
			//{
			//	fs << "M1" << cameraMatrix_L << "D1" << distCoeffs_L <<
			//		"M2" << cameraMatrix_R << "D2" << distCoeffs_R;
			//	fs.release();
			//}
			//else
			//	std::cout << "Error: can not save the intrinsic parameters\n";

			cv::Rect validRoi[2];
			cv::Size tempsize(0, 0);
			cv::stereoRectify(cameraMatrix_L, distCoeffs_L,
				cameraMatrix_R, distCoeffs_R,
				imageSize, R, T, R1, R2, P1, P2, Q,
				0, 1, tempsize, &validRoi[0], &validRoi[1]);

			//fs.open("extrinsics.yml", cv::FileStorage::WRITE);
			//if (fs.isOpened())
			//{
			//	fs << "R" << R << "T" << T << "R1" << R1 << "R2" << R2 << "P1" << P1 << "P2" << P2 << "Q" << Q;
			//	fs.release();
			//}
			//else
			//	std::cout << "Error: can not save the extrinsic parameters\n";

			// OpenCV can handle left-right
			// or up-down camera arrangements
			bool isVerticalStereo = fabs(P2.at<double>(1, 3)) > fabs(P2.at<double>(0, 3));

			// COMPUTE AND DISPLAY RECTIFICATION
			if (!showRectified)
				return;

			cv::Mat rmap[2][2];
			// IF BY CALIBRATED (BOUGUET'S METHOD)
			if (useCalibrated)
			{
				// we already computed everything
			}
			// OR ELSE HARTLEY'S METHOD
			else
				// use intrinsic parameters of each camera, but
				// compute the rectification transformation directly
				// from the fundamental matrix
			{
				std::vector<cv::Point2f> allimgpt[2];
				for (k = 0; k < 2; k++)
				{
					for (i = 0; i < nimages; i++)
						std::copy(imagePoints[k][i].begin(), imagePoints[k][i].end(), back_inserter(allimgpt[k]));
				}
				F = findFundamentalMat(cv::Mat(allimgpt[0]), cv::Mat(allimgpt[1]), cv::FM_8POINT, 0, 0);
				cv::Mat H1, H2;
				stereoRectifyUncalibrated(cv::Mat(allimgpt[0]), cv::Mat(allimgpt[1]), F, imageSize, H1, H2, 3);

				R1 = cameraMatrix_L.inv() * H1 * cameraMatrix_L;
				R2 = cameraMatrix_R.inv() * H2 * cameraMatrix_R;
				P1 = cameraMatrix_L;
				P2 = cameraMatrix_R;
			}

			//Precompute maps for cv::remap()
			cv::initUndistortRectifyMap(cameraMatrix_L, distCoeffs_L, R1, P1, imageSize, CV_16SC2, rmap[0][0], rmap[0][1]);
			cv::initUndistortRectifyMap(cameraMatrix_R, distCoeffs_R, R2, P2, imageSize, CV_16SC2, rmap[1][0], rmap[1][1]);

			cv::Mat canvas;
			double sf;
			int w, h;
			if (!isVerticalStereo)
			{
				sf = 600. / MAX(imageSize.width, imageSize.height);
				w = cvRound(imageSize.width * sf);
				h = cvRound(imageSize.height * sf);
				canvas.create(h, w * 2, CV_8UC3);
			}
			else
			{
				sf = 300. / MAX(imageSize.width, imageSize.height);
				w = cvRound(imageSize.width * sf);
				h = cvRound(imageSize.height * sf);
				canvas.create(h * 2, w, CV_8UC3);
			}

			for (i = 0; i < nimages; i++)
			{
				for (k = 0; k < 2; k++)
				{
					cv::Mat img = cv::imread(goodImageList[i * 2 + k], 0), rimg, cimg;
					remap(img, rimg, rmap[k][0], rmap[k][1], cv::INTER_LINEAR);
					cvtColor(rimg, cimg, cv::COLOR_GRAY2BGR);
					cv::Mat canvasPart = !isVerticalStereo ? canvas(cv::Rect(w * k, 0, w, h)) : canvas(cv::Rect(0, h * k, w, h));
					resize(cimg, canvasPart, canvasPart.size(), 0, 0, cv::INTER_AREA);
					if (useCalibrated)
					{
						cv::Rect vroi(cvRound(validRoi[k].x * sf), cvRound(validRoi[k].y * sf),
							cvRound(validRoi[k].width * sf), cvRound(validRoi[k].height * sf));
						rectangle(canvasPart, vroi, cv::Scalar(0, 0, 255), 3, 8);
					}
				}

				if (!isVerticalStereo)
					for (j = 0; j < canvas.rows; j += 16)
						line(canvas, cv::Point(0, j), cv::Point(canvas.cols, j), cv::Scalar(0, 255, 0), 1, 8);
				else
					for (j = 0; j < canvas.cols; j += 16)
						line(canvas, cv::Point(j, 0), cv::Point(j, canvas.rows), cv::Scalar(0, 255, 0), 1, 8);
				//cv::imshow("rectified", canvas);
				m_entity->insertItem(canvas);
				//char c = (char)cv::waitKey();
				//if (c == 27 || c == 'q' || c == 'Q')
					//break;
			}
			roi1 = validRoi[0];
			roi2 = validRoi[1];
		}
		catch (std::exception e)
		{
			std::cout << "StereoCalib�������ش���" << e.what() << std::endl;
		}
	}
	/*
	 * ��ȡ��Ŀ�궨��flags
	 */
	int kalibra::getCalibrate1D_flags()
	{
		int flag = 0;
		flag |= cv::CALIB_FIX_PRINCIPAL_POINT;
		flag |= cv::CALIB_FIX_ASPECT_RATIO;
		flag |= cv::CALIB_ZERO_TANGENT_DIST;
		flag |= cv::CALIB_FIX_K1;
		flag |= cv::CALIB_FIX_K2;
		flag |= cv::CALIB_FIX_K3;
		flag |= cv::CALIB_FIX_K4;
		flag |= cv::CALIB_FIX_K5;
		flag |= cv::CALIB_FIX_K6;
		flag |= cv::CALIB_RATIONAL_MODEL;
		flag |= cv::CALIB_THIN_PRISM_MODEL;
		flag |= cv::CALIB_FIX_S1_S2_S3_S4;
		flag |= cv::CALIB_TILTED_MODEL;
		flag |= cv::CALIB_FIX_TAUX_TAUY;
		return flag;
	}
	/*
	 * ��ȡ����궨��flags
	 */
	int kalibra::getCalibrate2D_flags()
	{
		int flag = 0 | cv::CALIB_FIX_INTRINSIC;
		flag |= cv::CALIB_SAME_FOCAL_LENGTH;
		flag |= cv::CALIB_FIX_K1;
		flag |= cv::CALIB_FIX_K2;
		flag |= cv::CALIB_FIX_K3;
		flag |= cv::CALIB_FIX_K4;
		flag |= cv::CALIB_FIX_K5;
		flag |= cv::CALIB_FIX_K6;
		flag |= cv::CALIB_RATIONAL_MODEL;
		flag |= cv::CALIB_THIN_PRISM_MODEL;
		flag |= cv::CALIB_FIX_S1_S2_S3_S4;
		flag |= cv::CALIB_TILTED_MODEL;
		flag |= cv::CALIB_FIX_TAUX_TAUY;
		return flag;
	}
}