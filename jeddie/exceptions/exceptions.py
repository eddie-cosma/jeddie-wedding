from flask import g

class MissingConfigException(Exception):
    """Raised when the config file is not set in environmental variables"""
    pass


class InvalidRSVPException(Exception):
    """Raised whenever an invalid value is passed through an RSVP flow"""
    def __init__(self, message: str | None = None):
        self.message = g.language.get(message, None)
        super().__init__(self.message)
