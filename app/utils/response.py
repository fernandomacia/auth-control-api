# app/utils/response.py

"""Utility helpers for consistent JSON responses."""

from fastapi.responses import JSONResponse
from typing import Any, Dict


def json_response(
    success: bool,
    message: str,
    status_code: int = 200,
    data: Dict[str, Any] | None = None,
) -> JSONResponse:
    """Return a standardized JSON response payload.

    The function wraps the provided ``data`` in a ``success``/``message`` envelope
    and avoids mutable default arguments by defaulting ``data`` to ``None`` and
    replacing it with an empty dictionary.
    """
    payload = {
        "success": success,
        "message": message,
        "data": data or {},
    }
    return JSONResponse(content=payload, status_code=status_code)
