def network_error_handler(error):
    """
    Generate a simple message for network/request failure errors.

    args:
        error: The exception object from the network error.
        (e.g., error from except req.RequestException as error:)

    returns: tuple (bool, str): 
            - connection (bool): False if there was a network error, otherwise True.
            - message (str): A string message describing the network error.
    """
    if error is not None:
        return False, f"[ERROR] Network Error ({type(error).__name__}): {error}"
    return True, "[OK]"

def response_error_handler(response):
    """
    Handles GitHub HTTP response errors only.
    Does nothing for successful responses.

    args:
        response: The HTTP response object from the GitHub API request.

    returns: tuple (str, str):
            - action (str):  "break" if a critical issue requires stopping, otherwise "continue".
            - message (str): A string message describing the error.
    """
    if response is None:
        return "break", "[ERROR] No Response Received, check connection or retry later."

    # Response handling
    status = response.status_code
    remaining = response.headers.get("X-RateLimit-Remaining", "unknown")

    # Token error
    if status == 401:
        return "break", "[ERROR] Invalid or Expired Token."
        
    # Rate limit reached
    elif status == 429 or status == 403 or (remaining != "unknown" and int(remaining) <= 15):
        return "break", (f'[WARN] Token RateLimit is close to being reached, remaining: "{remaining}"' +
                         "\n take a break and continue later...")
        
    # Not found
    elif status == 404:
       return "continue", "[WARN] Resource Not Found."
       
    # GitHub internal error (server)
    elif status >= 500:
        return "break", f"[ERROR] Server Error {status}, retry later."
        
    # other
    elif status in [400, 408, 409, 412, 413, 414, 415, 416, 417]:
        return "continue", f"[WARN] HTTP= {status}, reason: {response.reason}" 
        
    elif status >= 400:
        return "break", f"[ERROR] HTTP= {status}, reason: {response.reason}"
