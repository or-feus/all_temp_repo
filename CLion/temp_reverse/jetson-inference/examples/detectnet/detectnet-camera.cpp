/*
 * Copyright (c) 2017, NVIDIA CORPORATION. All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 *////
#include "function.hpp"
#include "MJPEGWriter.h"
#include "tracker.h"

using namespace cv;
using namespace std;

#define SIZE 1024


// cv::Point ptOld;

extern cv::Mat img;

extern string *StringSplit(string strOrigin, string strTok);

extern bool is_reverse;

int shm_signal = 0;

int number_frame = 0;
int foggy_or_storm_frame = 0;
int normal_frame = 0;

bool signal_received = false;
MJPEGWriter test(7777);

// reserve tracking variable
extern std::vector<cv::Point> front_lane;
extern std::vector<cv::Point> end_lane;

std::vector<std::pair<cv::Rect, int>> firstResults;
std::shared_ptr<SingleTracker> ptr_main;


int usage() {
    printf("usage: detectnet-camera [-h] [--network NETWORK] [--camera CAMERA]\n");
    printf("                        [--width WIDTH] [--height HEIGHT]\n\n");
    printf("Locate objects in a live camera stream using an object detection DNN.\n\n");
    printf("optional arguments:\n");
    printf("  --help           show this help message and exit\n");
    printf("  --camera CAMERA  index of the MIPI CSI camera to use (NULL for CSI camera 0),\n");
    printf("                   or for VL42 cameras the /dev/video node to use (/dev/video0).\n");
    printf("                   by default, MIPI CSI camera 0 will be used.\n");
    printf("  --width WIDTH    desired width of camera stream (default is 1280 pixels)\n");
    printf("  --height HEIGHT  desired height of camera stream (default is 720 pixels)\n\n");
    printf("%s\n", detectNet::Usage());

    return 0;
}

void sig_handler(int signo) {
    if (signo == SIGINT) {
        printf("received SIGINT\n");
        signal_received = true;
        test.stop();
        exit(1);
    }
}

int main(int argc, char **argv) {
    /*
     * parse command line
     */

    std::string search_exec_proc = "/home/user/jetson-inference/dbict/control/run";
    if (fileExists(search_exec_proc)) system("rmdir /home/user/jetson-inference/dbict/control/run");



    commandLine cmdLine(argc, argv);

    double fps_clock = 0;
    double duration = 0;

    // tracker variable

    std::vector<std::pair<cv::Rect, int>> firstResults;
    std::shared_ptr<SingleTracker> ptr_main;
    bool firstFrameWithDetections = true;
    const int update_frame = 0;
    int update_counter = 0;
    std::string last_event;
    TrackingSystem tracking_system(&last_event);

    //


    bool uart = 0;
    unsigned char connect_LMB = 0;
    unsigned char connect_CAN = 0;
    unsigned int det_code = 0;
    int reverse_count = 0;
    int trueDetect = 0;
    int notDetect = 0;
    int empty = 0;
    int det_err = 0;
    int count = 0;
    int reverse_clock = 0;


    // init parent directory
    std::string record_path = "/home/user/record";
    std::string log_path = "/home/user/detlog";

    // init record directory
    std::string record_dir_by_date = record_path + "/" + to_date();                     // ex) /home/user/record/300101
    std::string record_file_by_date = record_dir_by_date + '/' + to_hour() + ".mp4";    // ex) /home/user/record/300101/00.mp4


    // init log & detected pic directory
    std::string log_dir_by_date = log_path + "/" + to_date();                 // ex) /home/user/detlog/300101
    std::string pic_dir_by_date = log_dir_by_date + "/pic";                  // ex) /home/user/detlog/300101/pic



    if (!fileExists(record_path)) mkdir(record_path.c_str(), 0777);
    if (!fileExists(log_path)) mkdir(log_path.c_str(), 0777);
    if (!fileExists(record_dir_by_date)) mkdir(record_dir_by_date.c_str(), 0777);
    if (!fileExists(log_dir_by_date)) mkdir(log_dir_by_date.c_str(), 0777);
    if (!fileExists(pic_dir_by_date)) mkdir(pic_dir_by_date.c_str(), 0777);


    std::string ctl_dir = "/home/user/jetson-inference/dbict/control/";

    std::string run_detectnet = ctl_dir + "run";
    std::string uarton = ctl_dir + "uarton";
    std::string uartoff = ctl_dir + "uartoff";
    std::string mod = ctl_dir + "mod";
    std::string std = ctl_dir + "std";
    std::string canerr = ctl_dir + "canerr";
    std::string lmberr = ctl_dir + "lmberr";


    std::string led_o = ctl_dir + "led_o";
    std::string w_light_o = ctl_dir + "w_light_o";



    VideoWriter video;


    cv::Scalar meanValues, stdDevValues;

    CSharedMemory m;
    m.setKey(0x1000);
    m.setupSharedMemory(256);
    m.attachSharedMemory();



    std::string region("/home/user/jetson-inference/dbict/control/region.txt");
    draw_reverse_region(region);


    std::string stdnum("/home/user/jetson-inference/dbict/control/stddev.txt");
    int stddev = get_stddev(stdnum);

    if (cmdLine.GetFlag("help"))
        return usage();

    /*
     * attach signal handler
     */
    if (signal(SIGINT, sig_handler) == SIG_ERR) {
        printf("\ncan't catch SIGINT\n");
        test.stop();
    }

    /*
     * create the camera device
     */
    gstCamera *camera = gstCamera::Create(cmdLine.GetInt("width", gstCamera::DefaultWidth),
                                          cmdLine.GetInt("height", gstCamera::DefaultHeight),
                                          cmdLine.GetString("camera"));

    if (!camera) {
        printf("\ndetectnet-camera:  failed to initialize camera device\n");
        return 0;
    }

    printf("\ndetectnet-camera:  successfully initialized camera device\n");
    printf("    width:  %u\n", camera->GetWidth());
    printf("   height:  %u\n", camera->GetHeight());
    // printf("    depth:  %u (bpp)\n\n", camera->GetPixelDepth());

    /*
     * create detection network
     */
    detectNet *net = detectNet::Create(argc, argv);

    if (!net) {
        printf("detectnet-camera:   failed to load detectNet model\n");
        return 0;
    }

    // create openGL windowRect

    // glDisplay* display = glDisplay::Create();

    // if( !display )
    // 	printf("detectnet-camera:  failed to create openGL display\n");

    // start streaming/

    if (!camera->Open()) {
        printf("detectnet-camera:  failed to open camera for streaming\n");
        return 0;
    }

    printf("detectnet-camera:  camera open for streaming\n");

    /*
     * processing loop
     */

    save_nextvideo(video, record_file_by_date, record_dir_by_date);


    float confidence = 0.0f;
    test.start();
    while (!signal_received) {

        is_reverse = 0;

        bool ForcedSignal = 0;
        bool ForcedNotSignal = 0;

        duration = static_cast<double>(cv::getTickCount());



        int times = atoi(to_time().c_str());

        cv::Mat white_bg;

        white_bg = imread("/home/user/jetson-inference/dbict/picture/white.jpg", IMREAD_COLOR);
        if (white_bg.empty()) {
            cout << "could not open or find the image" << endl;
            return -1;
        }





        // init parent directory
        std::string record_path = "/home/user/record";
        std::string log_path = "/home/user/detlog";

        // init record directory
        std::string record_dir_by_date = record_path + "/" + to_date();                     // ex) /home/user/record/300101
        std::string record_file_by_date = record_dir_by_date + '/' + to_hour() + ".mp4";    // ex) /home/user/record/300101/00.mp4


        // init log & detected pic directory
        std::string log_dir_by_date =
                log_path + "/" + to_date();                                          // ex) /home/user/detlog/300101
        std::string pic_dir_by_date = log_dir_by_date + "/pic";                      // ex) /home/user/detlog/300101/pic
        std::string log_by_date = log_dir_by_date + "/" + to_hour() + "_log.txt";    // ex) /home/user/detlog/300101/00_log.txt


        std::ofstream log_file;
        log_file.open(log_by_date, std::ios_base::app);

        if (!fileExists(record_path)) mkdir(record_path.c_str(), 0777);
        if (!fileExists(log_path)) mkdir(log_path.c_str(), 0777);


        //// make directory
        if (!fileExists(record_dir_by_date)) {
            std::cout << "the current time is 00:00" << std::endl;
            std::cout << "change directory" << std::endl;
            mkdir(record_dir_by_date.c_str(), 0777);
            mkdir(log_dir_by_date.c_str(), 0777);
            mkdir(pic_dir_by_date.c_str(), 0777);
        }

        ///// create video every hours
        if (!fileExists(record_file_by_date)) {
            reverse_count = 0;
            cout << "The current time is " << to_time() << endl;
            cout << "Change video" << endl;

            video.open(record_file_by_date, VideoWriter::fourcc('a', 'v', 'c', '1'), 30,
                       cv::Size(det_width, det_height), true);

            if (!video.isOpened()) {
                cout << to_hour() << ".mp4 out failed" << endl;
                return -1;
            }
        }

        c_region(region, mod); // changed region drew
        stddev_modify(std, stddev);




        bool CarInWaitZone = false;

        // capture RGBA image
        float *imgRGBA = NULL;


        if (!camera->CaptureRGBA(&imgRGBA, 1000, 1))
            printf("detectnet-camera:  failed to capture RGBA image from camera\n");


        // detect objects in the frame
        detectNet::Detection *detections = NULL;
        const int numDetections = net->Detect(imgRGBA, camera->GetWidth(), camera->GetHeight(), &detections);

        cv::Mat cv_img = cv::Mat(camera->GetHeight(), camera->GetWidth(), CV_32FC4, imgRGBA);

        cv::Mat last_img;

        cv_img.convertTo(cv_img, CV_8UC3);

        cv::cvtColor(cv_img, cv_img, COLOR_RGBA2BGR);

        meanStdDev(cv_img, meanValues, stdDevValues);

        cv::Mat det_img = cv_img.clone();

        float FPS = 1000.0f / net->GetNetworkTime();

        if (!fileExists(run_detectnet)) mkdir(run_detectnet.c_str(), 0777);


        if (waitKey(10) == 27) {
            video.release();
            signal_received = true;
        }

        std::string str_stddev = to_string(int(stdDevValues[1]));
        int img_stddev = int(stdDevValues[1]);
        std::string normal_pic = pic_dir_by_date + "/" + return_current_time_and_date() + "_" + str_stddev + ".jpg";

        draw_lane(cv_img, front_lane, SCALAR_WHITE);
        draw_lane(cv_img, end_lane, SCALAR_WHITE);

        if (!fileExists(search_exec_proc)) system("mkdir /home/user/jetson-inference/dbict/control/run");



        if (numDetections > 0)
        {
            for (int n = 0; n < numDetections; n++) {
                Rect rect(int(detections[n].Left), int(detections[n].Top),
                          int(detections[n].Right - detections[n].Left), int(detections[n].Bottom - detections[n].Top));
                std::string res;

                firstResults.push_back(std::make_pair(rect, detections[n].ClassID));
            }

        }


        if(firstFrameWithDetections){
            tracking_system.setFrameWidth(cv_img.cols);
            tracking_system.setFrameHeight(cv_img.rows);
            tracking_system.setInitTarget(firstResults);
            tracking_system.initTrackingSystem();
        }
        if(update_counter == update_frame){
            tracking_system.updateTrackingSystem(firstResults);
        }
        int tracking_success = tracking_system.startTracking(cv_img);
        if(tracking_success == _FAIL){
            break;
        }
        if(tracking_system.getTrackerManager().getTrackerVec().size() != 0){
            tracking_system.drawTrackingResult(cv_img);
        }



        std::ostringstream out;
        out.str("");

        out << fixed;
        out.precision(2);

        out << return_current_time_and_date();

        duration = static_cast<double>(cv::getTickCount()) - duration;

        duration = duration / cv::getTickFrequency();
        fps_clock = 1 / duration;

//
//        reverse_clock = tracking_clocks(is_reverse, out);
//
//        std::cout << "reverse_clock : " << reverse_clock << std::endl;
//
//


//        out << "    fps : " << static_cast<int>(fps_clock) ;

        if (is_reverse) {
            count++;
            if (count == 1) {
                reverse_count++;
                std::cout << "reverse count:  " << reverse_count << "  " << return_current_time_and_date() << endl;
                log_file << "reverse count:  " << reverse_count << "  " << return_current_time_and_date() << endl;

                cv::imwrite(normal_pic, cv_img);

            }
        }else{
            count = 0;
        }
        if(fileExists(uarton)) is_reverse = true;
        if(fileExists(uartoff)) is_reverse = false;



        if(is_reverse) shm_signal = 1;
        else shm_signal = 0;

        if(fileExists(led_o)){
            shm_signal = 2;
        }
        if(fileExists(w_light_o)){
            shm_signal = 3;
        }
        if(shm_signal == 0){
            out << "   mode : normal" ;
        }else if(shm_signal == 1){
            out << "   mode : reverse detected" ;
        }else if(shm_signal == 2){
            out << "   mode : LED" ;
        }else if(shm_signal == 3){
            out << "   mode : Warning light" ;
        }

        cv::putText(white_bg, out.str(), cv::Point2f(5, 16), cv::FONT_HERSHEY_COMPLEX, 0.42, cv::Scalar(0, 0, 0));
        m.copyToSharedMemory(shm_signal);

//        cv::resize(cv_img, cv_img, cv::Size(320, 240), 1);
        cv::vconcat(white_bg, cv_img, last_img);


        line(last_img, Point(0, 0), Point(320, 0), cv::Scalar(0, 0, 0), 1);


        cv::imshow("destination image", last_img);
        video.write(last_img);
        test.write(last_img);

        firstFrameWithDetections = false;
        firstResults.clear();
        update_counter++;
        if(update_counter > update_frame){
            update_counter = 0;
        }

//        duration = static_cast<double>(cv::getTickCount()) - duration;
//
//        duration = duration / cv::getTickFrequency();
//        fps_clock = 1 / duration;
//        cout << static_cast<int>(fps_clock) << endl ;
#if 0
#endif



        // print out timing info
        //net->PrintProfilerTimes();



    }
    /*
    destroy resources

    printf("detectnet-camera:  shutting down...\n");

    SAFE_DELETE(camera);
    SAFE_DELETE(display);
    SAFE_DELETE(net);

    printf("detectnet-camera:  shutdown complete.\n");
    */
    return 0;
}

