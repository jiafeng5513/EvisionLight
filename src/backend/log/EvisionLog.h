//
// Created by Anna on 2022/1/11.
//

#ifndef EVISIONLIGHT_EVISIONLOG_H
#define EVISIONLIGHT_EVISIONLOG_H
#include <string>

class EvisionLog {
    EvisionLog();
    static void init();

    static void ConsoleLogInfo(const std::string msg);
    static void ConsoleLogDebug(const std::string msg);
    static void ConsoleLogWarning(const std::string msg);
    static void ConsoleLogError(const std::string msg);

    static void FileLogInfo(const std::string msg);
    static void FileLogDebug(const std::string msg);
    static void FileLogWarning(const std::string msg);
    static void FileLogError(const std::string msg);
};


#endif //EVISIONLIGHT_EVISIONLOG_H
