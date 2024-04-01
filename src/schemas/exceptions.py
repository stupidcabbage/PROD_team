class BaseDBException(Exception):
    def __init__(self, details: str) -> None:
        seld.details = details
