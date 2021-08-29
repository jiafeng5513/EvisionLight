#Kalibra:标定

#设置cmake最小版本号
cmake_minimum_required(VERSION 3.13.0)

#设置工程包含当前目录
set(CMAKE_INCLUDE_CURRENT_DIR ON) 

#包含目录
include_directories(${OpenCV_INCLUDE_DIRS})


#查找当前文件夹中的所有源代码文件
FILE(GLOB SRC_FILES "./*.cpp") 
#查找当前文件夹中所有的头文件
FILE(GLOB HEAD_FILES "./*.h") 

#文件整理
source_group("Source Files" FILES ${SRC_FILES})
source_group("Header Files" FILES ${HEAD_FILES})

#创建可执行文件工程
add_executable(Kalibra ${SRC_FILES} ${HEAD_FILES})
target_link_libraries(Kalibra ${OpenCV_LIBS})
