#!/usr/bin/env bash

set -e

function usage() {
    echo "Run the application

Usage: $0 [arguments]
    -h, --help                            display this help message
    -e, --env           <ENV>             environment to select the configuration (prod, dev)
    --aws-region        <AWS_REGION>      the AWS region used for the Parameter Store
    --aws-profile       <AWS_PROFILE>     [OPTIONAL] only for dev mode - the AWS profile used for the Parameter Store

Example:
    ./run.sh --env dev --aws-region eu-west-1 --aws-profile perso
"
}

# Check that we run this script from the config-generator root folder
CURRENT_DIRECTORY=$( basename "$PWD" )

if [ "$CURRENT_DIRECTORY" != "config-generator" ]; then
    echo "You must run this script from config-generator root project directory."
    exit 1
fi

# Retrieve project path
DIR="$( pwd )"

# Load helpers
# shellcheck source=scripts/functions.sh
source "${DIR}/scripts/functions.sh"

# get input arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -e|--env)
        ENV="$2"
        shift # past argument
        shift # past value
        ;;
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
check_argument "env" "${ENV}"
check_argument "aws-region" "${AWS_REGION}"

# fill the .env file to pass variable to the container
ENV_FILE=".env"

echo "AWS_REGION=""$AWS_REGION" > "$ENV_FILE"

if [ "$ENV" = "prod" ]; then
    docker-compose -f docker-compose.yml up -d --build
elif [ "$ENV" = "dev" ]; then
    # Validate optional arguments for dev mode
    check_argument "aws-profile" "${AWS_PROFILE}"

    AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile "$AWS_PROFILE")
    AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile "$AWS_PROFILE")

    echo "AWS_ACCESS_KEY_ID=""$AWS_ACCESS_KEY_ID" >> "$ENV_FILE"
    echo "AWS_SECRET_ACCESS_KEY=""$AWS_SECRET_ACCESS_KEY" >> "$ENV_FILE"

    docker-compose up --build

    rm .env
else
    echo "Environment is not correct"
    usage
fi
