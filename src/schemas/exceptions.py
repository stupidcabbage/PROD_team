class BaseDBException(Exception):
    def __init__(self,
                 details: str = "Произошла ошибка при обработке.") -> None:
        self.details = details
