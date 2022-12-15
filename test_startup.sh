#!/usr/bin/env bash

run() {
    output=`{ timeout 10 python3 $1; } 2>&1`
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

error=0
check main.py || error=1
for path in examples/*
do
    check $path/main.py || error=1
done
test $error -eq 0
