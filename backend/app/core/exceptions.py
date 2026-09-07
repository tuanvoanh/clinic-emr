import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

class ErrorCode(Enum):
    """
    Single Source of Truth for system and business error codes.
    Tuple format: (code: str, default_message: str, default_status_code: int)
    """
    # Global framework errors
    VALIDATION_ERROR = ("validation_error", "Invalid input data.", 400)
    HTTP_ERROR = ("http_error", "HTTP request error.", 400)
    INTERNAL_SERVER_ERROR = ("internal_server_error", "Internal server error. Please try again later.", 500)

    # Business domain errors
    INVALID_ICD10_CODE = ("invalid_icd10_code", "Invalid ICD-10 code or it does not exist in the system.", 400)
    PATIENT_NOT_FOUND = ("patient_not_found", "Patient not found.", 404)

    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

    @classmethod
    def from_code(cls, code_str: str) -> Optional["ErrorCode"]:
        """
        Lookup ErrorCode Enum by its string code value.
        """
        for item in cls:
            if item.code == code_str:
                return item
        return None

# User-friendly descriptions for standard Pydantic validation error types
PYDANTIC_ERROR_MESSAGES: Dict[str, str] = {
    "missing": "This field is required and cannot be empty.",
    "string_pattern_mismatch": "Input format is invalid.",
    "string_too_short": "Input string is too short.",
    "string_too_long": "Input string exceeds maximum length.",
    "int_parsing": "Input must be a valid integer.",
    "float_parsing": "Input must be a valid float number.",
    "value_error": "Invalid value."
}

class AppException(Exception):
    """
    Custom application exception for domain/business errors.
    Automatically extracts code, message, and status_code from the ErrorCode Enum.
    """
    def __init__(
        self,
        error_code: Union[ErrorCode, str],
        status_code: Optional[int] = None,
        message: Optional[str] = None,
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        if isinstance(error_code, ErrorCode):
            self.error_code: str = error_code.code
            self.status_code: int = status_code if status_code is not None else error_code.status_code
            self.message: str = message if message is not None else error_code.message
        else:
            self.error_code: str = str(error_code)
            matched = ErrorCode.from_code(self.error_code)
            self.status_code: int = status_code if status_code is not None else (matched.status_code if matched else 400)
            self.message: str = message if message is not None else (matched.message if matched else self.error_code)

        self.errors: List[Dict[str, Any]] = errors if errors is not None else []
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
    Handles Pydantic validation errors and formats them into a clean 400 Bad Request response.
    """
    errors = []
    for error in exc.errors():
        loc = error.get("loc", [])
        field = ".".join(str(l) for l in loc if l not in ("body", "query", "path"))
        code = error.get("type", "invalid_value")
        msg = PYDANTIC_ERROR_MESSAGES.get(code, error.get("msg", "Invalid value."))
        
        errors.append({
            "field": field,
            "code": code,
            "message": msg
        })
        
    return JSONResponse(
        status_code=ErrorCode.VALIDATION_ERROR.status_code,
        content={
            "status": "error",
            "status_code": ErrorCode.VALIDATION_ERROR.status_code,
            "error_code": ErrorCode.VALIDATION_ERROR.code,
            "message": ErrorCode.VALIDATION_ERROR.message,
            "errors": errors
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handles standard HTTP exceptions (e.g. 404, 403, 400 manually raised).
    If exc.detail matches a registered ErrorCode, maps it accordingly.
    """
    detail = str(exc.detail) if exc.detail else ""
    matched = ErrorCode.from_code(detail)
    
    if matched is not None:
        error_code = matched.code
        message = matched.message
    else:
        error_code = ErrorCode.HTTP_ERROR.code
        message = detail or ErrorCode.HTTP_ERROR.message

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
    return JSONResponse(
        status_code=ErrorCode.INTERNAL_SERVER_ERROR.status_code,
        content={
            "status": "error",
            "status_code": ErrorCode.INTERNAL_SERVER_ERROR.status_code,
            "error_code": ErrorCode.INTERNAL_SERVER_ERROR.code,
            "message": ErrorCode.INTERNAL_SERVER_ERROR.message,
            "errors": []
        }
    )

def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)


