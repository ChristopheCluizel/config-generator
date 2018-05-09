#!/usr/bin/env bash

set -e

function usage() {
    echo "Test the application

Usage: $0 [arguments]
    -h, --help                            display this help message
    --aws-region        <AWS_REGION>      the AWS region used fot the Parameter Store
    --aws-profile       <AWS_PROFILE>     the AWS profile used for the Parameter Store
    -b, --build         <BUILD>           [OPTIONAL] if we want to build the image [yes|no] (default: no)

Example:
    ./test.sh --aws-region eu-west-1 --aws-profile perso
"
}

# Check that we run this script from cj-rocket root folder
CURRENT_DIRECTORY=$( basename "$PWD" )

if [ "$CURRENT_DIRECTORY" != "config_generator" ]; then
    echo "You must run this script from config_generator root project directory."
    exit 1
fi

# Retrieve project path
DIR="$( pwd )"

# Load helpers
source "${DIR}/scripts/functions.sh"

# get input arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --aws-region)
        AWS_REGION="$2"
        shift # past argument
        shift # past value
        ;;
        --aws-profile)
        AWS_PROFILE="$2"
        shift # past argument
        shift # past value
        ;;
        -b|--build)
        BUILD="$2"
        shift # past argument
        shift # past value
        ;;
        -h|--help)
        usage
        exit 0
        ;;
        *)
        unknown_argument "$@"
        ;;
    esac
done

# Validate mandatory arguments
check_argument "aws-region" "${AWS_REGION}"
check_argument "aws-profile" "${AWS_PROFILE}"

# export environment variables necessary for the tests
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile "$AWS_PROFILE")
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile "$AWS_PROFILE")

# fill the .env file to pass variable to the container
ENV_FILE=".env"

echo "AWS_REGION=""$AWS_REGION" > "$ENV_FILE"
echo "AWS_ACCESS_KEY_ID=""$AWS_ACCESS_KEY_ID" >> "$ENV_FILE"
echo "AWS_SECRET_ACCESS_KEY=""$AWS_SECRET_ACCESS_KEY" >> "$ENV_FILE"

if [ "$BUILD" == "yes" ]; then
    docker-compose -f docker-compose.test.yml up --build
else
    docker-compose -f docker-compose.test.yml up
fi

rm .env