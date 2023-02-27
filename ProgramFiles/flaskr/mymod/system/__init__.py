import os
import json

from ProgramFiles.flaskr.mymod.log import LOGGER
from ProgramFiles.flaskr.mymod.system.user import User
from ProgramData import SYSTEMDIR

SYSTEM_JSON = os.path.join(SYSTEMDIR, "system.json")


class SystemDictionary:

    def __init__(self):
        try:
            with open(SYSTEM_JSON, mode="r", encoding="utf-8") as f:
                filedic: dict[str, dict[str, str | dict[str, str]]] = json.load(f)
        except (FileNotFoundError):
            LOGGER.info(f"Create File ({SYSTEM_JSON})")
            with open(SYSTEM_JSON, mode="w", encoding="utf-8") as f:
                filedic: dict[str, dict[str, str | dict[str, str]]] = {}
        self.last_refresh_date = filedic.pop("LastRefreshDate", "")
        self.dic = {k: User(**v) for k, v in filedic.items()}

    def to_dict(self):
        return {
            **{k: user.to_dict() for k, user in self.dic.items()},
            **{"LastRefreshDate": self.last_refresh_date}
        }

    def load(self, id: str, /) -> User:
        if id not in self.dic:
            LOGGER.debug(
                f"SystemDictionary.load\nWelcome New User !! ID: {id}"
            )
            self.dic[id] = User()
        return self.dic[id]

    def save_file(self):
        with open(SYSTEM_JSON, mode="w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=3, ensure_ascii=False)


system = SystemDictionary()
