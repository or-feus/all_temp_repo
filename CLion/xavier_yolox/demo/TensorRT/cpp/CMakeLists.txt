cmake_minimum_required(VERSION 2.6)

project(yolox)

add_definitions(-std=c++17)

option(CUDA_USE_STATIC_CUDA_RUNTIME OFF)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE Debug)

find_package(CUDA REQUIRED)

include_directories(${PROJECT_SOURCE_DIR}/include)
# include and link dirs of cuda and tensorrt, you need adapt them if yours are different
# cuda
include_directories(/usr/local/cuda/include)
link_directories(/usr/local/cuda/lib64)
# tensorrt
include_directories(/usr/include/aarch64-linux-gnu)
link_directories(/usr/lib/aarch64-linux-gnu)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -Wall -pthread -Ofast -Wfatal-errors -D_MWAITXINTRIN_H_INCLUDED")


FIND_PACKAGE(Boost COMPONENTS log system filesystem REQUIRED)
include_directories(${Boost_INCLUDE_DIR})

find_package(OpenCV)
include_directories(${OpenCV_INCLUDE_DIRS})

file(GLOB sources utils/*.cpp yolox.cpp)

add_executable(yolox ${PROJECT_SOURCE_DIR}/yolox.cpp ${sources})
target_link_libraries(yolox nvinfer)
target_link_libraries(yolox cudart)
target_link_libraries(yolox ${OpenCV_LIBS})

add_definitions(-O2 -pthread)

