import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import config


def verify_recaptcha(token: str, remote_ip: str) -> bool:
    """Validate the provided reCAPTCHA token.
    Functionality based on the `reCAPTCHA specification
    <https://developers.google.com/recaptcha/docs/display>`_.
    :param token: the token provided from the user request.
    :param remote_ip: the user's IP address
    :return: ``True`` if the token is valid, ``False`` otherwise.
    """
    if config.BYPASS_RECAPTCHA:
        return True

    if not token:
        return False

    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_secret_key = config.RECAPTCHA_SECRET
    payload = {
        'secret': recaptcha_secret_key,
        'response': token,
        'remoteip': remote_ip,
    }

    encoded_payload = urlencode(payload).encode()
    api_request = Request(recaptcha_url, encoded_payload, method='POST')
    response = urlopen(api_request)
    if response.status == 200:
        response_data = json.loads(response.read())
        return response_data.get('success', False)

    return False