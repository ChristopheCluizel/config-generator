#!/usr/bin/env bash

check_argument() {
    if [ -z "$2" ]; then
        echo "Argument [$1] is missing, please provide all arguments as following:"
        usage
        exit 1
    fi
}