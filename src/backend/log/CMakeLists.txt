cmake_minimum_required(VERSION 3.15)
project(EvisionLib)

FILE(GLOB SRC_FILES "*.cpp")
FILE(GLOB HEADER_FILES "*.h")

include_directories(${SPDLOG_DIR}/include)

add_library(${PROJECT_NAME} ${SRC_FILES} ${HEADER_FILES})
target_link_libraries(${PROJECT_NAME} spdlog)