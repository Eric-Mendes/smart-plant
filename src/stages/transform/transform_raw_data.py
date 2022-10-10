from src.stages.contracts.extract_contract import ExtractContract
from src.stages.contracts.transform_contract import TransformContract
from src.errors.transform_error import TransformError


class TransformRawData:
    """Adicionar documentação na classe"""

    def transform(self, extract_contract: ExtractContract) -> TransformContract:
        """Será feita todas tranformações referente aos dados do thingsboard"""
        try:
            data_thingsboard = self.__transfor_date(extract_contract)

            transform_data_contract = TransformContract(
                data_thingsboard
            )
            return transform_data_contract
        except Exception as exception:
            raise TransformError(str(exception)) from exception

    def __transfor_date(self, extract_allure: ExtractContract):
        data_thingsboard = extract_allure[0]
        #print('\n================================')
        #print(data_thingsboard)
        return data_thingsboard

    