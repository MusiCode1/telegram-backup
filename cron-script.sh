# /bin/bash -l
# 0 6 * * * ./cron-script.sh
export ~/.local/bin
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

SCRIPTPATH="$(
    cd "$(dirname "$0")" >/dev/null 2>&1
    pwd -P
)"
cd $SCRIPTPATH

~/.local/bin/pipenv shell python main.py
