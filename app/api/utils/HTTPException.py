class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str, code: int | None = None):
        self.detail = detail
        self.code = code
        self.status_code = status_code
