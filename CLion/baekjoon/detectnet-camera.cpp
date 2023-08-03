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
using namespace cv;
using namespace std;

#define SIZE 1024


// cv::Point ptOld;


extern cv::Mat img;
extern std::vector<cv::Point> RoiVtx;
extern string* StringSplit(string strOrigin, string strTok);
bool signal_recieved = false;
MJPEGWriter test(7777);



int usage(){
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
void sig_handler(int signo){
        if( signo == SIGINT )
        {
                printf("received SIGINT\n");
                signal_recieved = true;
                test.stop();
                exit(1);
        }
}

int main( int argc, char** argv ){
        /*
         * parse command line
         */



        commandLine cmdLine(argc, argv);

        double fps_clock = 0 ;
        double duration = 0;



        unsigned char uart = 0;
        int stddev = 0;
        int car_in_day = 0;
        int car_in_day2 = 0;
        int car_in_clock = 0;
        int car_in_clock2 = 0;
        int car_in =  0;
        int detect_in = 0;
        int trueDetect = 0;
        int totalframe = 0;
        int notDetect = 0;
        int empty = 0;
        int number_frame = 0;
        int foggy_or_storm_frame = 0;
        int normal_frame = 0;
        int det_err = 0;
        int count = 0;
        int sw_on = 0;
        int sw_off = 0;
        int one_second = 6;
        int poly[256];
        char fName[100];
        char gName[100];
        char sys_rm[100];
        std::ifstream region("/home/user/region.txt");
        std::string path = "/home/user/data/" + to_date() ;
        std::string path_pic = "/home/user/data/" + to_date() + "/" + to_date() + "pic";
        std::string path_rain_pic = "/home/user/data/" + to_date() + "/" + to_date() + "_rainpic";
        std::string begin_video_name = "/home/user/data/" + to_date() + '/' + to_hour() + ".mp4";



        std::string prev_run_detectnet = "/home/user/run";

        ifstream prev_search_run ;
        prev_search_run.open(prev_run_detectnet);

        if(prev_search_run){
                system("rmdir /home/user/run");
        }


        VideoWriter video;
        ifstream begin_video_search;

        begin_video_search.open(begin_video_name);

        cv::Scalar meanValues, stdDevValues;

        CSharedMemroy m;
        m.setKey(0x1000);
        m.setupSharedMemory(256);
        m.attachSharedMemory();

        if(!region){
                std::string winname = "window";
                std::ifstream url("/home/user/url.txt");
                std::string get_url;
                getline(url, get_url);
                VideoCapture cap(get_url);

                if(!cap.isOpened()){
                        "VIDEO load failed";
                        return 1;
                }

                cv::namedWindow(winname);

                while(cap.isOpened()){
                        int key = waitKey(100);
                        ofstream edit;
                        edit.open("/home/user/region.txt", std::ios_base::out | std::ios_base::app);
                        cv::moveWindow(winname, 10, 10);
                        cap >> img;


                        cv::waitKey(1);
                        cv::resize(img, img,cv::Size(640,480),1);
                        cv::setMouseCallback(winname, onMouse, NULL);
                        draw_ploygon(img, RoiVtx,SCALAR_WHITE);
                        if(key=='o'){
                                std::cout << "Good" << endl;
                                for(int i=0; i < (RoiVtx.size()) ; i++){
                                        edit << RoiVtx[i].x << " " << RoiVtx[i].y << " ";
                                }
                                cv::destroyWindow(winname);
                                break;
                        }else if(key== 'x'){
                                std::cout << "Region clear" << endl ;
                                RoiVtx.clear();
                        }
                        cv::imshow(winname, img);
                }
        }else{
                if(region.is_open()){
                        while(!region.eof()){

                                std::string position;
                                getline(region,position);
                                string* points = new string[256];
                                points = StringSplit(position," ");
                                for(int i=0; i <= 30 ; i++){
                                        poly[i*2] = atoi(points[i*2].c_str());
                                        poly[i*2+1] = atoi(points[i*2+1].c_str());
                                        if(poly[i*2] != 0 && poly[i*2+1] != 0){
                                                RoiVtx.push_back(Point(poly[i*2],poly[i*2+1]));
                                        }
                                }
                        }
                }
        }


        std::ifstream stdnum("/home/user/stddev.txt");
        std::string get_std;
        getline(stdnum, get_std);
        stddev = stoi(get_std);




        region.close();
        if( cmdLine.GetFlag("help") )
                return usage();

        /*
         * attach signal handler
         */
        if( signal(SIGINT, sig_handler) == SIG_ERR ){
                printf("\ncan't catch SIGINT\n");
                test.stop();
        }

        /*
         * create the camera device
         */
        gstCamera* camera = gstCamera::Create(cmdLine.GetInt("width", gstCamera::DefaultWidth),
                                                                   cmdLine.GetInt("height", gstCamera::DefaultHeight),
                                                                   cmdLine.GetString("camera"));

        if( !camera )
        {
                printf("\ndetectnet-camera:  failed to initialize camera device\n");
                return 0;
        }

        printf("\ndetectnet-camera:  successfully initialized camera device\n");
        printf("    width:  %u\n", camera->GetWidth());
        printf("   height:  %u\n", camera->GetHeight());
        printf("    depth:  %u (bpp)\n\n", camera->GetPixelDepth());

        /*
         * create detection network
         */
        detectNet* net = detectNet::Create(argc, argv);

        if( !net )
        {
                printf("detectnet-camera:   failed to load detectNet model\n");
                return 0;
        }

        // create openGL windowRect

        // glDisplay* display = glDisplay::Create();

        // if( !display )
        //      printf("detectnet-camera:  failed to create openGL display\n");

        // start streaming/

        if( !camera->Open() )
        {
                printf("detectnet-camera:  failed to open camera for streaming\n");
                return 0;
        }

        printf("detectnet-camera:  camera open for streaming\n");

        /*
         * processing loop
         */

        int resulte = mkdir(path.c_str(), 0777);
        int pathpicdir = mkdir(path_pic.c_str(), 0777);
        int pathrainpicdir = mkdir(path_rain_pic.c_str(), 0777);




        if(!begin_video_search){
                cout << "create begin video. time : " << return_current_time_and_date() << endl;
                video.open(begin_video_name, VideoWriter::fourcc('a','v','c','1'), 30, cv::Size(320,265), true);
                begin_video_search.close();
        }else{
                FILE *f;
                FILE *g;
                strcpy(fName, begin_video_name.c_str());

                f = fopen(fName, "r");
                fseek(f, 0, SEEK_END);
                int fileLength = ftell(f);
                fclose(f);

                if(fileLength < 100){
                        string ffname = "rm " + begin_video_name;
                        // CFile::Remove(ffname);
                        strcpy(sys_rm, ffname.c_str());
                        system(sys_rm);
                        cout << "change file   time : " << return_current_time_and_date() << endl;
                        video.open(begin_video_name, VideoWriter::fourcc('a','v','c','1'), 30, cv::Size(320,265), true);
                }else{
                        for(int i=1; i < 10; i++){
                                begin_video_name = "/home/user/data/" + to_date() + "/" + to_hour() + "_" + to_string(i) + ".mp4";
                                ifstream begin_video_search;
                                begin_video_search.open(begin_video_name);

                                if(begin_video_search){
                                        strcpy(gName, begin_video_name.c_str());

                                        g = fopen(gName, "r");
                                        fseek(g, 0, SEEK_END);
                                        int fileLengths = ftell(g);
                                        fclose(g);
                                        if(fileLengths < 100){
                                                string ffname = "rm " + begin_video_name;
                                                strcpy(sys_rm, ffname.c_str());
                                                system(sys_rm);
                                                cout << "create number " << i << " video. time : " << return_current_time_and_date() << "  remove begin video" << endl;
                                                video.open(begin_video_name, VideoWriter::fourcc('a','v','c','1'), 30, cv::Size(320,265), true);
                                                begin_video_search.close();
                                                break;
                                        }
                                }else{
                                        cout << "create number " << i << " video. time : " << return_current_time_and_date() << "  remove begin video" << endl;
                                        video.open(begin_video_name, VideoWriter::fourcc('a','v','c','1'), 30, cv::Size(320,265), true);
                                        begin_video_search.close();
                                        break;
                                }
                        }
                }
        }

        float confidence = 0.0f;
        test.start();
        while( !signal_recieved )
        {

                count++;

                duration = static_cast<double>(cv::getTickCount());


                int times = atoi(to_time().c_str());

                cv::Mat white_bg;

                white_bg = imread("/home/user/white.jpg",IMREAD_COLOR);
                if(white_bg.empty()){
                        cout << "could not open or find the image" << endl;
                        return -1;
                }


                std::string run_detectnet = "/home/user/run";
                std::string uarton = "/home/user/uarton";
                std::string uartoff = "/home/user/uartoff";


                std::string mod = "/home/user/mod";
                std::string std = "/home/user/std";

                std::string canerr = "/home/user/canerr";
                std::string lmberr = "/home/user/lmberr";



                ifstream search_on ;
                search_on.open(uarton);

                ifstream search_off ;
                search_off.open(uartoff);

                ifstream search_mod ;
                search_mod.open(mod);

                ifstream search_std ;
                search_std.open(std);

                ifstream search_can ;
                search_can.open(canerr);

                ifstream search_lmb ;
                search_lmb.open(lmberr);

                ifstream search_run ;
                search_run.open(run_detectnet);



                std::string path = "/home/user/data/" + to_date() ;
                std::string path_pic = "/home/user/data/" + to_date() + "/" + to_date() + "pic";
                std::string path_rain_pic = "/home/user/data/" + to_date() + "/" + to_date() + "_rainpic";
                std::string video_name = "/home/user/data/" + to_date() + '/' + to_hour() +".mp4";
                std::string video_log = "/home/user/data/" + to_date() + '/' + to_hour() +"_log.txt";

        std::ofstream log_every_hours;
        log_every_hours.open(video_log, std::ios_base::app);

                bool Object_Detection = false;
                ///// check File existence /////

                ifstream search_path_dir;
                search_path_dir.open(path);

                ifstream search_video;
                search_video.open(video_name);


                /////make directory /////
                if(!search_path_dir){
                        cout << "The currut time is 00:00" << endl ;
                        cout << "Change directory" << endl;
                        int pathdir = mkdir(path.c_str(), 0777);
                        int pathpicdir = mkdir(path_pic.c_str(), 0777);
                        int pathrainpicdir = mkdir(path_rain_pic.c_str(), 0777);
                        system("sudo find /home/user/data/* -mtime +100 -exec rm {} -r \\;");
                        car_in_day = 0;
                        car_in_clock = 0;
                        car_in_day2 = 0;
                        car_in_clock2 = 0;
                }

                ///// create video every hours /////

                if(!search_video){
                        car_in = 0;
                        cout << "The currut time is " << to_time()<< endl ;
                        cout << "Change video" << endl;
                        int fourcc = VideoWriter::fourcc('a','v','c','1');
                        video.open(video_name, fourcc,30, cv::Size(320,265), true);

                        if (!video.isOpened())
                        {
                                cout << to_hour() << ".mp4 out failded" << endl;
                                return -1;
                        }
                }

                if(search_mod){
                        std::ifstream region("/home/user/region.txt");
                        if(region.is_open()){
                                RoiVtx.clear();
                                while(!region.eof()){
                                        std::string position;
                                        getline(region,position);
                                        string* points = new string[256];
                                        points = StringSplit(position," ");
                                        for(int i=0; i <= 30 ; i++){
                                                poly[i*2] = atoi(points[i*2].c_str());
                                                poly[i*2+1] = atoi(points[i*2+1].c_str());
                                                if(poly[i*2] != 0 && poly[i*2+1] != 0){
                                                        RoiVtx.push_back(Point(poly[i*2],poly[i*2+1]));
                                                }
                                        }
                                }
                        }
                        region.close();
                        system("rmdir /home/user/mod");
                }

                if(search_std){
                        std::ifstream std("/home/user/stddev.txt");
                        std::string get_std;
                        getline(std, get_std);
                        stddev = stoi(get_std);
                        system("rmdir /home/user/std");
                }


                totalframe++;

        bool CarInWaitZone=false;

                // capture RGBA image
                float* imgRGBA = NULL;


                if( !camera->CaptureRGBA(&imgRGBA, 1000, 1) )
                        printf("detectnet-camera:  failed to capture RGBA image from camera\n");
                // ////run detectnet /////
                if(!search_run){
                        system("mkdir /home/user/run");
                }

                // detect objects in the frame
                detectNet::Detection* detections = NULL;
                const int numDetections = net->Detect(imgRGBA, camera->GetWidth(), camera->GetHeight(), &detections);

                cv::Mat cv_img = cv::Mat(camera->GetHeight(), camera->GetWidth(), CV_32FC4, imgRGBA);
                cv::Mat det_img;
                cv::Mat last_img;

                cv_img.convertTo(cv_img, CV_8UC3);

                cv::cvtColor(cv_img, cv_img, COLOR_RGBA2BGR);

                meanStdDev(cv_img, meanValues, stdDevValues);

                float FPS = 1000.0f / net->GetNetworkTime();

                cv::resize(cv_img, det_img,cv::Size(320, 240),1);

                if(waitKey(10)== 27){
                        video.release();
                        signal_recieved = true;
                }
                draw_ploygon(cv_img, RoiVtx,SCALAR_WHITE);

                std::string str_stddev = to_string(int(stdDevValues[1]));

                std::string detectpic;
                detectpic = path_pic + "/" + return_current_time_and_date() + "_" + str_stddev + ".jpg";

                std::string foggypic;
                foggypic = path_rain_pic + "/" + return_current_time_and_date() + "_" + str_stddev + ".jpg";



                // if(totalframe ==0xff)
                //      totalframe = 0;

                if( numDetections > 0 )
                {
                        //printf("%i objects detected\n", numDetections);

                        for( int n=0; n < numDetections; n++ )
                        {
                                Rect rect(int(detections[n].Left),int(detections[n].Top),int(detections[n].Right-detections[n].Left),int(detections[n].Bottom-detections[n].Top));
                                std::string res;

                                if(DoesROIOverlap(rect,RoiVtx,res))
                                {
                                        cv::rectangle(cv_img, rect, SCALAR_BLUE, 2);
                                        CarInWaitZone=true;

                                }else{
                                        cv::rectangle(cv_img, rect, SCALAR_RED, 2);
                                }
                                //printf("detected obj %i  class #%u (%s)  confidence=%f\n", n, detections[n].ClassID, net->GetClassDesc(detections[n].ClassID), detections[n].Confidence);
                                //printf("bounding box %i  (%f, %f)  (%f, %f)  w=%f  h=%f\n", n, detections[n].Left, detections[n].Top, detections[n].Right, detections[n].Bottom, detections[n].Width(), detections[n].Height());

            }
                        if(CarInWaitZone){
                                trueDetect++;
                                Object_Detection= true;
                                notDetect = 0;


                                if(trueDetect >= one_second * 3){
                                        draw_ploygon(cv_img, RoiVtx, SCALAR_GREEN);
                                        notDetect = 0;
                    uart= 1;
                    empty= 0;
                                        detect_in++;
                                        if(trueDetect == one_second * 3){
                                                car_in_clock += 1;
                                                trueDetect += 1;
                                                car_in++;
                                                car_in_day++;
                                                std::cout << "DETECT :    " << car_in << "    " << return_current_time_and_date() <<"    in" << endl;
                                                log_every_hours << "DETECT :    " << car_in << "    " << return_current_time_and_date() <<"    in"<< endl;

                                                notDetect = 0;

                                                if(stdDevValues[1] > 20){
                                                        cv::imwrite(detectpic, det_img);
                                                }else{
                                                        cv::imwrite(foggypic, det_img);
                                                }

                                                if(car_in_day% 256 == 0){
                                                        car_in_day2 ++;
                                                }
                                        }
                                        if(detect_in % one_second == 0){
                                                car_in_clock++;
                                                if(car_in_clock % 256 == 0){
                                                        car_in_clock2++;
                                                }
                                        }
                }
                        }else{
                notDetect++;
                draw_ploygon(cv_img, RoiVtx,SCALAR_WHITE);
            }
                        if(uart && notDetect > one_second){
                                trueDetect = 0;
                                notDetect = 0;
                                empty = 0;
                                uart = 0;
                        }
                        if(trueDetect < one_second * 3 && notDetect > one_second * 3){
                                trueDetect = 0;
                                notDetect = 0;
                                empty = 0;
                                uart = 0;
                        }
                }
                if(numDetections == 0){
                        empty++;
                        if(empty > 5){
                        uart = 0;
                        trueDetect = 0;
            notDetect = 0;
                        empty = 0;
                        }
                }

                if(stdDevValues[1] < stddev){
                        foggy_or_storm_frame++;
                        normal_frame = 0;
                        if(foggy_or_storm_frame >= one_second * 2){
                                normal_frame = 0;
                                uart = 1;
                                if(foggy_or_storm_frame == one_second * 2){
                                        std::cout << "Start BAD weather:\t" << return_current_time_and_date()  <<"\tStdDev:\t" << stdDevValues[1] << endl;
                                        log_every_hours << "Start BAD weather:\t" << return_current_time_and_date() <<"\tStdDev:\t" << stdDevValues[1] << endl;
                                }
                        }
                }else{
                        normal_frame++;
                }
        if(foggy_or_storm_frame > one_second * 2 && normal_frame > one_second * 3 ){
                        foggy_or_storm_frame = 0;
                        uart = 0;
                        std::cout << "Stop BAD weather:\t" << return_current_time_and_date()  <<"\tStdDev:\t" << stdDevValues[1] << endl;
                        log_every_hours << "Stop BAD weather:\t" << return_current_time_and_date() <<"\tStdDev:\t" << stdDevValues[1] << endl;
        }
                if(foggy_or_storm_frame < one_second * 2 && normal_frame > one_second * 3 ){
                        foggy_or_storm_frame = 0;
                }


                if(search_on){
                        uart = 1;
                        draw_ploygon(cv_img, RoiVtx, SCALAR_GREEN);
                }

                if(search_off){
                        uart = 0;
                        draw_ploygon(cv_img, RoiVtx, SCALAR_RED);
                }



                std::ostringstream out;
                out.str("");

                out << fixed;
                out.precision(2);

                out << return_current_time_and_date();

        // if(uart){
        //     out << "    O";
        // }else{
        //     out << "    X";
                // }
                out <<" Std:" << stdDevValues[1] ;

                if(search_can){
            out << "  CAN: X";
        }else{
            out << "  CAN: O";
                }
                if(search_lmb){
            out << "  LMB: X";
        }else{
            out << "  LMB: O";
                }
                cv::putText(white_bg, out.str(), cv::Point2f(5, 16), cv::FONT_HERSHEY_COMPLEX, 0.42, cv::Scalar(0, 0, 0));


                m.copyToSharedMemroy(totalframe, uart, car_in_day2, car_in_day, car_in_clock2, car_in_clock);

                cv::resize(cv_img, cv_img,cv::Size(320,240),1);
                cv::vconcat(white_bg,cv_img,last_img);

                cv::imshow("destination image", last_img);
        video.write(last_img);
                test.write(last_img);

                // uart = 0;
                // // update OpenGL display
                // if( display != NULL )
                // {
                //      // render the image
                //      display->RenderOnce(imgRGBA, camera->GetWidth(), camera->GetHeight());

                //      // update the status bar
                //      char str[256];
                //      sprintf(str, "TensorRT %i.%i.%i | %s | Network %.0f FPS", NV_TENSORRT_MAJOR, NV_TENSORRT_MINOR, NV_TENSORRT_PATCH, precisionTypeToStr(net->GetPrecision()), 1000.0f / net->GetNetworkTime());
                //      display->SetTitle(str);

                //      // check if the user quit
                //      if( display->IsClosed() )
                //              signal_recieved = true;
                // }

                duration = static_cast<double>(cv::getTickCount())-duration;

                duration = duration / cv::getTickFrequency();
                fps_clock = 1 / duration ;
                // cout << fps_clock << endl ;
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

