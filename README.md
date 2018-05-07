Config Generator
===

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
* curl -X POST -H "Content-Type: text/plain" --data-binary '{"key":"value"}' 'localhost:8000/generate-conf?key_prefix=perso/dev'
* curl -X POST -H "Content-Type: text/plain" --data-binary @resources/conf_template_examples/json_conf_template.j2  'localhost:8000/generate-conf?key_prefix=perso/dev'
* cat resources/conf_template_examples/python_conf_template.j2 | curl -X POST -H "Content-Type: text/plain" --data-binary @- 'localhost:8000/generate-conf?key_prefix=perso/dev'

```