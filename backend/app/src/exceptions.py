from fastapi import HTTPException, status


class NotFound(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class Unauthorized(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class Forbidden(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
