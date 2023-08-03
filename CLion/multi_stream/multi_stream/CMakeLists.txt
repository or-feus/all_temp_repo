cmake_minimum_required(VERSION 2.8)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread -Wno-write-strings -Wno-deprecated-declarations")
project( main )
find_package( OpenCV REQUIRED )
add_definitions(-D__STDC_FORMAT_MACROS)
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( main json.hpp main.cpp MJPEGWriter.cpp MJPEGWriter.h)
target_link_libraries( main ${OpenCV_LIBS} )

#
#if(POLICY CMP0054)
#    cmake_policy(SET CMP0054 NEW)
#endif()
