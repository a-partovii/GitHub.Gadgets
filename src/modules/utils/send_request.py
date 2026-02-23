import requests as req
from modules.utils import network_error_handler, delay

def send_request(method:str, url:str, headers:dict, max_retries:int =10, network_timeout:int =10) -> req.Response | bool :
    """
        Send an HTTP request with retries on network errors.

        Args:
            method (str): HTTP method (Get, Put, etc.).
            url (str): Request URL.
            headers (dict): Request headers.
            max_retries (int, optional): Number of retries (default=10).
            network_timeout (int, optional): Timeout in seconds (default=10).

        Returns:
            req.Response | bool: Response on success, False on failure.
    """
    for _ in range(0, max_retries) : # Retry loop for network failures
            try:
                response = req.request(method=method, url=url, headers=headers, timeout=network_timeout)
                return response

            # Network errors
            except req.RequestException as error:
                message = network_error_handler(error)
                delay(message)

    print(message)
    return False