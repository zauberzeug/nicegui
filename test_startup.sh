#!/usr/bin/env bash

run() {
    [[ ${1##*.} == "py" ]] && cmd_prefix="python3" || cmd_prefix=""
    output=$({ timeout 10 $cmd_prefix $1; } 2>&1)
    exitcode=$?
    test $exitcode -eq 124 && exitcode=0 # exitcode 124 is comming from "timeout command above"
    echo $output | grep -e "NiceGUI ready to go" -e "Uvicorn running on http://0.0.0.0:8000" > /dev/null || exitcode=1
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
    if run $(basename "$1"); then
        echo "ok --------"
        popd > /dev/null
    else
        echo "failed -------"
        popd > /dev/null
        return 1
    fi
}

check main.py || error=1
for path in examples/*
do
    if test -f $path/start.sh; then
       check $path/start.sh || error=1 
    elif test -f $path/main.py; then
        check $path/main.py || error=1
    fi
done
test $error -eq 0
