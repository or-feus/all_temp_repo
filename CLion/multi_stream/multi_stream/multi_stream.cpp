#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include "json.hpp"
#include "MJPEGWriter.h"

using json = nlohmann::json;
MJPEGWriter test(9999);

/* 참고사항
 * 1. 4채널의 영상은 전부 동일한 프레임이 되어야 한다.
 * 2. 화면의 drop frame을 감지할 수 있는 로직을 생성해야 한다.
 * 3. 비어있는 화면은 검은 화면으로 대체 한다.
 * 4. 화면은 640 x 480의 화면으로 생성한다.
 * 5. if frame의 크기가 0이 되면 frame 재생성 같은 로직 만들기
 * */


std::vector<std::string> urls(const std::string &json_file) {
    std::ifstream i(json_file);
    json j;
    i >> j;

    const auto nano = j["nano"];
    const int quantity = nano["active_numbers"];

    std::vector<std::string> v;

    for (int i = 0; i < quantity; ++i) {
        v.push_back(nano["machine"][i]["ip"]);
    }

    return v;
}



int main(int argc, char **argv) {
    std::string path = argv[1];
    std::vector<std::string> v = urls(path);

    const int quantity = v.size();

    cv::Mat black(240, 320, CV_8UC3, cv::Scalar(0, 0, 0));

    double fps_clock = 0;
    double duration = 0;

    cv::Mat result;
    cv::Mat row1;
    cv::Mat row2;
    cv::Mat frame[4];
    cv::VideoCapture cap[quantity];
    for (int i = 0; i < v.size(); ++i) {
        cap[i] = cv::VideoCapture(v[i]);
    }

    if(v.size() < 4) {
        if((4- v.size() == 0)){}
        else if((4 - v.size()) == 1){
            frame[3] = black.clone();
        }
        else if((4 - v.size()) == 2){
            frame[3] = black.clone();
            frame[2] = black.clone();
        }
        else if((4 - v.size()) == 3){
            frame[3] = black.clone();
            frame[2] = black.clone();
            frame[1] = black.clone();
        }else{
            std::cout << "do not exist frames" << std::endl;
            return -1;
        }
    }
    test.start();

    while (1) {

        duration = static_cast<double>(cv::getTickCount());

//        if(v.size() < 4) {
//            cv::Mat image
//        }

        for (int i = 0; i < v.size(); ++i) {
            cap[i] >> frame[i];
            std::cout << "no." << i+1 << ":" << cap[i].get(cv::CAP_PROP_FRAME_WIDTH) << "," << cap[i].get(cv::CAP_PROP_FRAME_HEIGHT) << endl;
        }
        cv::hconcat(frame[0], frame[1], row1);
        cv::hconcat(frame[2], frame[3], row2);
        cv::vconcat(row1, row2, result);
        if (waitKey(10) == 27) break;

        test.write(result);
        duration = static_cast<double>(cv::getTickCount()) - duration;
        duration = duration / cv::getTickFrequency();
        fps_clock = 1 / duration;
//        std::cout << "FPS: " << fps_clock << endl;
    }

    return 0;
}
