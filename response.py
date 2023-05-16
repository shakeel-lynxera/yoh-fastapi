def api_response(message="something went wrong. try again later.", data=None, status_code=400):
    return {
        "message": message,
        "data": {} if data is None else data,
        "status_code": status_code
    }
