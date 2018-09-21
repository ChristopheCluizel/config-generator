#!/usr/bin/env bash

set -e

function usage() {
    echo "Deploy the application to a host machine

Usage: $0 [arguments]
    -h, --help                          display this help message
    --host-ip        <HOST_IP>          the public IP of a host machine to deploy
    --aws-region     <AWS_REGION>       the AWS region used for the Parameter Store

Example:
    ./deploy.sh --host-ip 192.0.0.1 --aws-region eu-west-1
"
}

# Check that we run this script from config-generator root folder
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
        --host-ip)
        HOST_IP="$2"
        shift # past argument
        shift # past value
        ;;
        --aws-region)
        AWS_REGION="$2"
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
check_argument "host-ip" "${HOST_IP}"
check_argument "aws-region" "${AWS_REGION}"

# Set the remote host IP in the Ansible inventory file
sed "s/<host_ip>/""$HOST_IP""/g" inventory.ini.template > inventory.ini

# Provide the host machine
ansible-playbook ansible.yml -i inventory.ini --extra-vars "aws_region=""$AWS_REGION"