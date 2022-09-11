from typing import Dict, Optional, Union, List


class AppError(Exception):
    status_code = 500

    @property
    def code(self):
        return f"{self.__class__.__name__.lower().replace('error', '')}_error"

    def get_data(self) -> Dict[str, str]:
        return {
            "code": self.code,
            "detail": "An error occurred",
        }

    def get_status_code(self):
        return self.status_code


class ValidationError(AppError):
    status_code = 400

    def __init__(
        self, error_data: Optional[Union[Dict[str, str], List[Dict[str, str]]]] = None
    ):
        self.error_data = error_data or {
            "detail": "Validation error",
        }

    def get_data(self) -> Dict[str, str]:
        return {
            "code": self.code,
            "error": self.error_data,
        }


class LoginError(AppError):
    status_code = 401

    def get_data(self) -> Dict[str, str]:
        return {
            "code": self.code,
            "detail": "Invalid credentials",
        }
