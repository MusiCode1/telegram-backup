# /bin/bash -l
# 0 6 * * * .../cron-script.sh >> .../log.txt 2>&1
export PATH=$HOME/.local/bin:$PATH
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

script_path="$(
    cd "$(dirname "$0")" >/dev/null 2>&1
    pwd -P
)"

cd $script_path

pipenv run run_backup