def network_error_handler(error):
    """
    Generate a simple message for network/request failure errors.

    args:
        error: The exception object from the network error.
        (e.g., error from except req.RequestException as error:)

    returns:
        str | None: A string message describing the network error, or None if there was no error.
    """
    if error is not None:
        return f"[ERROR] Network Error ({type(error).__name__}): {error}"
