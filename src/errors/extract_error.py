class ExtractError(Exception):
    'Classe para tratamento de exception para parte referente a Extração do ETL'
    def __init__(self, message:str) -> None:
        super().__init__(message)
        self.message = message
        self.error_type = 'ExtractError'
