Config Generator
===

## How to run
Run the following command
```bash
./scripts/run.sh --help
```

## Query examples
```bash
* curl -X POST -H "Content-Type: text/plain" --data-binary '{"key":"value"}' 'localhost:8000/generate-conf?client=perso&env=dev'
* curl -X POST -H "Content-Type: text/plain" --data-binary @resources/json_conf_template.j2  'localhost:8000/generate-conf?client=perso&env=dev'
* cat resources/python_conf_template.j2 | curl -X POST -H "Content-Type: text/plain" --data-binary @- 'localhost:8000/generate-conf?client=perso&env=dev'

```