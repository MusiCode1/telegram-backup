from telethon import TelegramClient, functions, types
from dotenv import load_dotenv
from subprocess import PIPE, Popen

import subprocess
import telethon
import datetime
import asyncio
import random

import gzip
import time
import os
import io

load_dotenv()

chunk_size = 1024 * 16
chunk_size_max = 1024 * 1024 * 1024 * 2

date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
file_name = "backup." + date + ".sql"


class upload_mysqldump_to_tg:

    def size(self, num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def exec(self, data):

        if data["db_password"] is not None:
            local_password = "-p" + data["db_password"]

        else:
            local_password = ""

        arg = [
            data["program"], "-u", data["db_user"],
            local_password, data["db"]
        ]

        print("get mysqldump...")

        self.p = Popen(arg, stdout=PIPE, stdin=PIPE, stderr=PIPE)

        time.sleep(5)

        poll = self.p.poll()

        if poll is not None:
            raise Exception(self.p.stderr.read().decode())

    def gzip_compress(self):

        def get_file_name():
            return file_name + ".gz." + str(self.file_num).rjust(3, "0")

        def open_file():
            self.file_num += 1
            file = get_file_name()
            self.file_list.append(file)
            return open(file, "wb")

        p = self.p.stdout

        with io.BytesIO() as stream:

            file = ""
            i = 0
            with gzip.GzipFile(file_name, "wb", fileobj=stream) as w_gz:

                for chunk in iter(lambda:  p.read(chunk_size), b''):

                    if not file or file.tell() >= chunk_size_max:
                        if file:
                            file.close()

                        file = open_file()

                    w_gz.write(chunk)
                    w_gz.flush()

                    file.write(stream.getvalue())

                    i += len(chunk)
                    if not i % (1024*512):
                        print("source", self.size(i), "|",
                              "destination", self.size(file.tell()))
                        # print(chunk[0:50].decode())

                    stream.seek(0)
                    stream.truncate(0)

                w_gz.close()
                file.write(stream.getvalue())
                file.close()

    async def upload(self, tg):

        def progress_callback(current, total):
            print('Uploaded', self.size(current), 'out of', total,
                  'bytes: {:.2%}'.format(current / total))

        if self.file_num < 2:
            file = self.file_list[0]
            new_file = file.replace(".001", "")

            os.rename(file, new_file)
            self.file_list = new_file

        caption = "**Name:** " + str(self.name) \
            + "\n" + "**DataBase source:** " + self.db \
            + "\n" + "**Date:** " + \
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        res = await self.client.send_file(
            tg["entity"], self.file_list,
            caption=caption,
            progress_callback=progress_callback)

        if(type(self.file_list) is str):
            os.remove(self.file_list)
        else:
            for file in self.file_list:
                os.remove(file)

    def __init__(self, name, mysqldump, tg):

        if not mysqldump["db"]:
            raise Exception("no dataBase parameter")

        if not mysqldump["program"]:
            mysqldump["program"] = "mysqldump"

        if not mysqldump["db_password"]:
            mysqldump["db_password"] = None

        if not mysqldump["db_user"]:
            mysqldump["db_user"] = "root"

        self.file_num = 0
        self.p = ""
        self.file_list = []
        self.db = mysqldump["db"]
        self.name = name

        self.client = TelegramClient("token", tg["api_id"], tg["api_hash"])
        self.client.start()

        res = self.client(functions.messages.SetTypingRequest(
            peer=tg["entity"],
            action=types.SendMessageUploadDocumentAction(0)
        ))

        print(res)

        self.exec({
            "db": mysqldump["db"],
            "db_user": mysqldump["db_user"],
            "db_password": mysqldump["db_password"],
            "program": mysqldump["program"]
        })

        self.gzip_compress()

        with self.client:
            self.client.loop.run_until_complete(self.upload(tg))
