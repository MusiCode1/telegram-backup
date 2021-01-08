from telethon import TelegramClient
from dotenv import load_dotenv
from subprocess import PIPE
import subprocess
import telethon
import datetime
import asyncio
import random

import gzip
import os
import io

chunk_size = 1024 * 16
chunk_size_max = 1024 * 1024 * 1024 * 2

date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
file_name = "backup_" + date + ".sql"

db = os.getenv("db")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
program = os.getenv("program")

path = os.getenv("path")

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")

entity = int(os.getenv("entity"))


class get_mysqldump:

    def exec(self, data):

        if data["password"] is not None:
            local_password = "-p" + data["password"]

        else:
            local_password = ""

        arg = [data["program"], "-u", data["user"],
               local_password, data["db"]]

        self.p = subprocess.Popen(arg, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    def gzip_compress(self):

        def get_file_name():
            return file_name + ".gz." + str(self.file_num).rjust(3, "0")

        p = self.p.stdout

        with io.BytesIO() as stream:

            file = ""
            i = 0
            with gzip.GzipFile(file_name, "wb", fileobj=stream) as w_gz:
                for chunk in iter(lambda:  p.read(chunk_size), b''):

                    chunk = chunk.decode("utf-8")
                    # print(chunk)
                    chunk = chunk.encode()

                    if not file or file.tell() >= chunk_size_max:
                        if file:
                            file.close()
                        self.file_num += 1
                        file = open(get_file_name(), "wb")

                    w_gz.write(chunk)
                    w_gz.flush()

                    file.write(stream.getvalue())
                    stream.seek(0)
                    stream.truncate(0)

                    i += len(chunk)
                    if not i % (1024*512):
                        print(i/1024/1024)
                w_gz.close()
                file.write(stream.getvalue())
                file.close()

    async def upload(self):

        def callback(current, total):
            print('Downloaded', current, 'out of', total,
                  'bytes: {:.2%}'.format(current / total))

        file_list = []

        if self.file_num < 2:
            file = file_name + ".gz"
            os.rename(file + ".001", file)
            file_list.append(file)
        else:
            for index in range(1, self.file_num + 1):
                file_list.append(file_name + ".gz." + str(index).rjust(3, "0"))

        res = await self.client.send_file(entity, file_list,
                                          progress_callback=callback)

        for file in file_list:
            os.remove(file)

    def __init__(self, db, user="root", password=None, program="mysqldump"):

        self.file_num = 0
        self.p = ""

        self.exec({"db": db, "user": user,
                   "password": password, "program": program})
        self.gzip_compress()

        self.client = TelegramClient("token", api_id, api_hash)
        self.client.start()

        with self.client:
            self.client.loop.run_until_complete(self.upload())


get_mysqldump(db, db_user, db_password, program)
