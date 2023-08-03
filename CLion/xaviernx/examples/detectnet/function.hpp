#include "gstCamera.h"
#include "glDisplay.h"
#include "opencv2/opencv.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/core.hpp"
#include "detectNet.h"
#include "commandLine.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <array>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <signal.h>
#include <gflags/gflags.h>
#include <functional>
#include <iostream>
#include <fstream>
#include <random>
#include <memory>
#include <chrono>
#include <vector>
#include <string>
#include <algorithm>
#include <iterator>
// UART

#include <fcntl.h> // Contains file controls like O_RDWR
#include <errno.h> // Error integer and strerror() function
#include <termios.h> // Contains POSIX terminal control definitions
#include <unistd.h> // write(), read(), close()

const cv::Scalar SCALAR_BLACK = cv::Scalar(0.0, 0.0, 0.0);
const cv::Scalar SCALAR_WHITE = cv::Scalar(255.0, 255.0, 255.0);
const cv::Scalar SCALAR_YELLOW = cv::Scalar(0.0, 255.0, 255.0);
const cv::Scalar SCALAR_GREEN = cv::Scalar(0.0, 200.0, 0.0);
const cv::Scalar SCALAR_RED = cv::Scalar(0.0, 0.0, 255.0);
const cv::Scalar SCALAR_BLUE = cv::Scalar(255.0, 0.0, 0.0);

using namespace cv;
using namespace std;


class CSharedMemroy {

private :

    int m_shmid;
    key_t m_key;
    char *m_shared_memory[8];


public :

    void setShmId(int key);

    int getShmId();

    void setKey(key_t key);

    void setupSharedMemory(int size);

    void attachSharedMemory();

    void copyToSharedMemory(bool det_code);
//   void close();
};






///Time


std::string return_current_time_and_date();

std::string to_hour();

std::string to_time();

std::string to_date();




///// Draw



///// Draw

void draw_lane(cv::Mat src, std::vector <cv::Point> vertices, cv::Scalar color);

bool DoesROIOverlap(cv::Rect boundingbox, std::vector <cv::Point> contour, std::string &res);

int DoesROIOverlapCount(cv::Rect boundingbox, int lanes, int &det_line, int &id);

extern std::string *StringSplit(std::string strOrigin, std::string strTok);

void front_onMouse(int event, int x, int y, int flags, void *userdata);

void end_onMouse(int event, int x, int y, int flags, void *userdata);

bool intersection(cv::Point o1, cv::Point p1, cv::Point o2, cv::Point p2, cv::Point &r);

int ccw(cv::Point p1, cv::Point p2, cv::Point p3);

int comparator(cv::Point left, cv::Point right);

void swap_(cv::Point p1, cv::Point p2);

bool LineIntersection(cv::Point x1, cv::Point x2, cv::Point y1, cv::Point y2);

bool zero_point_ext(cv::Point begin_point, cv::Point end_point);

void draw_region(const std::string &region);