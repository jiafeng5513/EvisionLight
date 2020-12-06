#EvisionSandbox:主程序

#设置cmake最小版本号
cmake_minimum_required(VERSION 3.13.0)

#设置工程包含当前目录
set(CMAKE_INCLUDE_CURRENT_DIR ON) 

# 设置使用Boost的静态库
set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_STATIC_RUNTIME ON)

#包含目录
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${gl3w_FOLDER_PATH})
include_directories(${glfw_FOLDER_PATH}/include)
include_directories(${imgui_FOLDER_PATH})
include_directories(${imgui_FOLDER_PATH}/backends)
include_directories(${zlib_FOLDER_PATH})
include_directories(${Boost_INCLUDE_DIR})
include_directories(${fdialog_FOLDER_PATH}/src)
include_directories(${fdialog_FOLDER_PATH}/src/include)

#库目录
link_directories(${Boost_LIBRARY_DIRS})

#预处理器定义
add_definitions( "-DHAS_BOOST" )
add_definitions(-D UNICODE)

# 源代码收集
FILE(GLOB IMGUI "${imgui_FOLDER_PATH}/imconfig.h"
                "${imgui_FOLDER_PATH}/imgui_demo.cpp"
                "${imgui_FOLDER_PATH}/imgui_draw.cpp"
                "${imgui_FOLDER_PATH}/imgui_internal.h"
                "${imgui_FOLDER_PATH}/imgui_widgets.cpp"
                "${imgui_FOLDER_PATH}/imgui.cpp"
                "${imgui_FOLDER_PATH}/imgui.h"                
                "${imgui_FOLDER_PATH}/backends/imgui_impl_glfw.cpp"
                "${imgui_FOLDER_PATH}/backends/imgui_impl_glfw.h"               
                "${imgui_FOLDER_PATH}/backends/imgui_impl_opengl3.cpp"
                "${imgui_FOLDER_PATH}/backends/imgui_impl_opengl3.h"                
                "${imgui_FOLDER_PATH}/misc/natvis/imgui.natvis")
FILE(GLOB GL3W "${gl3w_FOLDER_PATH}/GL/*.h" "${gl3w_FOLDER_PATH}/GL/*.c")
FILE(GLOB FILE_DIALOG "${fdialog_FOLDER_PATH}/src/nfd_common.c"
                      "${fdialog_FOLDER_PATH}/src/nfd_win.cpp" 
                      "${fdialog_FOLDER_PATH}/src/include/*.*")

#查找当前文件夹中的所有源代码文件
FILE(GLOB SRC_FILES "./*.cpp") 
#查找当前文件夹中所有的头文件
FILE(GLOB HEAD_FILES "./*.h") 

#文件整理
source_group("ImGUI" FILES ${IMGUI})
source_group("GL3W" FILES ${GL3W})
source_group("file dialog utils" FILES ${FILE_DIALOG})
source_group("Source Files" FILES ${SRC_FILES})
source_group("Header Files" FILES ${HEAD_FILES})


#创建可执行文件工程
add_executable(EvisionSandbox ${GL3W} ${IMGUI} ${SRC_FILES} ${HEAD_FILES} ${FILE_DIALOG})
target_link_libraries(EvisionSandbox ${OPENGL_gl_LIBRARY})
target_link_libraries(EvisionSandbox ${OpenCV_LIBS})
target_link_libraries(EvisionSandbox Boost::boost Boost::thread)
target_link_libraries(EvisionSandbox ${Boost_LIBRARIES})
target_link_libraries(EvisionSandbox glfw)

# target_link_libraries(EvisionSandbox optimized ${CMAKE_BINARY_DIR}/Release/glfw3.lib)
# target_link_libraries(EvisionSandbox debug ${CMAKE_BINARY_DIR}/Debug/glfw3.lib)
# target_link_libraries(EvisionSandbox optimized ${CMAKE_BINARY_DIR}/Release/zlib.lib)
# target_link_libraries(EvisionSandbox debug ${CMAKE_BINARY_DIR}/Debug/zlib.lib)
