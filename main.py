from telethon import TelegramClient
from dotenv import load_dotenv
from subprocess import PIPE
import subprocess
import os
import gzip
import io
import telethon
import datetime


load_dotenv()

db = os.getenv("db")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
program = os.getenv("program")

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")

entity = os.getenv("entity")


def get_mysqldump(db, user="root", password=None, program="mysqldump"):

    def exec():

        if password is not None:
            local_password = "-p" + password

        else:
            local_password = ""

        arg = [program, "-u", user,
               local_password, db]

        p = subprocess.Popen(arg, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        # p.wait()

        output = p.stdout.read()
        output = output.decode("utf-8")
        output = output.encode()

        return output

    def gzip_compress(data):
        file = io.BytesIO()

        with gzip.GzipFile("backup.sql", "wb", fileobj=file) as f:
            f.write(data)
            f.close()

        return file.getvalue()

    data = exec()
    data = gzip_compress(data)
    return data


async def main():

    file_name = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    file_name = "backup_" + file_name + ".sql.gzip"

    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    caption = "db backup:" + "\n" + "db: {}" + "\n" + "date: {}"
    caption = caption.format(db, date)

    file = get_mysqldump(db, db_user, db_password, program)

    attributes = [
        telethon.tl.types.DocumentAttributeFilename(
            file_name)
    ]

    res = await client.send_file(entity,
                                 file, caption=caption, attributes=attributes)

    print(res)

    pass


# Remember to use your own values from my.telegram.org!
client = TelegramClient('token', api_id, api_hash)
with client:
    client.loop.run_until_complete(main())
