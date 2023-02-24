"""
統計用モジュール
"""
import pandas as pd

from ProgramFiles.flaskr import app
from ProgramFiles.flaskr.mymod.log import LOGGER


#
# Sub Function
#
def year_to_period(date):
    date = str(date)
    if len(date) != 8:
        return "0"
    else:
        return int(date[0:4]) + int(date[4:5]) - 1945


#
# Main Function
#
def arrage_df(df: pd.DataFrame) -> list[pd.DataFrame]:
    if app.debug:
        LOGGER.debug(df.head(3))
    if df.empty:
        return (
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]))
    columns_totall = [
        c for c in df.columns
        if any([x in c for x in ["数量", "金額"]])
    ]
    df = df[["伝票日付", *columns_totall]].copy()
    df1 = df.copy()
    df1.loc[:, "期"] = df1["伝票日付"].map(year_to_period)
    df1 = df1[["期", *columns_totall]].groupby("期").sum()
    df1.insert(0, "期", value=df1.index)
    df1.loc[:, columns_totall] = df1[columns_totall].applymap("{:,}".format)
    # Create Index
    df.loc[:, "伝票日付"] = pd.to_datetime(
        df["伝票日付"], format=r"%Y%m%d", errors="coerce"
    )
    df.set_index("伝票日付", inplace=True)
    # Month
    try:
        df2 = df.copy().groupby(pd.Grouper(freq="1M")).sum()
    except (AttributeError):  # 'NatType object has no attribute 'normalize'
        return (
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]))
    df2.insert(0, "伝票日付", value=df2.index)
    df2.loc[:, "伝票日付"] = df2["伝票日付"].dt.strftime(r"%Y/%m")
    df2.loc[:, columns_totall] = df2[columns_totall].applymap("{:,}".format)
    # Day
    df3 = df.copy().groupby(pd.Grouper(freq="1D")).sum()
    df3.insert(0, "伝票日付", value=df3.index)
    df3.loc[:, "伝票日付"] = df3["伝票日付"].dt.strftime(r"%Y/%m/%d")
    df3.loc[:, columns_totall] = df3[columns_totall].applymap("{:,}".format)
    return df1, df2, df3
