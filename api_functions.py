import hashlib
import hmac
import json
import time
import requests

api_client_id = "PKxQBuKM"
api_client_secret = "Wy6knva2UP2u-kWZS9TtWInYoi11_OJafgeUFuFHCYc"
api_exchange_address = "https://test.deribit.com"


def get_positions():
    # BTC POSITIONS
    tstamp = str(int(time.time()) * 1000)
    url = "/api/v2/private/get_positions"
    # nonce should be a random string, static nonce for simple illustration here
    nonce = "1234567890"
    # body of the POST request, JSON-RPC string
    body = "{\"jsonrpc\": \"2.0\",\"id\": \"8003\",\"method\": \"private/get_positions\",\"params\": {\"currency\": \"BTC\"}}"

    # signature for the request
    request_data = "POST" + "\n" + url + "\n" + body + "\n"
    base_signature_string = tstamp + "\n" + nonce + "\n" + request_data
    byte_key = api_client_secret.encode()
    message = base_signature_string.encode()
    sig = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

    authorization = "deri-hmac-sha256 id=" + api_client_id + ",ts=" + tstamp + ",sig=" + sig + ",nonce=" + nonce
    headers = {"Authorization": authorization}

    # send HTTPS POST request
    json_response = requests.post((api_exchange_address + url + "?"), headers=headers, data=body)
    response_dict = json.loads(json_response.content)

    positions_list_BTC = response_dict["result"]

    # ETH POSITIONS
    tstamp = str(int(time.time()) * 1000)
    url = "/api/v2/private/get_positions"
    # nonce should be a random string, static nonce for simple illustration here
    nonce = "1234567891"
    # body of the POST request, JSON-RPC string
    body = "{\"jsonrpc\": \"2.0\",\"id\": \"8003\",\"method\": \"private/get_positions\",\"params\": {\"currency\": \"ETH\"}}"

    # signature for the request
    request_data = "POST" + "\n" + url + "\n" + body + "\n"
    base_signature_string = tstamp + "\n" + nonce + "\n" + request_data
    byte_key = api_client_secret.encode()
    message = base_signature_string.encode()
    sig = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

    authorization = "deri-hmac-sha256 id=" + api_client_id + ",ts=" + tstamp + ",sig=" + sig + ",nonce=" + nonce
    headers = {"Authorization": authorization}

    # send HTTPS POST request
    json_response = requests.post((api_exchange_address + url + "?"), headers=headers, data=body)
    response_dict = json.loads(json_response.content)

    positions_list_ETH = response_dict["result"]

    # SOL POSITIONS
    tstamp = str(int(time.time()) * 1000)
    url = "/api/v2/private/get_positions"
    # nonce should be a random string, static nonce for simple illustration here
    nonce = "1234567892"
    # body of the POST request, JSON-RPC string
    body = "{\"jsonrpc\": \"2.0\",\"id\": \"8003\",\"method\": \"private/get_positions\",\"params\": {\"currency\": \"SOL\"}}"

    # signature for the request
    request_data = "POST" + "\n" + url + "\n" + body + "\n"
    base_signature_string = tstamp + "\n" + nonce + "\n" + request_data
    byte_key = api_client_secret.encode()
    message = base_signature_string.encode()
    sig = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

    authorization = "deri-hmac-sha256 id=" + api_client_id + ",ts=" + tstamp + ",sig=" + sig + ",nonce=" + nonce
    headers = {"Authorization": authorization}

    # send HTTPS POST request
    json_response = requests.post((api_exchange_address + url + "?"), headers=headers, data=body)
    response_dict = json.loads(json_response.content)

    positions_list_SOL = response_dict["result"]

    return positions_list_BTC, positions_list_ETH, positions_list_SOL


def get_instrument(instrument):
    url = "/api/v2/public/get_instrument"
    parameters = {'instrument_name': instrument}
    # send HTTPS GET request
    json_response = requests.get((api_exchange_address + url + "?"), params=parameters)
    response_dict = json.loads(json_response.content)
    instrument_details = response_dict["result"]

    return instrument_details


def get_instruments(currency):
    url = "/api/v2/public/get_instruments"
    parameters = {'currency': currency}
    # send HTTPS GET request
    json_response = requests.get((api_exchange_address + url + "?"), params=parameters)
    response_dict = json.loads(json_response.content)
    instrument_list = response_dict["result"]

    return instrument_list


def get_book_summary_by_instrument(instrument):
    url = "/api/v2/public/get_book_summary_by_instrument"
    parameters = {'instrument_name': instrument}
    # send HTTPS GET request
    json_response = requests.get((api_exchange_address + url + "?"), params=parameters)
    response_dict = json.loads(json_response.content)
    instrument_details = response_dict["result"]

    return instrument_details


def get_order_book(instrument):
    url = "/api/v2/public/get_order_book"
    parameters = {'instrument_name': instrument}
    # send HTTPS GET request
    json_response = requests.get((api_exchange_address + url + "?"), params=parameters)
    response_dict = json.loads(json_response.content)
    instrument_details = response_dict["result"]

    return instrument_details
