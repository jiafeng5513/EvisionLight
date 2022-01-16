//
// Created by Anna on 2022/1/11.
//
#include <chrono>
#include "EvisionLog.h"
#include "spdlog/spdlog.h"
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/rotating_file_sink.h"
EvisionLog::EvisionLog() {

}

void EvisionLog::init(const std::string& filepath) {
    spdlog::set_level(spdlog::level::debug);
    spdlog::set_automatic_registration(true);
    auto console_logger = spdlog::stdout_color_mt("console");
    std::string logFileName = filepath+"/evision-"+getTimeStamp()+".log";
    auto file_logger = spdlog::rotating_logger_mt("file", logFileName, 1048576 * 5, 5);
    spdlog::set_pattern("%^[%l][%H:%M:%S.%e]%$ %v");
}

void EvisionLog::ConsoleLogInfo(const std::string& msg) {
    spdlog::get("console")->info(msg);
}

void EvisionLog::ConsoleLogDebug(const std::string& msg) {
    spdlog::get("console")->debug(msg);
}

void EvisionLog::ConsoleLogWarning(const std::string& msg) {
    spdlog::get("console")->warn(msg);
}

void EvisionLog::ConsoleLogError(const std::string& msg) {
    spdlog::get("console")->error(msg);
}

void EvisionLog::FileLogInfo(const std::string& msg) {
    spdlog::get("file")->info(msg);
}

void EvisionLog::FileLogDebug(const std::string& msg) {
    spdlog::get("file")->debug(msg);
}

void EvisionLog::FileLogWarning(const std::string& msg) {
    spdlog::get("file")->warn(msg);
}

void EvisionLog::FileLogError(const std::string& msg) {
    spdlog::get("file")->error(msg);
}

std::string EvisionLog::getTimeStamp() {
    std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds> tpMicro
       = std::chrono::time_point_cast<std::chrono::microseconds>(std::chrono::system_clock::now());
    time_t totalMicroSeconds = tpMicro.time_since_epoch().count();
    std::chrono::microseconds durMicro = std::chrono::microseconds(totalMicroSeconds);
    tpMicro = std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds>(durMicro);
    time_t timestamp_s = std::chrono::system_clock::to_time_t(tpMicro);
    int micro = (totalMicroSeconds % 1000000);
    tm time;
    gmtime_s(&time, &timestamp_s);

    char szTime[64];
    sprintf_s(szTime, "%04d%02d%02d-%02d%02d%02d-%06d", time.tm_year + 1900, time.tm_mon + 1, time.tm_mday, (time.tm_hour + 8) % 24, time.tm_min, time.tm_sec, micro);
    
    return (szTime);
}


extern "C"{
__declspec(dllexport) void EvisionLogInit(const char* filepath, const int len){
    std::string filepath_str;
    filepath_str.assign(filepath, len);
    EvisionLog::init(filepath_str);
}
__declspec(dllexport) void EvisionConsoleLogInfo(const char* msg, const int len)
{
    std::string msg_str;
    msg_str.assign(msg, len);
    EvisionLog::ConsoleLogInfo(msg_str);
}
__declspec(dllexport) void EvisionConsoleLogDebug(const char* msg, const int len)
{
    std::string msg_str;
    msg_str.assign(msg, len);
    EvisionLog::ConsoleLogDebug(msg_str);
}
__declspec(dllexport) void EvisionConsoleLogWarning(const char* msg, const int len)
{
    std::string msg_str;
    msg_str.assign(msg, len);
    EvisionLog::ConsoleLogWarning(msg_str);
}
__declspec(dllexport) void EvisionConsoleLogError(const char* msg, const int len)
{
    std::string msg_str;
    msg_str.assign(msg, len);
    EvisionLog::ConsoleLogError(msg_str);
}
__declspec(dllexport) void EvisionFileLogInfo(const char* msg, const int len)
{
    std::string msg_str;
    msg_str.assign(msg, len);
    EvisionLog::FileLogInfo(msg_str);
}
__declspec(dllexport) void EvisionFileLogDebug(const char* msg, const int len)
{
    std::string msg_str;
    msg_str.assign(msg, len);
    EvisionLog::FileLogDebug(msg_str);
}
__declspec(dllexport) void EvisionFileLogWarning(const char* msg, const int len)
{
    std::string msg_str;
    msg_str.assign(msg, len);
    EvisionLog::FileLogWarning(msg_str);
}
__declspec(dllexport) void EvisionFileLogError(const char* msg, const int len)
{
    std::string msg_str;
    msg_str.assign(msg, len);
    EvisionLog::FileLogError(msg_str);
}
}