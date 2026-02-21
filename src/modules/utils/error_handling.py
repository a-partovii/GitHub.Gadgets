def network_error_handler(error):
    """
    Generate a simple message for network/request failure errors.

    args:
        error: The exception object from the network error.
        (e.g., error from except req.RequestException as error:)

    returns: (tuplebool, str): 
            - success (bool): False if there was a network error, otherwise True.
            - message (str): A string message describing the network error.
    """
    if error is not None:
        message = f"[ERROR] Network Error ({type(error).__name__}): {error}"
        return False, message
    return True, "[OK]"

def response_error_handler(response):
    """
    Handles GitHub HTTP response errors only.
    Does nothing for successful responses.
    """
    if response is None:
        return

    # Response handling
    status = response.status_code
    remaining = response.headers.get("X-RateLimit-Remaining", "unknown")

    # Token error
    if status == 401:
        return "[ERROR] Invalid or Expired Token."

    # Rate limit reached
    elif status == 403 or (remaining != "unknown" and int(remaining) <= 5):
        return (f'[WARN] Token RateLimit is Close to Being Reached, Remaining: "{remaining}"' +
                         "\n Take a break and continue later...")

    # Not found
    elif status == 404:
       return "[WARN] Resource not found"

    # GitHub internal error (server)
    elif status >= 500:
        return f"[ERROR] Server error {status}"

    # other
    elif status >= 400:
        return f"[ERROR] http= {status}, reason: {response.reason}"
