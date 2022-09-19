from datetime import datetime
import datetime as date



class MainPipeline:
    ''' Colocar doctring'''
    @classmethod
    def run_pipeline(cls) -> None:
        ''' Colocar doctring'''
        inicio = date.datetime.now()
        print(f"Inicio: {date.datetime.now()}")

    
        print(f"Fim: {date.datetime.now()}")
        fim = date.datetime.now()
        print(f"Diferenca de data {fim-inicio} ")
 
