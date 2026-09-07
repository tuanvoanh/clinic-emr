import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

ERROR_MAPPING_FILE = Path(__file__).parent / "error_mapping.json"

def load_error_mapping() -> Dict[str, Any]:
    """
    Loads error mapping rules from error_mapping.json if present.
    """
    if ERROR_MAPPING_FILE.exists():
        try:
            with open(ERROR_MAPPING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load error_mapping.json: {e}")
    return {}

ERROR_MAPPING = load_error_mapping()

def get_error_message(error_code: str) -> Optional[str]:
    """
    Looks up the default English message for a given error code in error_mapping.json.
    """
    for section in ERROR_MAPPING.values():
        if isinstance(section, dict) and error_code in section:
            return section[error_code]
    return None

class AppException(Exception):
    """
    Custom application exception for domain/business errors.
    Automatically retrieves the default description from error_mapping.json if message is omitted.
    """
    def __init__(
        self,
        error_code: str,
        status_code: int = 400,
        message: Optional[str] = None,
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        self.error_code = error_code
        self.status_code = status_code
        self.message = message or get_error_message(error_code) or error_code
        self.errors = errors if errors is not None else []
        super().__init__(self.message)

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handles custom application / business exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "status_code": exc.status_code,
            "error_code": exc.error_code,
            "message": exc.message,
            "errors": exc.errors
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles Pydantic validation errors and formats them cleanly.
    """
    errors = []
    pydantic_msgs = ERROR_MAPPING.get("pydantic_validation_codes", {})
    
    for error in exc.errors():
        loc = error.get("loc", [])
        field = ".".join(str(l) for l in loc if l not in ("body", "query", "path"))
        code = error.get("type", "invalid_value")
        # Use mapped error message if available, otherwise fallback to Pydantic msg
        msg = pydantic_msgs.get(code, error.get("msg", "Invalid value."))
        
        errors.append({
            "field": field,
            "code": code,
            "message": msg
        })
        
    global_msgs = ERROR_MAPPING.get("global_errors", {})
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "status_code": 400,
            "error_code": "validation_error",
            "message": global_msgs.get("validation_error", "Invalid input data."),
            "errors": errors
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handles standard HTTP exceptions (e.g. 404, 403, 400 manually raised).
    If exc.detail matches a registered error code, maps it accordingly.
    """
    detail = exc.detail if exc.detail else ""
    mapped_msg = get_error_message(detail)
    
    if mapped_msg is not None:
        error_code = detail
        message = mapped_msg
    else:
        error_code = "http_error"
        message = detail or "HTTP request error."

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "status_code": exc.status_code,
            "error_code": error_code,
            "message": message,
            "errors": []
        }
    )

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catches all unhandled 500 server errors to prevent stack trace leaks.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    global_msgs = ERROR_MAPPING.get("global_errors", {})
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "status_code": 500,
            "error_code": "internal_server_error",
            "message": global_msgs.get("internal_server_error", "Internal server error. Please try again later."),
            "errors": []
        }
    )

def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

