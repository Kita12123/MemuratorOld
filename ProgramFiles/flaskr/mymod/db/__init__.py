"""
Database Package
"""
from datetime import datetime

from ProgramFiles.flaskr.mymod.log import LOGGER
from ProgramFiles.flaskr.mymod.db import connect
from ProgramFiles.flaskr.mymod.db.host import host, HostFile
from ProgramFiles.flaskr.mymod.system import system

#
# Initializing
#
odbc = connect.HostOnOdbc()
sql = connect.DataBaseOnSqlite3()


class SyncHost:

    def __init__(self):
        for h in host.files:
            sql.update_by_sql(h.sql_create_table)

    def _refresh(
        self,
        h: HostFile, /, *,
        where_sqlite3: str = "1=1"
    ) -> None:
        # HOST -> df
        LOGGER.info(f"Syncing {h.file_name}.{h.lib_name} ({where_sqlite3}) ...")
        where_host = h.to_where_host_by(where_sqlite3)
        df = odbc.create_df(sql=h.select_host_where(where_host))
        # df -> SQLite3
        # すべて更新するときは、テーブルを再作成する
        # if where_sqlite3 == "1=1":
        #     sql.update_by_sql(h.sql_deleate_table)
        #     sql.update_by_sql(h.sql_create_table)
        # else:
        sql.update_by_sql(sql=h.deleate_sqlite3_where(where_sqlite3))
        sql.update_by_df(
            df=df,
            tablename=h.table_name,
            if_exists="append",
            index=False
        )

    def refresh_all(
        self, *,
        first_date: str,
        last_date: str,
        contain_master: bool
    ):
        system.last_refresh_date = "更新中"
        LOGGER.info(f"{' Start Connect DataBase ':*^60}")
        first_host = int(first_date) - 19500000
        last_host = int(last_date) - 19500000
        for d in host.data_files:
            self._refresh(
                d,
                where_sqlite3=f"伝票日付>={first_host} AND 伝票日付<={last_host}"
            )
        if contain_master:
            for m in host.master_files:
                self._refresh(m)
        LOGGER.info(f"{' Finish Connect DataBase ':*^60}")
        system.last_refresh_date = datetime.now().strftime(r"%Y/%m/%d %H時%M分%S秒")


sync = SyncHost()