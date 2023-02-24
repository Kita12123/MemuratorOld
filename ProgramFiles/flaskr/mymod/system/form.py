from ProgramFiles.flaskr.mymod.sql_code import DB


class Form:

    def __init__(self, **kwargs):
        self.dic = {}
        self.update(**kwargs)

    @property
    def db_name(self):
        return self.dic.get("DB_name", "")

    def to_dict(self):
        return self.dic

    def update(self, **kwargs):
        self.dic.update(kwargs)

    def values_for_checkbox(self, column: str) -> list[str]:
        def func(x: str) -> list[str]:
            if not x.isdigit():
                return [x]
            x = int(x)
            if column == "得意先":
                if len(str(x)) < 5:
                    return [f"{x}10", f"{x}20", f"{x}40"]
                else:
                    [str(x)]
            return [x]
        value = self.dic.get(column, "").replace(" ", "")
        if not value:
            return []
        elif "," not in value:
            return func(value)
        result = []
        for s in value.split(","):
            result += func(s)
        return result

    def to_sql(self, *, download: bool) -> str:
        if download:
            return DB.load(self.db_name).to_sql_download(**self.dic)
        else:
            return DB.load(self.db_name).to_sql_display(**self.dic)
