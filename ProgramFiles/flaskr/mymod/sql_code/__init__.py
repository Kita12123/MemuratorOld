import os

from ProgramFiles.flaskr.mymod.log import LOGGER
from ProgramFiles.flaskr.mymod.sql_code._type import (
    ColumnType, NUM, STR, DATE, TOKCD, SEIBUCD
)
from ProgramFiles.flaskr.mymod.sql_code.to_where import main_

CD = os.path.dirname(__file__)
DOWNLOAD_DIR = os.path.join(CD, "download")
DISPLAY_DIR = os.path.join(CD, "display")
MARK_USERFORM = "\n\n/*" + "-"*50 + "入力フォーム範囲" + "-"*50 + "*/\n\n"


class DataBase:

    def __init__(
        self,
        sql_filename: str,
        column_type_dic: dict[str, ColumnType], /
    ):
        self.sql_filename = sql_filename
        self.column_type_dic = column_type_dic

    @property
    def columns(self):
        return tuple(self.column_type_dic.keys())

    @property
    def sql_display(self):
        display_file = os.path.join(DISPLAY_DIR, self.sql_filename+".txt")
        with open(display_file, mode="r", encoding="utf-8") as f:
            return f.read()

    @property
    def sql_download(self):
        download_file = os.path.join(DOWNLOAD_DIR, self.sql_filename+".txt")
        with open(download_file, mode="r", encoding="utf-8") as f:
            return f.read()

    def to_sql_display(self, **kwargs: str):
        lis = [
            main_(k, self.column_type_dic[k], v) for k, v in kwargs.items()
            if k in self.columns and v.replace(" ", "")
        ]
        LOGGER.debug(f"""DataBase.to_sql_display
        Filename: {self.sql_filename}, WHERE list: {lis}""")
        if lis:
            where = " AND ".join([f"( {a} )\n" for a in lis])
        else:
            where = "1=1"
        return self.sql_display.format(MARK_USERFORM + where + MARK_USERFORM)

    def to_sql_download(self, **kwargs: str):
        lis = [
            main_(k, self.column_type_dic[k], v) for k, v in kwargs.items()
            if k in self.columns and v.replace(" ", "")
        ]
        if lis:
            where = " AND ".join([f"( {a} )\n" for a in lis])
        else:
            where = "1=1"
        return self.sql_download.format(MARK_USERFORM + where + MARK_USERFORM)


class DataBaseDictionary:

    dic: dict[str, DataBase] = {}

    def add(
        self, *,
        name: str,
        sql_filename: str,
        column_dic: dict[str, ColumnType]
    ):
        for v in column_dic.values():
            if type(v) is not ColumnType:
                raise TypeError("ColumnTypeクラス以外を指定しています!!")
        self.dic[name] = DataBase(sql_filename, column_dic)

    def load(self, name: str, /) -> DataBase:
        return self.dic[name]


DB = DataBaseDictionary()

DB.add(
    name="売上データ",
    sql_filename="売上データ",
    column_dic={
        "伝票日付": DATE,
        "伝票区分": NUM,
        "伝票区分名＊": STR,
        "扱い区分名＊": STR,
        "運送会社名＊": STR,
        "委託区分名＊": STR,
        "担当者コード": NUM,
        "担当者名＊": STR,
        "得意先コード": TOKCD,
        "得意先カナ": STR,
        "雑コード": NUM,
        "雑カナ": NUM,
        "送荷先コード": NUM,
        "製品部品コード": SEIBUCD,
        "製品部品カナ": STR,
        "級区分": NUM,
        "数量": NUM,
        "単価": NUM,
        "金額": NUM,
        "出荷伝票番号": STR,
        "備考": STR
    }
)

DB.add(
    name="出荷データ",
    sql_filename="出荷データ",
    column_dic={
        "伝票日付": DATE,
        "伝票区分": NUM,
        "伝票区分名＊": STR,
        "扱い区分名＊": STR,
        "運送会社名＊": STR,
        "委託区分名＊": STR,
        "担当者コード": NUM,
        "担当者名＊": STR,
        "得意先コード": TOKCD,
        "得意先カナ": STR,
        "雑コード": NUM,
        "雑カナ": NUM,
        "送荷先コード": NUM,
        "製品部品コード": SEIBUCD,
        "製品部品カナ": STR,
        "級区分": NUM,
        "数量": NUM,
        "単価": NUM,
        "金額": NUM,
        "出荷伝票番号": STR,
        "備考": STR
    }
)

DB.add(
    name="出荷データ（九州）",
    sql_filename="出荷データ（九州）",
    column_dic={
        "伝票日付": DATE,
        "伝票区分": NUM,
        "伝票区分名＊": STR,
        "扱い区分名＊": STR,
        "運送会社名＊": STR,
        "委託区分名＊": STR,
        "担当者コード": NUM,
        "担当者名＊": STR,
        "得意先コード": TOKCD,
        "得意先カナ": STR,
        "雑コード": NUM,
        "雑カナ": NUM,
        "送荷先コード": NUM,
        "製品部品コード": SEIBUCD,
        "製品部品カナ": STR,
        "級区分": NUM,
        "数量": NUM,
        "単価": NUM,
        "金額": NUM,
        "出荷伝票番号": STR,
        "備考": STR
    }
)

DB.add(
    name="出荷データ（長野）",
    sql_filename="出荷データ（長野）",
    column_dic={
        "伝票日付": DATE,
        "伝票区分": NUM,
        "伝票区分名＊": STR,
        "扱い区分名＊": STR,
        "運送会社名＊": STR,
        "委託区分名＊": STR,
        "担当者コード": NUM,
        "担当者名＊": STR,
        "得意先コード": TOKCD,
        "得意先カナ": STR,
        "雑コード": NUM,
        "雑カナ": NUM,
        "送荷先コード": NUM,
        "製品部品コード": SEIBUCD,
        "製品部品カナ": STR,
        "級区分": NUM,
        "数量": NUM,
        "単価": NUM,
        "金額": NUM,
        "出荷伝票番号": STR,
        "備考": STR
    }
)

DB.add(
    name="伝票区分マスタ",
    sql_filename="伝票区分マスタ",
    column_dic={
        "伝票区分": NUM,
        "名称": STR,
        "カナ名": STR
    }
)

DB.add(
    name="担当者マスタ",
    sql_filename="担当者マスタ",
    column_dic={
        "担当者コード": NUM,
        "名称": STR,
        "カナ名": STR
    }
)

DB.add(
    name="得意先マスタ",
    sql_filename="得意先マスタ",
    column_dic={
        "得意先コード": TOKCD,
        "カナ名": STR,
        "名称": STR,
        "担当者コード": NUM,
        "担当者名": STR,
        "郵便番号": STR,
        "住所": STR,
        "電話番号": STR,
        "締め日": NUM,
        "ＬＥＳＳ率": NUM,
        "作成日": DATE
    }
)

DB.add(
    name="送荷先マスタ",
    sql_filename="送荷先マスタ",
    column_dic={
        "送荷先コード": NUM,
        "カナ名": STR,
        "名称": STR,
        "郵便番号": STR,
        "住所": STR,
        "電話番号": STR
    }
)

DB.add(
    name="雑マスタ",
    sql_filename="雑マスタ",
    column_dic={
        "雑コード": NUM,
        "カナ名": STR,
        "名称": STR,
        "郵便番号": STR,
        "住所": STR,
        "電話番号": STR
    }
)

DB.add(
    name="製品部品マスタ",
    sql_filename="製品部品マスタ",
    column_dic={
        "製品部品コード": SEIBUCD,
        "カナ名": STR,
        "部番": STR,
        "旧小売単価": NUM,
        "小売単価": NUM,
        "原価": NUM,
        "重量": NUM,
        "廃止区分": STR,
        "作成日": DATE
    }
)

DB.add(
    name="仕入データ",
    sql_filename="仕入データ",
    column_dic={
        "伝票日付": DATE,
        "納期": STR,
        "仕入先コード": NUM,
        "仕入先カナ": STR,
        "仕入先名": STR,
        "発注区分": STR,
        "品目コード": STR,
        "品目カナ": NUM,
        "品目仕様＊": STR,
        "品目図番＊": STR,
        "数量": NUM,
        "材料単価": NUM,
        "材料金額": NUM,
        "加工単価": NUM,
        "加工金額": NUM,
        "機種コード": NUM,
        "機種カナ": STR,
        "伝票番号": NUM
    }
)

DB.add(
    name="定期注文データ",
    sql_filename="定期注文データ",
    column_dic={
        "手配先名": STR,
        "納期": NUM,
        "注文区分": STR,
        "発注区分": STR,
        "品目コード": STR,
        "品目カナ": STR,
        "仕様": STR,
        "図番": STR,
        "数量": NUM,
        "材料単価": NUM,
        "加工単価": NUM,
        "納入場所": STR,
        "納品書番号": NUM,
        "注文番号": NUM
    }
)

DB.add(
    name="手配先マスタ",
    sql_filename="手配先マスタ",
    column_dic={
        "手配先コード": NUM,
        "名称": STR,
        "略称": STR
    }
)

DB.add(
    name="品目マスタ",
    sql_filename="品目マスタ",
    column_dic={
        "品目コード": STR,
        "カナ名": STR,
        "名称": STR,
        "仕様": STR,
        "図番": STR,
        "部番": STR,
        "資材単価": NUM,
        "加工単価": NUM,
        "手配先コード": NUM,
        "納入先コード": NUM,
        "検査区分": NUM,
        "変更日": DATE,
        "作成日": DATE
    }
)
