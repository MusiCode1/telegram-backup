from lib.main import upload_mysqldump_to_tg
import os

mysqldump = {
    "path": os.getenv("path"),
    "db": os.getenv("db"),
    "db_user": os.getenv("db_user"),
    "db_password": os.getenv("db_password"),
    "program": os.getenv("program")
}

tg = {
    "api_id": os.getenv("api_id"),
    "api_hash": os.getenv("api_hash"),

    "entity": int(os.getenv("entity"))
}


upload_mysqldump_to_tg(mysqldump, tg)
