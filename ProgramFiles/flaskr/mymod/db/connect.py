import pyodbc
import sqlite3
import pandas as pd
from werkzeug.exceptions import BadRequest

from ProgramData import DATABASE
from ProgramFiles.flaskr.mymod.log import LOGGER


class HostOnOdbc:
    """ODBC接続クラス"""

    def create_df(self, sql: str) -> pd.DataFrame:
        """データフレーム作成"""
        with pyodbc.connect(
            "DSN=HOST;UID=MINORU1;PWD=;SCH=;CNV=K"
        ) as conn:
            df = pd.read_sql(sql, conn)
        return df


class DataBaseOnSqlite3:
    """SQLite3接続クラス"""

    database = DATABASE

    @property
    def connection(self) -> sqlite3.Connection:
        return sqlite3.connect(
                self.database,
                timeout=8,
                check_same_thread=False
        )

    def create_df(self, sql: str) -> pd.DataFrame:
        """データフレーム作成"""
        with self.connection as conn:
            try:
                df = pd.read_sql(sql, conn)
            except (pd.errors.DatabaseError) as e:
                raise BadRequest(e)
        return df

    def create_list(self, sql: str) -> list:
        """リスト作成"""
        with self.connection as conn:
            results = conn.cursor().execute(sql).fetchall()
            conn.commit()
        return results

    def update_by_sql(self, sql: str) -> None:
        """更新"""
        with self.connection as conn:
            try:
                conn.cursor().execute(sql)
                conn.commit()
            except (sqlite3.OperationalError) as e:
                LOGGER.critical(e)
                raise sqlite3.OperationalError(e)

    def update_by_df(
        self,
        df: pd.DataFrame,
        tablename: str,
        if_exists: str,
        index: bool
    ) -> None:
        """更新"""
        with self.connection as conn:
            df.to_sql(
                name=tablename,
                con=conn,
                if_exists=if_exists,
                index=index)
            conn.commit()
