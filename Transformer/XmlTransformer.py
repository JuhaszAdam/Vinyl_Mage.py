import xml.etree.ElementTree as ET

from Transformer.AbstractTransformer import Transformer


class XmlTransformer(Transformer):

    def transform(self, file_name):
        try:
            file = ET.parse(file_name)

            vinyl_list = []
            for row in file.getroot():
                vinyl_list.append(self.create_vinyl_from_row(row))

            return vinyl_list

        except FileNotFoundError as error:
            return error.strerror

    def create_vinyl_from_row(self, row):
        paired_list: dict = {}
        for attrib in row:
            paired_list[attrib.tag] = attrib.text

        return self.adapter.adapt(paired_list)

    @staticmethod
    def export(vinyl_list: list):
        products = ET.Element('products')
        for vinyl in vinyl_list:
            product = ET.SubElement(products, 'product')
            for key, attr in vinyl.attr.items():
                ET.SubElement(product, key).text = str(attr)

        tree = ET.ElementTree(products)
        ET.indent(tree, '    ')
        tree.write('Resources/Test_Import.xml', encoding="utf-8", xml_declaration=True)
