
from .extractor_thingsboard import DriversThingsBoard


def test_extractor_thingsboard():
    """teste de extração de arquivos no formato xlsx"""
    extractor_pandas = DriversThingsBoard
    extractor_pandas.extract_thingsboard()
    print(extractor_pandas.extract_thingsboard())
    # assert 1==1
    # assert isinstance(df_rel_mensal, pd.DataFrame)
