from datetime import date

from requests import Response


def mock_fixer_api(url):
    response = Response()
    response._content = b'{"success": true,"timestamp": 1644780663,"base": "EUR","date":' + str.encode(
        "\"%s\"" % date.today().strftime('%Y-%m-%d'))+b','+b'"rates": {"EGP": 17.832328, "EUR": 1, "USD": 1.134951}}'
    response.status_code = 200
    return response
