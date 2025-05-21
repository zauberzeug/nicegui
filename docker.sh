#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Usage:"
    echo
    echo "  `basename $0` (b | build)        Build or rebuild"
    echo "  `basename $0` (u | up)           Create and start"
    echo "  `basename $0` (U | upbuild)      Create and start (force build)"
    echo "  `basename $0` (d | down)         Stop and remove"
    echo "  `basename $0` (s | start)        Start"
    echo "  `basename $0` (r | restart)      Restart"
    echo "  `basename $0` (h | stop)         Stop (halt)"
    echo "  `basename $0` ps                 List"
    echo "  `basename $0` rm                 Remove"
    echo "  `basename $0` stats              Show statistics"
    echo
    echo "  `basename $0` (l | log)                 Show log tail (last 100 lines)"
    echo "  `basename $0` (e | exec)     <command>  Execute command"
    echo "  `basename $0` (a | attach)              Attach to container with shell"
    echo
    echo "  `basename $0` prune      Remove all unused containers, networks and images"
    echo "  `basename $0` stopall    Stop all running containers (system-wide!)"
    echo "  `basename $0` killall    Kill all running containers (system-wide!)"
    echo
    echo "Arguments:"
    echo
    echo "  command       Command to be executed inside a container"
    exit
fi

cmd=$1
cmd_args=${@:2}
case $cmd in
    b | build)
        docker compose build $cmd_args
        ;;
    u | up)
        docker compose up -d $cmd_args
        ;;
    U | buildup | upbuild | upb | bup | ub)
        docker compose up -d --build $cmd_args
        ;;
    d | down)
        docker compose down $cmd_args
        ;;
    s | start)
        docker compose start $cmd_args
        ;;
    r | restart)
        docker compose restart $cmd_args
        ;;
    h | stop)
        docker compose stop $cmd_args
        ;;
    rm)
        docker compose rm $cmd_args
        ;;
    ps)
        docker compose ps $cmd_args
        ;;
    stat | stats)
        docker stats $cmd_args
        ;;
    l | log | logs)
        docker compose logs -f --tail 100 $cmd_args app
        ;;
    e | exec)
        docker compose exec $cmd_args app
        ;;
    a | attach)
        docker compose exec $cmd_args app /bin/bash
        ;;
    prune)
        docker system prune
        ;;
    stopall)
        docker stop $(docker ps -aq)
        ;;
    killall)
        docker kill $(docker ps -aq)
        ;;
    *)
        echo "Unsupported command \"$cmd\""
        exit 1
esac
