cmake_minimum_required(VERSION 2.8)
project( DisplayImage )
include_directories(include)
find_package( OpenCV REQUIRED )
add_executable( DisplayImage DisplayImage.cpp alg_conv.cpp)
target_link_libraries( DisplayImage ${OpenCV_LIBS} )

