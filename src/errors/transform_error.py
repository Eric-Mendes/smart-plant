class TransformError(Exception):
    '''Tratamento de erro para parte de Extração '''
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.error_type = 'Transform Error'