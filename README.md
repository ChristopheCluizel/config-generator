Config Generator
===

[![Build Status](https://travis-ci.org/ChristopheCluizel/config-generator.svg?branch=master)](https://travis-ci.org/ChristopheCluizel/config-generator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## How to clone the repo
```bash
git clone git@github.com:ChristopheCluizel/config-generator.git config_generator
```

## How to run
Run the following command
```bash
./scripts/run.sh --help
```

## How to stop
```bash
./scripts/down.sh
```

## How to test
The container will be run in attached mode to be able to directly see the results.
```bash
./scripts/test.sh --help
```

## How to linter
```bash
./scripts/linter.sh
```

## CURL query examples
```bash
* curl -X POST -H "Content-Type: text/plain" --data-binary '{"key":"{{all_test_config__generator_test__key}}"}' 'localhost:8000/generate-conf'
* curl -X POST -H "Content-Type: text/plain" --data-binary @resources/conf_template_examples/json_conf_template.j2  'localhost:8000/generate-conf?key_prefix=perso/dev'
* cat resources/conf_template_examples/python_conf_template.j2 | curl -X POST -H "Content-Type: text/plain" --data-binary @- 'localhost:8000/generate-conf?key_prefix=perso/dev'

```

## How to deploy

The following points are required on the machine before deploying:
* attach a role to the machine so that it can access the Parameter Store.
* attach a security group to the machine to whitelist IPs. Otherwise, the API will be opened to the world and all your Parameter Store secrets reachable by anyone. Authorize only HTTPS connection.

Currently, the following deploy script works only for an instance with the following Amazon AMI : ami-66506c1c
```bash
./scripts/deploy.sh --help
```