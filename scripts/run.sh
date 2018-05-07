#!/usr/bin/env bash

set -e

function usage() {
    >&2 cat << EOM
Run the app
--help display this message.

Usage:

    $0 env aws_region [aws_profile]

Options:
    env             environment to select the configuration (prod, dev)
    aws_region      the AWS region used fot the Parameter Store
    aws_profile     only for dev mode - the AWS profile used for the Parameter Store

Example:

In this example

    ./run.sh dev eu-west-1 perso
EOM
    exit 1
}

if [ "$1" == "--help" ]; then
    usage
fi

# Validate arguments
if [ ! -z "$1" ] && [ ! -z "$2" ]; then
    ENV=$1
    AWS_REGION=$2
else
    usage
fi

#check that we run this script from cj-rocket root folder
CURRENT_DIRECTORY=$( basename "$PWD" )

if [ "$CURRENT_DIRECTORY" != "config_generator" ]; then
    echo "You must run this script from config_generator root project directory."
    exit 1
fi

if [ "$ENV" = "prod" ]; then
    docker-compose -f docker-compose.yml up -d --build
elif [ "$ENV" = "dev" ]; then
    # Validate optional arguments for dev mode
    if [ ! -z "$3" ]; then
        AWS_PROFILE=$3
    else
        usage
    fi

    AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile "$AWS_PROFILE")
    AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile "$AWS_PROFILE")

    # fill the .env file to pass variable to the container
    ENV_FILE=".env"

    echo "AWS_REGION=""$AWS_REGION" > "$ENV_FILE"
    echo "AWS_ACCESS_KEY_ID=""$AWS_ACCESS_KEY_ID" >> "$ENV_FILE"
    echo "AWS_SECRET_ACCESS_KEY=""$AWS_SECRET_ACCESS_KEY" >> "$ENV_FILE"

    docker-compose up --build

    rm .env
else
    echo "Environment is not correct"
fi
