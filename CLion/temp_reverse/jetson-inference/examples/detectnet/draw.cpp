#include "function.hpp"

cv::Mat img;
std::vector <cv::Point> front_lane;
std::vector <cv::Point> end_lane;


void draw_reverse_region(const std::string &region) {

    int poly[256];
    int draw_region_step = 0;
    int length = 0;

    if (!fileExists(region)) {
        std::ifstream url("/home/user/jetson-inference/dbict/control/url.txt");
        std::string get_url;
        getline(url, get_url);
        cv::VideoCapture cap(get_url);
        std::string winname = "winname";

        if (!cap.isOpened()) {
            "VIDEO load failed";
            exit(0);
        }

        cv::namedWindow(winname);
        cv::Mat draw_img;


        while (cap.isOpened()) {

            std::ofstream edit;
            edit.open("/home/user/jetson-inference/dbict/control/region.txt", std::ios_base::out | std::ios_base::app);
            int key = cv::waitKey(100);

            cap >> draw_img;
            cv::waitKey(1);

            std::ostringstream out;
            out.str("");

            draw_lane(draw_img, front_lane, SCALAR_WHITE);
            draw_lane(draw_img, end_lane, SCALAR_WHITE);

            if (draw_region_step == 0) {
                out << "Draw front lane";
                cv::setMouseCallback(winname, front_onMouse, NULL);

                if (key == 'o') {
                    for (int i = 0; i < front_lane.size(); i++) {
                        edit << front_lane[i].x << " " << front_lane[i].y << " ";
                    }
                    edit << std::endl;
                    std::cout << "complete draw front lane" << std::endl;

                    draw_region_step++;
                } else if (key == 'x') {
                    front_lane.clear();
                }

            } else if (draw_region_step == 1) {
                out << "Draw end lane";
                cv::setMouseCallback(winname, end_onMouse, NULL);

                if (key == 'o') {
                    for (int i = 0; i < end_lane.size(); i++) {
                        edit << end_lane[i].x << " " << end_lane[i].y << " ";
                    }
                    draw_region_step++;
                    cv::destroyWindow(winname);
                    break;
                } else if (key == 'x') {
                    end_lane.clear();
                }
            }
            cv::imshow(winname, draw_img);
        }

    } else {
        std::ifstream region_txt("/home/user/jetson-inference/dbict/control/region.txt");
        while (!region_txt.eof()) {

            std::string position;
            getline(region_txt, position);
            std::string *points = new std::string[256];

            points = StringSplit(position, " ");
            length++;


            for (int i = 0; i < sizeof(points) / 2; i++) {
                poly[i * 2] = atoi(points[i * 2].c_str());
                poly[i * 2 + 1] = atoi(points[i * 2 + 1].c_str());
                if (length == 1) {
                    front_lane.push_back(cv::Point(poly[i * 2], poly[i * 2 + 1]));
                } else if (length == 2) {
                    end_lane.push_back(cv::Point(poly[i * 2], poly[i * 2 + 1]));
                }
            }
        }
        region_txt.close();
    }
}


void draw_lane(cv::Mat src, std::vector <cv::Point> vertices, cv::Scalar color) {

    if (vertices.size() > 0) {
        line(src, vertices[0], vertices[1], color, 2);
    }
}


void front_onMouse(int event, int x, int y, int flags, void *userdata) {

    if (event == cv::EVENT_LBUTTONDOWN) {
        front_lane.push_back(cv::Point(x, y));
    }
}


void end_onMouse(int event, int x, int y, int flags, void *userdata) {

    if (event == cv::EVENT_LBUTTONDOWN) {
        end_lane.push_back(cv::Point(x, y));
    }
}

extern std::string *StringSplit(std::string strOrigin, std::string strTok) {
    int cutAt;
    int index = 0;
    std::string *strResult = new std::string[256];

    while ((cutAt = strOrigin.find_first_of(strTok)) != strOrigin.npos) {
        if (cutAt > 0) {
            strResult[index++] = strOrigin.substr(0, cutAt);
        }
        strOrigin = strOrigin.substr(cutAt + 1);
    }
    if (strOrigin.length() > 0) {
        strResult[index++] = strOrigin.substr(0, cutAt);
    }
    return strResult;
}


// extract zero point
bool zero_point_ext(cv::Point begin_point, cv::Point end_point) {

    if (begin_point.x == 0 && begin_point.y == 0) return 0;
    else if (end_point.x == 0 && end_point.y == 0) return 0;
    else return 1;
}

int ccw(cv::Point p1, cv::Point p2, cv::Point p3) {

    int cross_product = (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y);

    if (cross_product > 0) return 1;
    else if (cross_product < 0) return -1;
    else return 0;
}

int comparator(cv::Point left, cv::Point right) {
    int ret;
    if (left.x == right.x) ret = (left.y <= right.y);
    else ret = (left.x <= right.x);
    return ret;
}

void swap_(cv::Point p1, cv::Point p2) {
    cv::Point temp;
    temp = p1;
    p1 = p2;
    p2 = temp;
}

bool LineIntersection(cv::Point x1, cv::Point x2, cv::Point y1, cv::Point y2) {
    int ret;

    int l1_l2 = ccw(x1, x2, y1) * ccw(x1, x2, y2);
    int l2_l1 = ccw(y1, y2, x1) * ccw(y1, y2, x2);
    if (y1.x < 0 || y1.y < 0 || y2.x < 0 || y2.y < 0) {
        // cout << "ret :  0" << endl;
        return false;
    }
    if (l1_l2 == 0 && l2_l1 == 0) {
        if (comparator(x2, x1)) {
            swap(x1, x2);
        }
        if (comparator(y2, y1)) {
            swap(y1, y2);
        }
        ret = (comparator(y1, x2)) && (comparator(x1, y2));
        // cout << "ret : a" << ret <<ret <<ret <<ret <<ret << " " << x1 << x2  << y1  <<y2  << endl ;
    } else {
        ret = (l1_l2 <= 0) && (l2_l1 <= 0);
        // if(ret)
        // cout << "ret : b" << ret <<ret <<ret <<ret <<ret << " " << x1 <<x2  << y1  << y2 << endl;
    }
    return ret;
}


void SendStatusValueInToPixel(Mat &image, std::vector <cv::Point> vertices, unsigned char detected, unsigned char LMB,
                              unsigned char CAN, bool OnSignal, bool OffSignal, unsigned char StdDev) {

    image.at<Vec3b>(0,
                    0)[0] = detected; // Detected Left Turn Signal                    // Blue in BGR  -> [0,0] point pixel
    image.at<Vec3b>(0,
                    0)[1] = LMB;       // On or Off LMB                                // Green in BGR -> [0,0] point pixel
    image.at<Vec3b>(0,
                    0)[2] = CAN;      // On or Off CAN                                // Red in BGR   -> [0,0] point pixel

    /*
     *  Forced On or Off Detect Signal                                                  // Blue in BGR  -> [0,1] point pixel
     */

    if (!OnSignal && !OffSignal) {
        image.at<Vec3b>(0, 1)[0] = 0;
    } else if (OnSignal && !OffSignal) {
        image.at<Vec3b>(0, 1)[0] = 1;
    } else {
        image.at<Vec3b>(0, 1)[0] = 2;
    }


    image.at<Vec3b>(0,1)[1] = StdDev;             // Green in BGR -> [0,1] point pixel
    image.at<Vec3b>(0,1)[2] = 0;                  // Blue in BGR  -> [0,1] point pixel

    image.at<Vec3b>(0, 2)[0] = 0;
    image.at<Vec3b>(0, 2)[1] = 0;
    image.at<Vec3b>(0, 2)[2] = 0;


    image.at<Vec3b>(0, 3)[0] = 0;
    image.at<Vec3b>(0, 3)[1] = 0;
    image.at<Vec3b>(0, 3)[2] = 0;

    for (int i = 0; i <= vertices.size(); i++) {

        if (vertices[i].x > 100) {
            image.at<Vec3b>(0, i * 2 + 10)[0] = vertices[i].x / 100;
            image.at<Vec3b>(0, i * 2 + 10)[1] = (vertices[i].x % 100) / 10;
            image.at<Vec3b>(0, i * 2 + 10)[2] = (vertices[i].x % 100) % 10;

        } else if (100 > vertices[i].x && vertices[i].x >= 10) {
            image.at<Vec3b>(0, i * 2 + 10)[0] = 0;
            image.at<Vec3b>(0, i * 2 + 10)[1] = vertices[i].x / 10;
            image.at<Vec3b>(0, i * 2 + 10)[2] = vertices[i].x % 10;

        } else {
            image.at<Vec3b>(0, i * 2 + 10)[0] = 0;
            image.at<Vec3b>(0, i * 2 + 10)[1] = 0;
            image.at<Vec3b>(0, i * 2 + 10)[2] = vertices[i].x;
        }

        if (vertices[i].y > 100) {
            image.at<Vec3b>(0, i * 2 + 11)[0] = vertices[i].y / 100;
            image.at<Vec3b>(0, i * 2 + 11)[1] = (vertices[i].y % 100) / 10;
            image.at<Vec3b>(0, i * 2 + 11)[2] = (vertices[i].y % 100) % 10;

        } else if (100 > vertices[i].y && vertices[i].y >= 10) {
            image.at<Vec3b>(0, i * 2 + 11)[0] = 0;
            image.at<Vec3b>(0, i * 2 + 11)[1] = vertices[i].y / 10;
            image.at<Vec3b>(0, i * 2 + 11)[2] = vertices[i].y % 10;

        } else {
            image.at<Vec3b>(0, i * 2 + 11)[0] = 0;
            image.at<Vec3b>(0, i * 2 + 11)[1] = 0;
            image.at<Vec3b>(0, i * 2 + 11)[2] = vertices[i].y;
        }

    }


}