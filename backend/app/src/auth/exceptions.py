from exceptions import NotFound, Unauthorized


class UserNotFound(NotFound):
    def __init__(self):
        super().__init__(detail="User not found.")


class TokenUnauthorized(Unauthorized):
    def __init__(self):
        super().__init__(detail="Invalid token. Please sign-in again.")
