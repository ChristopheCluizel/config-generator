import boto3
from jinja2 import Environment, FileSystemLoader
import re
from .APIException import Exception_400
import os


def generate_conf(request):
    data = extract_data(request)
    template_string = data['data']
    key_prefix = data['parameters']['key_prefix']
    aws_region = os.environ['AWS_REGION']

    template_keys = get_template_keys_from_string(template_string)
    cmdb_param_names = generate_cmdb_param_names(template_keys, key_prefix)

    secret_dict = {}
    for template_key, cmdb_param_name in cmdb_param_names.items():
        secret_dict[template_key] = get_ssm_param(cmdb_param_name, aws_region)

    jinja_env = Environment(
        loader=FileSystemLoader('.'),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # register the custom Jinja filter
    jinja_env.filters['split'] = split_filter

    template_without_secret = jinja_env.from_string(template_string)
    template_with_secrets = generate_template_with_secrets(template_without_secret, secret_dict)

    return template_with_secrets


def extract_data(request):
    data = request.data.decode("utf-8")
    key_prefix = request.args.get('key_prefix')

    if data == '':
        raise Exception_400("request body is missing", "request body is missing", None)

    return {"data": data, "parameters": {"key_prefix": key_prefix}}


def get_template_keys_from_string(template_string):
    """
    Retrieve all the keys from the template string which are identified by '{{ <key_name> }}'.

    :param template_string: the template in a string
    :type template_string: string
    :return: the list of the template keys corresponding to secret parameters
    :rtype: list[string]
    """

    keys = re.findall(r"{{([a-z0-9_ ]+)", template_string)
    trimmed_keys = [key.strip() for key in keys]

    return trimmed_keys


def generate_cmdb_param_names(template_keys, key_prefix):
    """
    Generate the secret parameter names based on the client and environment. In the Parameter Store,
    the parameter names follow the following pattern: /<client>/<env>/<template_key>. Example: /ripl/prod/redshift/host

    :param template_keys: all the secret parameters to retrieve based on the template
    :type template_keys: list[string]
    :param key_prefix: a prefix to add before template keys (can be None)
    :type key_prefix: string
    :return: a dictionary containing the template keys with the corresponding secret parameter name as value
        Example: {"redshift_user": "/ripl/prod/redshift/user"}
    :rtype: dict
    """
    res = {}

    if key_prefix is None:
        key_prefix_string = "/"
    else:
        key_prefix_string = "/{}/".format(key_prefix)

    for template_key in template_keys:
        # as we can't use '-' in the template variable name, we use '__'. However in the Parameter Store, the '-'
        # can be used. Therefore we have to do the conversion
        template_key_with_dash = template_key.replace('__', '-')

        # '_' in the template corresponds to '/' in the AWS Parameter Store
        path = template_key_with_dash.replace('_', '/')
        res[template_key] = "{}{}".format(key_prefix_string, path)

    return res


def get_ssm_param(cmdb_param_name, region_name="eu-west-1"):
    """
    Get the secret parameter from the AWS Parameter Store thanks to its name. The permissions to access the Parameter
    Store are:
    * "Assume Role" for remote server
    * "Environment variables" for dev mode and running tests locally (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)

    :param cmdb_param_name: the name of the secret parameter name to retrieve from the Parameter Store
    :type cmdb_param_name: string
    :param region_name: the region name of the Parameter Store we want to use
    :type region_name: string
    :return: the secret parameter
    :rtype: string
    """
    ssm = boto3.client('ssm', region_name=region_name)

    ssm_response = ssm.get_parameter(
        Name=cmdb_param_name,
        WithDecryption=True
    )

    ssm_parameter = ssm_response.get("Parameter").get("Value")
    return ssm_parameter


def generate_template_with_secrets(template_without_secret, secret_dict):
    """
    Generate the template with the secrets.

    :param template_without_secret: the template without the secret
    :type template_without_secret: jinja2.Template
    :param secret_dict: the secret
    :type secret_dict: dict
    :return: the template with the secrets
    :rtype: string
    """
    return template_without_secret.render(secret_dict)


def split_filter(string_to_split, delimiter):
    """
    Create a custom Jinja filter to use it in the Jinja2 template. Same functionality as the split function in the
    Python language

    :param string_to_split: the string to split
    :type string_to_split: string
    :param delimiter: the delimiter to split the string into
    :type delimiter: string
    :return: the string split as a list
    :rtype: list[string]
    """
    if string_to_split is not None:
        return string_to_split.split(delimiter)
    else:
        return None
