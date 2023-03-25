"""
FLASK Main
"""
import os
import traceback
from flask import (
    redirect,
    render_template,
    send_file,
    request,
    send_from_directory,
)
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ProgramData import TEMP_CSV
from ProgramFiles.flaskr.mymod.log import LOGGER
from ProgramFiles.flaskr.mymod import db
from ProgramFiles.flaskr.mymod.db import sync, host
from ProgramFiles.flaskr.mymod.df import arrage_df
from ProgramFiles.flaskr.mymod.system import system
from ProgramFiles.flaskr.mymod.req import req
from ProgramFiles.flaskr import app, scheduler


@scheduler.task("interval", id="refresh_db", seconds=1*60*60)
def schedule_fuction():
    now_time = datetime.now()
    if now_time.strftime(r"%H") in ["08", "10", "12", "14", "16", "18"]:
        last_month = datetime.today() - relativedelta(months=1)
        sync.refresh_all(
            first_date=last_month.strftime(r"%Y%m00"),
            last_date=str(999999 + 19500000),
            contain_master=True,
            table_name="すべて"
        )


@app.route("/", methods=["GET"])
def index():
    user = system.load(request.remote_addr)
    return render_template(
        "index.html",
        MyColor=user.mycolor,
        Department=user.department,
        LastRefreshDate=system.last_refresh_date,
        user_form=user.form.to_dict(),
    )


@app.route("/show_sql", methods=["GET"])
def show_sql():
    user = system.load(request.remote_addr)
    sql_display = user.form.to_sql(
        download=False
    ).replace(" ", "&emsp;").replace("\n", "<br>")
    sql_download = user.form.to_sql(
        download=True
    ).replace(" ", "&emsp;").replace("\n", "<br>")
    return render_template(
        "show_sql.html",
        MyColor=user.mycolor,
        sql_display=sql_display,
        sql_download=sql_download
    )


@app.route("/show_table", methods=["POST"])
def show_table():
    user = system.load(request.remote_addr)
    user.form.update(**req.form_to_query())
    # Create DataFrame on sqlite3
    df = db.sql.create_df(sql=user.form.to_sql(download=False))
    # Message
    messages = []
    count = len(df)
    if count >= user.max_rows:
        messages.append(f"件数：{count:,} ({user.max_rows})")
    else:
        messages.append(f"件数：{count:,}")
    # Arrange DataFrame
    df1, df2, df3 = arrage_df(df=df)
    columns_sum = [
        c for c in df.columns
        if any([x in c for x in ["数量", "金額"]])
    ]
    for t_c in columns_sum:
        messages.append(f"合計{t_c} : {df[t_c].sum():,}")
    columns_num = [
        c for c in df.columns
        if any([x in c for x in ["数量", "単価", "金額"]])
    ]
    df_dsp = df.head(user.max_rows)
    df_dsp.loc[:, columns_num] = (
        df_dsp[columns_num].applymap("{:,}".format)
    )
    if app.debug:
        LOGGER.debug(
            f"main.show_table\nuser.form.todict(): {user.form.to_dict()}"
        )
    return render_template(
        "show_table.html",
        MyColor=user.mycolor,
        Department=user.department,
        LastRefreshDate=system.last_refresh_date,
        user_form=user.form.to_dict(),
        messages=messages,
        headers=df_dsp.columns,
        records=df_dsp.values.tolist(),
        headers1=df1.columns,
        records1=df1.values.tolist(),
        headers2=df2.columns,
        records2=df2.values.tolist(),
        headers3=df3.columns,
        records3=df3.values.tolist(),
    )


@app.route("/search/<column>", methods=["POST"])
def search(column):
    user = system.load(request.remote_addr)
    # 抽出条件QUERYに反映させる -> "/"へ
    if request.form.get("ok") == "決定":
        user.form.update(
            **{column: ",".join(request.form.getlist("key_code"))}
        )
        return redirect("/")
    # user_dic, master_query作成
    if "DB_name" in req.form_to_dict():
        # ここのQUERYを保存するかしないかの判定がむずかしい
        # indexからきた場合はする
        user.form.update(**req.form_to_dict())
    elif request.form.get("ok") == "抽出":
        user.form.update(**req.form_to_dict())
        user.form.update(
            **{column: ",".join(request.form.getlist("key_code"))}
        )
    df = db.sql.create_df(sql=user.form.to_sql(download=False))
    # Message
    messages = []
    count = len(df)
    if count >= user.max_rows:
        messages.append(
            "件数：{:,} ({})".format(count, user.max_rows)
        )
    else:
        messages.append("件数：{:,}".format(count))
    df_dsp = df.head(user.max_rows)
    return render_template(
        "master.html",
        MyColor=user.mycolor,
        Department=user.department,
        LastRefreshDate=system.last_refresh_date,
        user_form=user.form.to_dict(),
        messages=messages,
        column=column,
        SelectList=user.form.values_for_checkbox(column),
        headers=df_dsp.columns,
        records=df_dsp.values.tolist()
    )


@app.route("/download/<flg>", methods=["GET"])
def download(flg):
    user = system.load(request.remote_addr)
    df = db.sql.create_df(sql=user.form.to_sql(download=True))
    if flg != "master":
        df1, df2, df3 = arrage_df(df=df)
        # To File .csv
        if flg == "totall1":
            df = df1
        elif flg == "totall2":
            df = df2
        elif flg == "totall3":
            df = df3
    df.to_csv(TEMP_CSV, index=False, encoding="cp932", escapechar="|")
    return send_file(
        TEMP_CSV,
        download_name="download.csv"
    )


#
# Setting
#
@app.route("/setting", methods=["GET", "POST"])
def setting():
    user = system.load(request.remote_addr)
    db_tables = [h.file_name for h in host.data_files]
    if request.method == "POST":
        click = request.form.get("ok")
        if click == "設定変更":
            user.update(
                MaxRows=int(request.form["MaxRows"]),
                Department=request.form["Department"],
                MyColor=request.form["MyColor"]
            )
            system.save_file()
        elif (
            click == "最新データ取得"
            and system.last_refresh_date != "更新中"
        ):
            table_name = request.form.get("table_name")
            sync.refresh_all(
                first_date=request.form["first_date"].replace("-", ""),
                last_date=request.form["last_date"].replace("-", ""),
                contain_master=request.form.get("contain_master"),
                table_name=table_name
            )
            system.save_file()
    last_month = datetime.today() - relativedelta(months=1)
    return render_template(
        "setting.html",
        MaxRows=user.max_rows,
        MyColor=user.mycolor,
        Department=user.department,
        LastRefreshDate=system.last_refresh_date,
        first_date=last_month.strftime(r"%Y-%m-01"),
        last_date=datetime.now().strftime((r"%Y-%m-%d")),
        log_texts=LOGGER.to_text_info()[-8:],
        db_tables=db_tables
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():
    log_texts = []
    sql_code = ""
    values = []
    if request.method == "POST":
        ok = request.form.get("ok", "")
        if ok == "設定変更":
            system.last_refresh_date = request.form["LastRefreshDate"]
        elif ok == "SQL送信":
            sql_code = request.form.get("sql_code")
            values = db.sql.create_list(sql=sql_code)
        elif ok == "debug":
            log_texts = LOGGER.to_text_debug()
        elif ok == "info":
            log_texts = LOGGER.to_text_info()
        elif ok == "warning":
            log_texts = LOGGER.to_text_warning()
        elif ok == "critical":
            log_texts = LOGGER.to_text_critical()
    return render_template(
        "admin.html",
        MyColor="default",
        log_texts=log_texts,
        sql_code=sql_code,
        LastRefreshDate=system.last_refresh_date,
        values=values
    )


@app.route('/favicon.ico')
def favicon():
    """Select ico"""
    return send_from_directory(
        os.path.join(app.root_path, 'static/image'),
        'favicon.ico'
    )


#
# Handling Error
#
def e_to_html(e) -> str:
    """HTML側で{% autoescape false %}にする"""
    return traceback.format_exception_only(e)[-1].replace(
        "\n", "<br>").replace(
            "\n", "<br>").replace(
                " ", "&nbsp;")


@app.errorhandler(400)
def bad_request(e):
    LOGGER.debug(f"{e}")
    return render_template(
        "400.html",
        MyColor="default",
        e=e_to_html(e)
    ), 400


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.errorhandler(405)
def method_not_allowed(e):
    return redirect("/")


@app.errorhandler(500)
def internal_server_error(e):
    LOGGER.debug(f"{e}")
    return render_template(
        "500.html",
        MyColor="default",
        e=e_to_html(e)
    ), 500
