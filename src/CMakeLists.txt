cmake_minimum_required(VERSION 3.15)
project(EvisionLight)

set(INSTALL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../install")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${INSTALL_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${INSTALL_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${INSTALL_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${INSTALL_DIR})


set(SPDLOG_DIR "${CMAKE_CURRENT_SOURCE_DIR}/3rd/spdlog")

add_subdirectory(3rd/spdlog)
add_subdirectory(backend/log)

add_custom_target(EvisionLight)
add_dependencies(EvisionLight EvisionLog)