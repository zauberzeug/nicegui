#!/usr/bin/env bash

run() {
    output=`{ timeout 2 python3 $1; } 2>&1`
    exitcode=$?
    test $exitcode -eq 124 && exitcode=0 # exitcode 124 is comming from "timeout command above"
    echo $output | grep "JustPy ready to go" > /dev/null || exitcode=1
    echo $output | grep "Traceback" > /dev/null && exitcode=1
    echo $output | grep "Error" > /dev/null && exitcode=1
    if test $exitcode -ne 0; then
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

exitcode=0
pushd ../
check main.py || exitcode=1
check examples.py || exitcode=1
popd
echo exit $exitcode
test $exitcode -eq 0