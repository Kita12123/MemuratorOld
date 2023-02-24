import re

from ProgramFiles.flaskr import app
from ProgramFiles.flaskr.mymod.log import LOGGER
from ProgramFiles.flaskr.mymod.sql_code._type import ColumnType


def to_sign_value(x_: str, /) -> tuple[str, str]:
    """値と記号に分ける"""
    x = re.sub("[,|&]", "", x_)
    if x[:2] in ("<=", ">=", "<>"):
        return x[:2], x[2:]
    elif x[:1] in ("<", ">", "="):
        return x[:1], x[1:]
    return "=", x


def tokcd(name: str, sign: str, value: str):
    """得意先コード４ｹﾀ未満を補正する"""
    z = '0'*(4 - len(value))
    if sign == "=":
        return f"({name}>={z}{value}00 AND {name}<={z}{value}99)"
    elif sign[0] == ">":
        return f"{name}{sign}{z}{value}00"
    elif sign[0] == "<":
        return f"{name}{sign}{z}{value}99"
    else:
        return f"{name}{sign}{value}"


def seibucd(name: str, sign: str, value: str):
    """製品部品コード５ｹﾀ未満を補正する"""
    z = '0'*(5 - len(value))
    if sign == "=":
        return f"({name}>={z}{value}00 AND {name}<={z}{value}99)"
    elif sign[0] == ">":
        return f"{name}{sign}{z}{value}00"
    elif sign[0] == "<":
        return f"{name}{sign}{z}{value}99"
    else:
        return f"{name}{sign}{value}"


def to_sql(name: str, type_: ColumnType, sign: str, value: str, /) -> str:
    if type_.istokcd():
        if len(value) <= 4:
            return tokcd(name, sign, value)
        else:
            return f"{name}{sign}{value}"
    elif type_.isseibucd():
        if len(value) <= 5:
            return seibucd(name, sign, value)
        else:
            return f"{name}{sign}{value}"
    elif type_.isnum():
        return f"{name}{sign}{value}"
    elif type_.isdate():
        return f"{name}{sign}{int(value) - 19500000}"
    elif type_.isstr():
        if sign == "=":
            return f"{name} LIKE'%{value}%'"
        elif sign == "<>":
            return f"{name} NOT LIKE'%{value}%'"
        return f"{name}{sign}'{value}'"
    raise TypeError("ColumnTypeクラス以外を指定しています!!")


def main_(name: str, type_: ColumnType, value_: str, /):
    if app.debug:
        LOGGER.debug(
            f"to_where.main_\nname: {name}, type: {type_}, value: {value_}"
        )
    value = value_.replace(" ", "").replace("　", "")
    if type(type_) is not ColumnType:
        raise TypeError("class ColumnTypeを指定してください")
    if not name or not value:
        raise ValueError(f"引数が不足しています。name: {name}, value: {value}")
    while value[0] in [",", "|", "&"]:
        value = value[1:]
    # Markがないとき
    if not any(x in value for x in (",", "|", "&")):
        return to_sql(name, type_, *to_sign_value(value))

    values = re.split("(?=[,|&])", value)
    result = ""
    for v_ in values:
        if not re.sub("[,|&<=>]", "", v_) and not type_.isstr():
            continue
        result += " " + v_.replace(
            re.sub("[,|&]", "", v_),
            " " + to_sql(name, type_, *to_sign_value(v_))
        )
    return re.sub("[,|]", "OR", result).replace("&", "AND")
