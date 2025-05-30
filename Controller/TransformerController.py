import os

from Transformer.CsvTransformer import CsvTransformer
from Transformer.XmlTransformer import XmlTransformer


class TransformerController:

    def __init__(self):
        self.transformer = None

    def transform(self, file_name):
        extension = os.path.splitext(file_name)[1]

        if '.csv' in extension:
            self.transformer = CsvTransformer()
            return self.transformer.transform(file_name)

        if '.xml' in extension:
            self.transformer = XmlTransformer()
            return self.transformer.transform(file_name)

        if '.txt' in extension:
            print('Mit csináljak egy txt vel? nevezd át legalább. Nem fogok külön megírni egy analizálót hogy mégis mit akarsz megetetni velem.')
            return

        return f"Error: '{extension}' format is currently not supported."

