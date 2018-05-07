from flask import Flask, Response, request, abort
from src import generator
import json
from src.APIException import Exception_400, Exception_404

app = Flask(__name__)


# TODO configure logger + logs format

@app.route("/")
def home():
    return status()


@app.route("/status")
def status():
    response = {'success': True}
    return Response(response=json.dumps(response), content_type='application/json', status=200)


@app.route("/generate-conf", methods=['POST'])
def generate_conf():
    try:
        result = generator.generate_conf(request)
        return Response(response=result, content_type='text/plain', status=200)
    except Exception_400 as e:
        app.logger.info(str(e.exception_message))
        abort(400, str(e.api_message))
    except Exception_404 as e:
        app.logger.info(str(e.exception_message))
        abort(404, str(e.api_message))
    except Exception as e:
        app.logger.error(str(e))
        abort(500)


@app.errorhandler(500)
def internal_server_error(error):
    res = {"error": "internal server error", "error_description": None}
    return Response(json.dumps(res), content_type='application/json', status=500)


@app.errorhandler(400)
def bad_request(error):
    res = {"error": "invalid request", "error_description": error.description}
    return Response(json.dumps(res), content_type='application/json', status=400)


@app.errorhandler(404)
def not_found(error):
    res = {"error": "not found", "error_description": error.description}
    return Response(json.dumps(res), content_type='application/json', status=404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
