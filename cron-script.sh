# /bin/bash -l
# 0 6 * * * .../cron-script.sh
export PATH=~/.local/bin:$PATH
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

file=./main.py

pipenv run python $file