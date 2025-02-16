class ResponseHasError(Exception):
    """Custom exception for API errors."""
    def __init__(self, response):
        self.status_code = response.status_code
        if self.status_code != 200:
            raise Exception(response.json()["error"]["message"])
