def success_response(data, status=200):
    return {
        "success": True,
        "data": data,
    }, status


def error_response(message, status=400):
    return {
        "success": False,
        "message": message,
    }, status
