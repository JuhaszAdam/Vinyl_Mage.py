import xml.etree.ElementTree as ET
from typing import Dict, Any

from Adapter.BertusAdapter import BertusAdapter
from Model.Vinyl import Vinyl


class XmlTransformer:
    adapter = BertusAdapter

    def transform(self, file_name):
        try:
            file = ET.parse(file_name)

            vinyl_list = {}
            i = 0

            for row in file.getroot():
                vinyl_list[i] = self.create_vinyl_from_row(row)
                i += 1

            return vinyl_list

        except FileNotFoundError as error:
            return error.strerror

    def create_vinyl_from_row(self, row):
        paired_list: dict = {}
        for attrib in row:
            paired_list[attrib.tag] = attrib.text

        return self.adapter.adapt(paired_list)
