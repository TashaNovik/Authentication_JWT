
class AuthError(Exception):
    def __init__(self, detail: str = "Authentication Error"):
        self.detail = detail
        super().__init__(detail)

class InvalidTokenError(AuthError):
    def __init__(self, detail: str = "Invalid Token"):
        super().__init__(detail)

class TokenExpiredError(InvalidTokenError):
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(detail)

class UserIdNotFoundError(InvalidTokenError):
     def __init__(self, detail: str = "User ID not found in token"):
        super().__init__(detail)

class InvalidSignatureError(InvalidTokenError):
     def __init__(self, detail: str = "Invalid token signature or format"):
        super().__init__(detail)