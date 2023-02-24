from ProgramFiles.flaskr import app
from ProgramFiles.flaskr.mymod.log import LOGGER
from ProgramFiles.flaskr.mymod.system.form import Form


class User:

    def __init__(self, **kwargs):
        self.dic: dict[str, str | dict] = {
            "MyColor": "default",
            "Department": "Sales",
            "MaxRows": 500,
            "Form": {}
        }
        self.update(**kwargs)
        if app.debug:
            LOGGER.debug(f"User.__init__\nself.dic: {self.dic}")
        self.dic["Form"] = Form(**self.dic["Form"])

    @property
    def mycolor(self):
        return self.dic["MyColor"]

    @property
    def department(self):
        return self.dic["Department"]

    @property
    def max_rows(self):
        return self.dic["MaxRows"]

    @property
    def form(self) -> Form:
        return self.dic["Form"]

    def to_dict(self):
        return {**self.dic, **{"Form": self.dic["Form"].to_dict()}}

    def update(self, **kwargs):
        if type(kwargs.get("MyColor", "")) is not str:
            raise TypeError("MyColor arg must String!!")
        if type(kwargs.get("Department", "")) is not str:
            raise TypeError("Department arg must String!!")
        if type(kwargs.get("MaxRows", 0)) is not int:
            raise TypeError("MaxRows arg must Integer!!")
        if type(kwargs.get("Form", {})) is not dict:
            raise TypeError("Form arg must Form!!")
        self.dic.update(kwargs)
