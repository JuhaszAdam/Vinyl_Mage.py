import os

from Transformer.CsvTransformer import CsvTransformer
from Transformer.JsonTransformer import JsonTransformer
from Transformer.XmlTransformer import XmlTransformer


class TransformerController:

    @staticmethod
    def transform(file_name):
        extension = os.path.splitext(file_name)[1]

        match extension:
            case '.csv':
                return CsvTransformer().transform(file_name)

            case '.xml':
                return XmlTransformer().transform(file_name)

            case '.json':
                return JsonTransformer().transform(file_name)

            case _:
                return f"Error: '{extension}' format is currently not supported."

    @staticmethod
    def export(vinyl_list, location, filename):
        XmlTransformer().export(vinyl_list, location, filename)
