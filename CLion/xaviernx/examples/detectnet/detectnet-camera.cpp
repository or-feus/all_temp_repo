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

extern bool reverse_tracker;

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


    unsigned char uart = 0;
    unsigned char connect_LMB = 0;
    unsigned char connect_CAN = 0;
    unsigned int det_code = 0;
    int stddev = 0;
    int car_in_day = 0;
    int car_in_day2 = 0;
    int car_in_clock = 0;
    int car_in_clock2 = 0;
    int car_in = 0;
    int detect_in = 0;
    int trueDetect = 0;
    int totalframe = 0;
    int notDetect = 0;
    int empty = 0;
    int foggy_or_storm_frame = 0;
    int normal_frame = 0;
    int det_err = 0;
    int count = 0;
    const int one_second = 6;

    int draw_region_step = 0;
    int length = 0;


    char fName[100];
    char gName[100];
    char sys_rm[100];

    std::ifstream region("/home/user/jetson-inference/dbict/control/region.txt");

    /// record
    std::string record_dir = "/home/user/record/" + to_date();
    std::string record = "/home/user/record/" + to_date() + '/' + to_hour() + ".mp4";


    /// detected log
    std::string det_log_pic_dir = "/home/user/detect_log/" + to_date();
    std::string det_pic = "/home/user/detect_log/" + to_date() + "/" + to_date() + "pic";
    std::string det_rain_pic = "/home/user/detect_log/" + to_date() + "/" + to_date() + "_rain_pic";


    std::string prev_run_detectnet = "/home/user/jetson-inference/dbict/control/run";

    ifstream prev_search_run;
    prev_search_run.open(prev_run_detectnet);

    if (prev_search_run) {
        system("rmdir /home/user/jetson-inference/dbict/control/run");
    }


    VideoWriter video;


    /// init video file
    ifstream begin_video_search;
    begin_video_search.open(record);

    cv::Scalar meanValues, stdDevValues;

    CSharedMemroy m;
    m.setKey(0x1000);
    m.setupSharedMemory(8);
    m.attachSharedMemory();

    int poly[256];

    if(!region){
        std::ifstream url("/home/user/jetson-inference/dbict/control/url.txt");
        std::string get_url;
        getline(url, get_url);

        cv::VideoCapture cap(get_url);

        std::string winname = "winname";

        if(!cap.isOpened()){
            "VIDEO load failed";
            return -1;
        }

        cv::namedWindow(winname);
        cv::Mat draw_img;


        while(cap.isOpened()){

            std::ofstream edit;
            edit.open("/home/user/jetson-inference/dbict/control/region.txt", std::ios_base::out | std::ios_base::app);
            int key = cv::waitKey(100);

            cap >> draw_img;
            cv::waitKey(1);

            std::ostringstream out;
            out.str("");

            draw_lane(draw_img, front_lane, SCALAR_WHITE);
            draw_lane(draw_img, end_lane, SCALAR_WHITE);

            if(draw_region_step == 0){
                out << "Draw front lane";
                cv::setMouseCallback(winname, front_onMouse, NULL);

                if(key == 'o'){
                    for(int i = 0; i < front_lane.size() ; i++){
                        edit << front_lane[i].x << " " << front_lane[i].y << " ";
                    }
                    edit << std::endl ;
                    std::cout << "complete draw front lane" << std::endl;

                    draw_region_step++;
                }else if(key == 'x'){
                    front_lane.clear();
                }

            }else if(draw_region_step == 1 ){
                out << "Draw end lane";
                cv::setMouseCallback(winname, end_onMouse, NULL);

                if(key == 'o'){
                    for(int i = 0; i < end_lane.size() ; i++){
                        edit << end_lane[i].x << " " << end_lane[i].y << " ";
                    }
                    draw_region_step++;
                    cv::destroyWindow(winname);
                    break;
                }else if(key == 'x'){
                    end_lane.clear();
                }
            }
            cv::imshow(winname,  draw_img);
        }

    }else{
        if(region.is_open()){
            while(!region.eof()){

                std::string position;
                getline(region, position);
                std::string *points = new std::string[256];

                points = StringSplit(position, " ");
                length++;


                for(int i=0; i < sizeof(points) / 2 ; i++){
                    poly[i*2] = atoi(points[i*2].c_str());
                    poly[i*2+1] = atoi(points[i*2+1].c_str());
                    if(length==1){
                        front_lane.push_back(cv::Point(poly[i*2],poly[i*2+1]));
                    }else if(length==2){
                        end_lane.push_back(cv::Point(poly[i*2],poly[i*2+1]));
                    }
                }
            }
        }
    }
    region.close();


    std::ifstream stdnum("/home/user/jetson-inference/dbict/control/stddev.txt");
    std::string get_std;
    getline(stdnum, get_std);
    stddev = stoi(get_std);


    region.close();
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

    int make_record_dir = mkdir(record_dir.c_str(), 0777);
    int make_log_pic_dir = mkdir(det_log_pic_dir.c_str(), 0777);
    int make_det_pic = mkdir(det_pic.c_str(), 0777);
    int make_det_rain_pic = mkdir(det_rain_pic.c_str(), 0777);


    if (!begin_video_search) {
        cout << "create begin video. time : " << return_current_time_and_date() << endl;
        video.open(record, VideoWriter::fourcc('a', 'v', 'c', '1'), 30, cv::Size(320, 265), true);
        begin_video_search.close();
    } else {
        FILE *f;
        FILE *g;
        strcpy(fName, record.c_str());

        f = fopen(fName, "r");
        fseek(f, 0, SEEK_END);
        int fileLength = ftell(f);
        fclose(f);

        if (fileLength < 100) {
            string ffname = "rm " + record;
            // CFile::Remove(ffname);
            strcpy(sys_rm, ffname.c_str());
            system(sys_rm);
            cout << "change file   time : " << return_current_time_and_date() << endl;
            video.open(record, VideoWriter::fourcc('a', 'v', 'c', '1'), 30, cv::Size(320, 265), true);
        } else {
            for (int i = 1; i < 10; i++) {
                record = "/home/user/record/" + to_date() + "/" + to_hour() + "_" + to_string(i) + ".mp4";
                ifstream begin_video_search;
                begin_video_search.open(record);

                if (begin_video_search) {
                    strcpy(gName, record.c_str());

                    g = fopen(gName, "r");
                    fseek(g, 0, SEEK_END);
                    int fileLengths = ftell(g);
                    fclose(g);
                    if (fileLengths < 100) {
                        string ffname = "rm " + record;
                        strcpy(sys_rm, ffname.c_str());
                        system(sys_rm);
                        cout << "create number " << i << " video. time : " << return_current_time_and_date()
                             << "  remove begin video" << endl;
                        video.open(record, VideoWriter::fourcc('a', 'v', 'c', '1'), 30, cv::Size(320, 265), true);
                        begin_video_search.close();
                        break;
                    }
                } else {
                    cout << "create number " << i << " video. time : " << return_current_time_and_date()
                         << "  remove begin video" << endl;
                    video.open(record, VideoWriter::fourcc('a', 'v', 'c', '1'), 30, cv::Size(320, 265), true);
                    begin_video_search.close();
                    break;
                }
            }
        }
    }

    float confidence = 0.0f;
    test.start();
    while (!signal_received) {

        reverse_tracker = 0;

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


        std::string run_detectnet = "/home/user/jetson-inference/dbict/control/run";
        std::string uart_on = "/home/user/jetson-inference/dbict/control/uart_on";
        std::string uart_off = "/home/user/jetson-inference/dbict/control/uart_off";


        std::string edit_region = "/home/user/jetson-inference/dbict/control/mod";
        std::string std = "/home/user/jetson-inference/dbict/control/std";

        std::string can_error = "/home/user/jetson-inference/dbict/control/can_error";
        std::string lmb_error = "/home/user/jetson-inference/dbict/control/lmb_error";


        ifstream search_on;
        search_on.open(uart_on);

        ifstream search_off;
        search_off.open(uart_off);

        ifstream search_mod;
        search_mod.open(edit_region);

        ifstream search_std;
        search_std.open(std);

        ifstream search_can;
        search_can.open(can_error);

        ifstream search_lmb;
        search_lmb.open(lmb_error);

        ifstream search_run;
        search_run.open(run_detectnet);



        /// record
        std::string record_dir = "/home/user/record/" + to_date();
        std::string record = "/home/user/record/" + to_date() + '/' + to_hour() + ".mp4";


        /// detected log
        std::string det_log_pic_dir = "/home/user/detect_log/" + to_date();
        std::string det_pic = "/home/user/detect_log/" + to_date() + "/" + to_date() + "pic";
        std::string det_rain_pic = "/home/user/detect_log/" + to_date() + "/" + to_date() + "_rain_pic";
        std::string video_log = "/home/user/detect_log/" + to_date() + '/' + to_hour() + "_log.txt";


        std::ofstream log_every_hours;
        log_every_hours.open(video_log, std::ios_base::app);

        bool Object_Detection = false;
        ///// check File existence /////

        ifstream search_record_dir;
        search_record_dir.open(record_dir);

        ifstream search_record;
        search_record.open(record);


        /////make directory /////
        if (!search_record_dir) {
            cout << "The currut time is 00:00" << endl;
            cout << "Change directory" << endl;

            int make_record_dir = mkdir(record_dir.c_str(), 0777);
            int make_log_pic_dir = mkdir(det_log_pic_dir.c_str(), 0777);
            int make_det_pic = mkdir(det_pic.c_str(), 0777);
            int make_det_rain_pic = mkdir(det_rain_pic.c_str(), 0777);

            system("sudo find /home/user/record/* -mtime +100 -exec rm {} -r \\;");
            system("sudo find /home/user/detect_log/* -mtime +100 -exec rm {} -r \\;");

            car_in_day = 0;
            car_in_clock = 0;
            car_in_day2 = 0;
            car_in_clock2 = 0;
        }

        ///// create video every hours /////

        if (!search_record) {
            car_in = 0;
            cout << "The currut time is " << to_time() << endl;
            cout << "Change video" << endl;
            int fourcc = VideoWriter::fourcc('a', 'v', 'c', '1');
            video.open(record, fourcc, 30, cv::Size(320, 265), true);

            if (!video.isOpened()) {
                cout << to_hour() << ".mp4 out failded" << endl;
                return -1;
            }
        }

        if (search_mod) {
            std::ifstream region("/home/user/jetson-inference/dbict/control/region.txt");
            if(region.is_open()){
                while(!region.eof()){

                    std::string position;
                    getline(region, position);
                    std::string *points = new std::string[256];

                    points = StringSplit(position, " ");
                    length++;


                    for(int i=0; i < sizeof(points) / 2 ; i++){
                        poly[i*2] = atoi(points[i*2].c_str());
                        poly[i*2+1] = atoi(points[i*2+1].c_str());
                        if(length==1){
                            front_lane.push_back(cv::Point(poly[i*2],poly[i*2+1]));
                        }else if(length==2){
                            end_lane.push_back(cv::Point(poly[i*2],poly[i*2+1]));
                        }
                    }
                }
            }
            region.close();
            system("rmdir /home/user/jetson-inference/dbict/control/mod");
        }

        if (search_std) {
            std::ifstream std("/home/user/jetson-inference/dbict/control/stddev.txt");
            std::string get_std;
            getline(std, get_std);
            stddev = stoi(get_std);
            system("rmdir /home/user/jetson-inference/dbict/control/std");
        }


        totalframe++;

        bool CarInWaitZone = false;

        // capture RGBA image
        float *imgRGBA = NULL;


        if (!camera->CaptureRGBA(&imgRGBA, 1000, 1))
            printf("detectnet-camera:  failed to capture RGBA image from camera\n");

        // ////run detectnet /////
        if (!search_run) {
            system("mkdir /home/user/jetson-inference/dbict/control/run");
        }

        // detect objects in the frame
        detectNet::Detection *detections = NULL;
        const int numDetections = net->Detect(imgRGBA, camera->GetWidth(), camera->GetHeight(), &detections);

        cv::Mat cv_img = cv::Mat(camera->GetHeight(), camera->GetWidth(), CV_32FC4, imgRGBA);

        cv::Mat last_img;

        cv_img.convertTo(cv_img, CV_8UC3);

        cv::cvtColor(cv_img, cv_img, COLOR_RGBA2BGR);

        meanStdDev(cv_img, meanValues, stdDevValues);

        float FPS = 1000.0f / net->GetNetworkTime();

        cv::Mat det_capture = cv_img;

        if (waitKey(10) == 27) {
            video.release();
            signal_received = true;
        }



        std::string str_stddev = to_string(int(stdDevValues[1]));

        std::string clear_pic;
        clear_pic = det_pic + "/" + return_current_time_and_date() + "_" + str_stddev + ".jpg";

        std::string bad_pic;
        bad_pic = det_rain_pic + "/" + return_current_time_and_date() + "_" + str_stddev + ".jpg";



//        draw_lane(cv_img, front_lane, SCALAR_WHITE);
//        draw_lane(cv_img, end_lane, SCALAR_WHITE);
        // if(totalframe ==0xff)
        // 	totalframe = 0;

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

        cv::putText(white_bg, out.str(), cv::Point2f(5, 16), cv::FONT_HERSHEY_COMPLEX, 0.42, cv::Scalar(0, 0, 0));
        m.copyToSharedMemory(reverse_tracker);

        cv::resize(cv_img, cv_img, cv::Size(320, 240), 1);
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

        duration = static_cast<double>(cv::getTickCount()) - duration;

        duration = duration / cv::getTickFrequency();
        fps_clock = 1 / duration;
//        cout << fps_clock << endl ;
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

