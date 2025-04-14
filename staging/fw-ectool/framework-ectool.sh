#!/usr/bin/env bash

if [ "$EUID" != 0 ]
then
    sudo bash "$0" "$@"
    exit $?
fi

if [[ -d /etc/framework-ectool ]]
then
    for script in /etc/framework-ectool/*
    do 
        bash "$script"
    done
fi
