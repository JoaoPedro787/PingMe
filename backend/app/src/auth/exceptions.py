from exceptions import NotFound, Unauthorized


class UserNotFound(NotFound):
    def __init__(self):
        super().__init__(detail="User not found.")


class TokenInvalid(Unauthorized):
    def __init__(self):
        super().__init__(detail="Invalid token. Please sign-in again.")


class TokenExpired(Unauthorized):
    def __init__(self):
        super().__init__(detail="Expired token. Please sign-in again.")
