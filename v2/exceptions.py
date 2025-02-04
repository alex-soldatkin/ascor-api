from fastapi import HTTPException
from typing import Any, Optional, Dict

class ASCORException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "details": details or {}
            }
        )

class DataValidationError(ASCORException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=422, message=message, details=details)

class DataNotFoundError(ASCORException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=404, message=message, details=details)
