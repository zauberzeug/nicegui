#!/usr/bin/env bash

run() {
    pwd
    output=$({ timeout 10 ./$1 $2; } 2>&1)
    exitcode=$?
    test $exitcode -eq 124 && exitcode=0 # exitcode 124 is comming from "timeout command above"
    echo $output | grep -e "NiceGUI ready to go" -e "Uvicorn running on http://127.0.0.1:8000" > /dev/null || exitcode=1
    echo $output | grep "Traceback" > /dev/null && exitcode=1
    echo $output | grep "Error" > /dev/null && exitcode=1
    if test $exitcode -ne 0; then
        echo "wrong exit code $exitcode. Output was:"
        echo $output
        return 1
    fi
}

check() {
    echo checking $1 ----------
    pushd $(dirname "$1") >/dev/null
    if run $(basename "$1") $2; then
        echo "ok --------"
        popd > /dev/null
    else
        echo "failed -------"
        popd > /dev/null
        return 1
    fi
}

error=0
check main.py || error=1
for path in examples/*
do
    # skip if python is 3.11 and if path is examples/sqlite_database
    if test $(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2) = "3.11" && test $path = "examples/sqlite_database"; then
        continue # until https://github.com/omnilib/aiosqlite/issues/241 is fixed
    fi

    # skip if python is 3.12 and if path is examples/sqlite_database
    if test $(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2) = "3.12" && test $path = "examples/sqlite_database"; then
        continue # until https://github.com/omnilib/aiosqlite/issues/241 is fixed
    fi

    # skip if path is examples/pyserial
    if test $path = "examples/pyserial"; then
        continue # because there is no serial port in github actions
    fi

    # install all requirements except nicegui
    if test -f $path/requirements.txt; then
        sed '/^nicegui/d' $path/requirements.txt > $path/requirements.tmp.txt || error=1 # remove nicegui from requirements.txt
        python3 -m pip install -r $path/requirements.tmp.txt || error=1
        rm $path/requirements.tmp.txt || error=1
    fi

    # run start.sh or main.py
    if test -f $path/start.sh; then
        check $path/start.sh dev || error=1
    elif test -f $path/main.py; then
        check $path/main.py || error=1
    fi
done
test $error -eq 0
