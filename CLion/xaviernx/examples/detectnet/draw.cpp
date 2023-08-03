#include "function.hpp"

cv::Mat img;
std::vector<cv::Point> front_lane;
std::vector<cv::Point> end_lane;


void draw_lane(cv::Mat src,std::vector<cv::Point> vertices, cv::Scalar color){

    if (vertices.size()>0) {
        line( src, vertices[0],  vertices[1], color, 2);
    }
}

bool DoesROIOverlap( cv::Rect boundingbox,std::vector<cv::Point> contour, std::string &res) {

    //Get the corner points.

    const cv::Point *pts = (const cv::Point*) cv::Mat(contour).data;
    int npts = cv::Mat(contour).rows;
    double C_area =cv::contourArea(contour);

    int xCenter = boundingbox.x+(boundingbox.width/2);
    int yCenter = boundingbox.y+(boundingbox.height/2);
    float AR =(float)boundingbox.width/(float)boundingbox.height;

    int IntersectionArea = 0;

    int xmin = boundingbox.x;
    int xmax = boundingbox.x+(boundingbox.width);
    int ymin = boundingbox.y;
    int ymax = boundingbox.y+(boundingbox.height);



    for(float x=xmin; x<xmax;x++){
        for(float y=ymin; y<ymax;y++){
            if(cv::pointPolygonTest(cv::Mat(contour), cv::Point2f(x,y), true) > 0)
                IntersectionArea++;
        }
    }
    int ratio = 100*IntersectionArea/boundingbox.area();

    int ratio_poly = 100*IntersectionArea/(int)C_area;
    if(boundingbox.area() > C_area*0.8){
        if(cv::pointPolygonTest(cv::Mat(contour), cv::Point2f(xCenter,yCenter), true) > 0){
            if(ratio > 40){
                res =  "Big!" ;
                return true;
            }
        }
    }
    if(ratio > 50){
        if(cv::pointPolygonTest(cv::Mat(contour), cv::Point2f(xCenter,yCenter), true) > 0){
            res =" ratio: "+std::to_string(C_area)+" ratio:"+std::to_string(ratio_poly) +"% size:"+std::to_string(boundingbox.area())+" intersect:"+std::to_string(IntersectionArea)+" ratio: "+std::to_string(ratio)+"%";
            return true;
        }
    }else{
        return false;
    }
}


int DoesROIOverlapCount( cv::Rect boundingbox,int lanes, int &det_line, int &id) {
    /// object bounding box point ///
    int xCenter = boundingbox.x+(boundingbox.width/2);
    int yCenter = boundingbox.y+(boundingbox.height/2);
    float AR =(float)boundingbox.width/(float)boundingbox.height;

    int IntersectionArea[lanes] = {0,};
    double lanes_area[lanes] = {0,};
    double polytest[lanes] = {0,} ;
    int ratio[lanes] = {0,};

    lanes_area[0] = {cv::contourArea(front_lane)};
    lanes_area[1] = {cv::contourArea(end_lane)};

    int xmin = boundingbox.x;
    int xmax = boundingbox.x+(boundingbox.width);
    int ymin = boundingbox.y;
    int ymax = boundingbox.y+(boundingbox.height);

    // for(float x=xmin; x<xmax;x++){
    // 	for(float y=ymin; y<ymax;y++){
    // 		for(int j=0; j < lanes; j++){
    // 			if(cv::pointPolygonTest(cv::Mat(RoiVtx[j]), cv::Point2f(xCenter,yCenter), true) > 0){
    // 				IntersectionArea[j]++;
    // 			}
    // 		}
    // 	}
    // }


    // int lane = 0;
    // for(int n=0; n < lanes ; n ++){
    // 	ratio[n] = 100 * IntersectionArea[n] / boundingbox.area();
    // 	if(boundingbox.area() > lanes_area[n] * 0.8  && ratio[n] > 40 && cv::pointPolygonTest(cv::Mat(RoiVtx[n]), cv::Point2f(xCenter,yCenter), true) > 0){
    // 		det_line =  n+1;
    // 		id = objectID;
    // 		// cout << n+1 << " DET lane IntersectionArea : " << pointPolygonTest(Mat(RoiVt[n]), Point2f(xCenter,yCenter), true) << "     ratio : " << ratio[n]  << " // " << boundingbox.area()<< " // "<< lanes_area[n] <<endl ;
    // 	}else if(ratio[n] > 50  && (cv::pointPolygonTest(cv::Mat(RoiVtx[n]), cv::Point2f(xCenter,yCenter), true) > 0)){
    // 		det_line =  n+1;
    // 		id = objectID;
    // 		// cout << n+1 << " DET lane IntersectionArea : " << pointPolygonTest(Mat(RoiVt[n]), Point2f(xCenter,yCenter), true) << "     ratio : " << ratio[n] << " // " << boundingbox.area()<< " // "<< lanes_area[n] << endl ;
    // 	}else{
    // 		// det_line = 0;
    // 		// cout << n+1 << " NOT lane IntersectionArea : " << pointPolygonTest(Mat(RoiVt[n]), Point2f(xCenter,yCenter), true) << "     ratio : " << ratio[n] << " // " << boundingbox.area()<< " // "<< lanes_area[n] <<endl ;
    // 	}
    // 	// cout << n+1 << "  lane IntersectionArea : " << IntersectionArea[n] << "     ratio : " << ratio[n] << endl ;
    // 	// return det_line;
    // }
}

void front_onMouse(int event, int x, int y, int flags, void *userdata){

    if(event == cv::EVENT_LBUTTONDOWN){
        front_lane.push_back(cv::Point(x, y));
    }
}


void end_onMouse(int event, int x, int y, int flags, void *userdata){

    if(event == cv::EVENT_LBUTTONDOWN){
        end_lane.push_back(cv::Point(x, y));
    }
}

extern std::string* StringSplit(std::string strOrigin, std::string strTok){
    int cutAt;
    int index = 0;
    std::string *strResult = new std::string[256];

    while((cutAt = strOrigin.find_first_of(strTok)) != strOrigin.npos){
        if(cutAt > 0){
            strResult[index++] = strOrigin.substr(0, cutAt);
        }
        strOrigin = strOrigin.substr(cutAt+1);
    }
    if(strOrigin.length()>0){
        strResult[index++] = strOrigin.substr(0, cutAt);
    }
    return strResult;
}

bool zero_point_ext(cv::Point begin_point, cv::Point end_point){

    if(begin_point.x == 0 && begin_point.y == 0){
        return 0;
    }else if(end_point.x == 0 && end_point.y == 0){
        return 0;
    }else{
        return 1;
    }
}

int ccw(cv::Point p1, cv::Point p2, cv::Point p3){

    int cross_product = (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y);

    if(cross_product > 0){
        return 1;
    }else if( cross_product < 0){
        return -1;
    }else{
        return 0;
    }
}
int comparator(cv::Point left, cv::Point right){
    int ret;
    if(left.x == right.x){
        ret = (left.y <= right.y);
    }else{
        ret = (left.x <= right.x);
    }
    return ret;
}
void swap_(cv::Point p1, cv::Point p2){
    cv::Point temp;
    temp = p1;
    p1 = p2;
    p2 = temp;
}
bool LineIntersection(cv::Point x1, cv::Point x2, cv::Point y1, cv::Point y2){
    int ret;

    int l1_l2 = ccw(x1, x2, y1) * ccw(x1, x2, y2);
    int l2_l1 = ccw(y1, y2, x1) * ccw(y1, y2, x2);
    if(y1.x < 0 || y1.y < 0 || y2.x < 0 || y2.y < 0){
        // cout << "ret :  0" << endl;
        return false;
    }
    if(l1_l2 == 0 && l2_l1 == 0){
        if(comparator(x2, x1)){
            swap(x1, x2);
        }
        if(comparator(y2, y1)){
            swap(y1, y2);
        }
        ret = (comparator(y1, x2)) && (comparator(x1,y2));
        // cout << "ret : a" << ret <<ret <<ret <<ret <<ret << " " << x1 << x2  << y1  <<y2  << endl ;
    }else{
        ret = (l1_l2 <= 0) && (l2_l1 <= 0);
        // if(ret)
        // cout << "ret : b" << ret <<ret <<ret <<ret <<ret << " " << x1 <<x2  << y1  << y2 << endl;
    }
    return ret;
}

