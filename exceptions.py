class LogoutException(Exception):
    def __init__(self, message="Требуется обновить креды"):
        self.message = message
        super().__init__(self.message)
        