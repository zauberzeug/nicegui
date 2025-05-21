#!/usr/bin/env bash

set -euo pipefail

run() {
    pwd
    output=$({ timeout 10 ./"$1" "${@:2}"; } 2>&1)
    exitcode=$?
    [[ $exitcode -eq 124 ]] && exitcode=0 # exitcode 124 is coming from "timeout command above"
    echo "$output" | grep -qE "NiceGUI ready to go|Uvicorn running on http://127.0.0.1:8000" || exitcode=1
    echo "$output" | grep -qE "Traceback|Error" && exitcode=1
    if [[ $exitcode -ne 0 ]]; then
        echo "Wrong exit code $exitcode. Output was:"
        echo "$output"
        return 1
    fi
}

check() {
    echo "Checking $1 ----------"
    pushd "$(dirname "$1")" >/dev/null

    max_attempts=3
    for attempt in $(seq 1 $max_attempts); do
        if run "$(basename "$1")" "${@:2}"; then
            echo "OK --------"
            popd > /dev/null
            return 0
        elif [ $attempt -eq $max_attempts ]; then
            echo "FAILED after $max_attempts attempts -------"
            popd > /dev/null
            return 1
        else
            echo "Attempt $attempt failed. Retrying..."
        fi
    done
}

check main.py || exit 1
for path in examples/*
do
    # Skip examples/generate_pdf
    if [[ $path == "examples/generate_pdf" ]]; then
        continue # until https://github.com/pygobject/pycairo/issues/387 is fixed
    fi

    # Skip examples/sqlite_database for Python 3.11 and 3.12
    if [[ $(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2) =~ ^3.1[12]$ ]] && [[ $path == "examples/sqlite_database" ]]; then
        continue # until https://github.com/omnilib/aiosqlite/issues/241 is fixed
    fi

    # skip if path is examples/pyserial
    if test $path = "examples/pyserial"; then
        continue # because there is no serial port in github actions
    fi

    # install all requirements except nicegui
    if test -f $path/requirements.txt; then
        sed '/^nicegui/d' $path/requirements.txt > $path/requirements.tmp.txt || exit 1 # remove nicegui from requirements.txt
        python3 -m pip install -r $path/requirements.tmp.txt || exit 1
        rm $path/requirements.tmp.txt || exit 1
    fi

    # run start.sh or main.py
    if test -f $path/start.sh; then
        check $path/start.sh dev || exit 1
    elif test -f $path/main.py; then
        check $path/main.py || exit 1
    fi
    if pytest -q --collect-only $path >/dev/null 2>&1; then
        echo "running tests for $path"
        pytest $path || exit 1
    fi
done

exit 0
