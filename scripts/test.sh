#!/usr/bin/env bash

set -e

function usage() {
    >&2 cat << EOM
Test the app
--help display this message.

Usage:

    $0 aws_region aws_profile build

Options:
    aws_region      the AWS region used fot the Parameter Store
    aws_profile     the AWS profile used for the Parameter Store
    build           (optional) if we want to build the image

Example:

In this example

    ./test.sh eu-west-1 perso
EOM
    exit 1
}

if [ "$1" == "--help" ]; then
    usage
fi

# Validate arguments
if [ ! -z "$1" ] && [ ! -z "$2" ]; then
    AWS_REGION=$1
    AWS_PROFILE=$2
else
    usage
fi

# export environment variables necessary for the tests
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile "$AWS_PROFILE")
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile "$AWS_PROFILE")

# fill the .env file to pass variable to the container
ENV_FILE=".env"

echo "AWS_REGION=""$AWS_REGION" > "$ENV_FILE"
echo "AWS_ACCESS_KEY_ID=""$AWS_ACCESS_KEY_ID" >> "$ENV_FILE"
echo "AWS_SECRET_ACCESS_KEY=""$AWS_SECRET_ACCESS_KEY" >> "$ENV_FILE"

if [ ! -z "$3" ] && [ "$3" == "build" ]; then
    docker-compose -f docker-compose.test.yml up --build
else
    docker-compose -f docker-compose.test.yml up
fi

rm .env