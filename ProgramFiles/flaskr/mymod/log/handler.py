"""
ログハンドラー
"""
from logging import (
    StreamHandler,
    Formatter,
    FileHandler,
    DEBUG,
    INFO,
    WARNING,
    CRITICAL
)

from ProgramData import DEBUG_LOG, INFO_LOG, WARNING_LOG, CRITICAL_LOG



class Handler:

    def __init__(self):
        self.formater = Formatter("[%(levelname)s]%(asctime)s-%(message)s")

    @property
    def default(self) -> StreamHandler:
        """Terminal"""
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(self.formater)
        return handler

    @property
    def debug_file(self) -> FileHandler:
        """Output debug.txt"""
        handler = FileHandler(
            DEBUG_LOG,
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(DEBUG)
        handler.setFormatter(self.formater)
        return handler

    @property
    def info_file(self) -> FileHandler:
        """Output info.txt"""
        handler = FileHandler(
            INFO_LOG,
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(INFO)
        handler.setFormatter(self.formater)
        return handler

    @property
    def warning_file(self) -> FileHandler:
        """Output warning.txt"""
        handler = FileHandler(
            WARNING_LOG,
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(WARNING)
        handler.setFormatter(self.formater)
        return handler

    @property
    def critical_file(self) -> FileHandler:
        """Output critical.txt"""
        handler = FileHandler(
            CRITICAL_LOG,
            mode="a",
            encoding="utf-8"
        )
        handler.setLevel(CRITICAL)
        handler.setFormatter(self.formater)
        return handler
