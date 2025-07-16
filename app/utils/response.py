# app/utils/response.py

from fastapi.responses import JSONResponse
from typing import Any, Dict


def json_response(
    success: bool,
    message: str,
    status_code: int = 200,
    data: Dict[str, Any] = {}
) -> JSONResponse:
    """
    Generate a consistent JSON response with a 'data' wrapper.
    
    :param success: Whether the response indicates success.
    :param message: Human-readable message.
    :param status_code: HTTP status code.
    :param data: Optional additional data to include under the 'data' key.
    :return: JSONResponse object.
    """
    payload = {
        "success": success,
        "message": message,
        "data": data
    }
    return JSONResponse(content=payload, status_code=status_code)
