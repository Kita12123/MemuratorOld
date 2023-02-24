import os

SYSTEMDIR = os.path.dirname(__file__)

DATABASE = os.path.join(SYSTEMDIR, "database.db")
TEMP_CSV = os.path.join(SYSTEMDIR, "download.csv")
SYSTEM_JSON = os.path.join(SYSTEMDIR, "system.json")
DEBUG_LOG = os.path.join(SYSTEMDIR, "debug.txt")
INFO_LOG = os.path.join(SYSTEMDIR, "info.txt")
WARNING_LOG = os.path.join(SYSTEMDIR, "warnig.txt")
CRITICAL_LOG = os.path.join(SYSTEMDIR, "critical.txt")
