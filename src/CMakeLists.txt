#根目录CMAKE
cmake_minimum_required(VERSION 3.13)
project(EvisionLight)
# 启动工程筛选器
SET_PROPERTY(GLOBAL PROPERTY USE_FOLDERS ON)
# 重命名CMake items 筛选器的名字,默认名为:CMakePredefinedTargets
set_property(GLOBAL PROPERTY PREDEFINED_TARGETS_FOLDER "_CMakeTargets")

# Find OpenCV
find_package(OpenCV REQUIRED)
message(STATUS "OpenCV library status:")
message(STATUS "version: ${OpenCV_VERSION}")
message(STATUS "libraries: ${OpenCV_LIBS}")
message(STATUS "include path: ${OpenCV_INCLUDE_DIRS}")

# Find boost
FIND_PACKAGE(Boost REQUIRED COMPONENTS system thread filesystem regex)


# find opengl
find_package(OpenGL)



# 输出路径
# set(CMAKE_STATIC_LINKER_FLAGS_DEBUG  ${PROJECT_SOURCE_DIR}/install/lib/Debug)
# set(CMAKE_STATIC_LINKER_FLAGS_RELEASE ${PROJECT_SOURCE_DIR}/install/lib/Release)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/../install/lib/Debug)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/../install/lib/Release)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/../install/bin/Debug)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/../install/bin/Release)
# set(CMAKE_DEBUG_POSTFIX "_d")
# set_target_properties(${TARGET_NAME} PROPERTIES DEBUG_POSTFIX "_d")

# 定义变量
set(glfw_FOLDER_PATH ${PROJECT_SOURCE_DIR}/../third-party/glfw)
set(gl3w_FOLDER_PATH ${PROJECT_SOURCE_DIR}/../third-party/imgui/examples/libs/gl3w)
set(imgui_FOLDER_PATH ${PROJECT_SOURCE_DIR}/../third-party/imgui)
set(zlib_FOLDER_PATH ${PROJECT_SOURCE_DIR}/../third-party/zlib)
set(fdialog_FOLDER_PATH ${PROJECT_SOURCE_DIR}/../third-party/nativefiledialog)


# 第三方
# glfw : 静态库
# zlib : 静态库
# imgui : 源文件引用
# nativefiledialog : 源文件引用
add_subdirectory(EvisionSandbox)
add_subdirectory(${glfw_FOLDER_PATH} glfw.out)
add_subdirectory(${zlib_FOLDER_PATH} zlib.out)

# 配置工程筛选器
# SET_TARGET_PROPERTIES(EvisionUtils EvisionCamera EvisionParamBridge PROPERTIES FOLDER Utils) 

# =============================================================================================
# if(WIN32)
# ELSEIF (UNIX)
# ENDIF()
# option(ObjectDetection "Object Detection" ON)
# if (ObjectDetection)
#     add_subdirectory(EvisionObjDetection)
#     add_subdirectory(EvisionObjDetectionEngine)
#     SET_TARGET_PROPERTIES(EvisionObjDetectionEngine PROPERTIES FOLDER Algorithm) 
#     SET_TARGET_PROPERTIES(EvisionObjDetection PROPERTIES FOLDER Ai) 
# endif()