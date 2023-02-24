from flask import request

from ProgramFiles.flaskr import app
from ProgramFiles.flaskr.mymod.log import LOGGER


class Request:

    def form_to_dict(self):
        return request.form.to_dict()

    def form_to_query(self) -> dict[str, str]:
        dic = request.form.to_dict()

        def set_value(old, sign, new, replace=False, date=False):
            old_v = dic.get(old, "")
            if date:
                old_v = old_v.replace("-", "")
            if not old_v:
                sign = ""
            if replace:
                dic[new] = sign + old_v
                return
            dic[new] = dic.get(new, "") + sign + old_v
            return

        set_value("開始日付", "&>=", "伝票日付", replace=True, date=True)
        set_value("終了日付", "&<=", "伝票日付", date=True)
        set_value("得意先", "", "得意先コード", replace=True)
        set_value("雑", "", "雑コード", replace=True)
        set_value("送荷先", "", "送荷先コード", replace=True)
        set_value("製品部品", "", "製品部品コード", replace=True)
        set_value("担当者", "", "担当者コード", replace=True)
        set_value("伝区", "", "伝票区分", replace=True)
        set_value("品目", "", "品目コード", replace=True)
        fg = dic.get("製品部品フラグ", "")
        if fg == "製品のみ":
            dic["製品部品コード"] = dic.get("製品部品コード", "") + f"&<{10**7}"
        elif fg == "部品のみ":
            dic["製品部品コード"] = dic.get("製品部品コード", "") + f"&>={10**7}"

        if app.debug:
            LOGGER.debug(f"Request.form_to_query\nAfter form: {dic}")
        return dic
