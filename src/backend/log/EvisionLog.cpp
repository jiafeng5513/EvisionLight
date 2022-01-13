//
// Created by Anna on 2022/1/11.
//

#include "EvisionLog.h"
#include "spdlog/spdlog.h"
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/rotating_file_sink.h"
EvisionLog::EvisionLog() {

}

void EvisionLog::init() {
    spdlog::set_level(spdlog::level::debug);
    spdlog::set_automatic_registration(true);
    auto console_logger = spdlog::stdout_color_mt("console");
    auto file_logger = spdlog::rotating_logger_mt("file", "EvisionLight.log", 1048576 * 5, 5);
    spdlog::set_pattern("%^[%l][%H:%M:%S.%e]%$ %v");
//    spdlog::get("console")->info("hello world");
//    spdlog::get("console")->info("hello ni ba ba");
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


extern "C"{
__declspec(dllexport) void EvisionLogInit(){
    EvisionLog::init();
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