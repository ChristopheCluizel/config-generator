#!/usr/bin/env bash

set -e

echo "---- Run shell linter..."
shellcheck scripts/*.sh
echo "OK"

echo "---- Run python linter..."
flake8 .
echo "OK"