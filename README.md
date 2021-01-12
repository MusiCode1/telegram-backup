# telegram-babkup
<div dir="rtl" text-align="right">
גיבוי MySQL לענן של טלגרם
- תמיכה בפיצול קבצים מעבר ל-2 ג'יגה


דוגמא לשימוש:
<div dir="ltr" text-align="left">

    from lib.main import upload_mysqldump_to_tg
    import os

    name = os.getenv("name")

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


    upload_mysqldump_to_tg(name, mysqldump, tg)
