

class ColumnType:

    def __init__(self, arg):
        self.arg = arg

    def isnum(self) -> bool:
        return self.arg == "num"

    def isstr(self) -> bool:
        return self.arg == "str"

    def isdate(self) -> bool:
        return self.arg == "date"

    def istokcd(self) -> bool:
        return self.arg == "tokcd"

    def isseibucd(self) -> bool:
        return self.arg == "seibucd"


NUM = ColumnType("num")
STR = ColumnType("str")
DATE = ColumnType("date")
TOKCD = ColumnType("tokcd")
SEIBUCD = ColumnType("seibucd")
