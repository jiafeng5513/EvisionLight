import os
import time
import logging


class EvisionLog(object):
    def __init__(self):
        pass

    @staticmethod
    def init_logger(log_path):
        log_filename = os.path.join(log_path, "evision_" + time.strftime('%Y%m%d_%H%M%S', time.localtime()) + ".log")
        logging_format = \
            logging.Formatter(fmt="[%(levelname)-9s][%(asctime)s][%(filename)s, line %(lineno)s] %(message)s",
                              datefmt="%Y/%m/%d %H:%M:%S")

        console_logger = logging.getLogger("console")
        console_logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging_format)
        console_logger.addHandler(console_handler)

        file_logger = logging.getLogger("file")
        file_logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(filename=log_filename, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging_format)
        file_logger.addHandler(file_handler)
        pass

    class Console(object):
        def __init__(self):
            pass

        @staticmethod
        def debug(msg):
            logging.getLogger('console').debug(msg)
            pass

        @staticmethod
        def info(msg):
            logging.getLogger('console').info(msg)
            pass

        @staticmethod
        def warning(msg):
            logging.getLogger('console').warning(msg)
            pass

        @staticmethod
        def error(msg):
            logging.getLogger('console').error(msg)
            pass

    class File(object):
        def __init__(self):
            pass

        @staticmethod
        def debug(msg):
            logging.getLogger('file').debug(msg)
            pass

        @staticmethod
        def info(msg):
            logging.getLogger('file').info(msg)
            pass

        @staticmethod
        def warning(msg):
            logging.getLogger('file').warning(msg)
            pass

        @staticmethod
        def error(msg):
            logging.getLogger('file').error(msg)
            pass

    class All(object):
        def __init__(self):
            pass

        @staticmethod
        def debug(msg):
            logging.getLogger('file').debug(msg)
            logging.getLogger('console').debug(msg)
            pass

        @staticmethod
        def info(msg):
            logging.getLogger('file').info(msg)
            logging.getLogger('console').info(msg)
            pass

        @staticmethod
        def warning(msg):
            logging.getLogger('file').warning(msg)
            logging.getLogger('console').warning(msg)
            pass

        @staticmethod
        def error(msg):
            logging.getLogger('file').error(msg)
            logging.getLogger('console').error(msg)
            pass


# this is a test case
if __name__ == '__main__':
    EvisionLog.init_logger('D:/WorkSpace/jiafeng_projects/EvisionLight')
    EvisionLog.Console.debug(r"调试调试")
    EvisionLog.Console.info("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    EvisionLog.Console.warning("调试信息")
    EvisionLog.Console.error("调试信息")

    EvisionLog.File.debug("调试调试")
    EvisionLog.File.info("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    EvisionLog.File.warning("调试信息")
    EvisionLog.File.error("调试信息")

