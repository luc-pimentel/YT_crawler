class NoAPIKeyException(Exception):
    """Exception raised when no API key is provided."""
    def __init__(self, message="No API key provided."):
        self.message = message
        super().__init__(self.message)