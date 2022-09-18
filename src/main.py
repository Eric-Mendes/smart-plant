#pylint: disable-all

from .PDF_Handler.getTicker import genTicker
import json

def main(path):
    df, costs = genTicker(path)

    my_dict = df.to_dict(orient="records")

    return my_dict


