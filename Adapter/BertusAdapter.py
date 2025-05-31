from Adapter.AbstractAdapter import AbstractAdapter
from Model.Vinyl import Vinyl


class BertusAdapter(AbstractAdapter):
    config = {
        'current_bb_id': 486,
        'product.szorzo': 1.7,
    }

    def adapt(self, bertus_vinyl_data: dict):

        if ('Collection' in bertus_vinyl_data) and ('Links' in bertus_vinyl_data):
            return self.bertus_api_import(bertus_vinyl_data)

        vinyl = Vinyl

        for key, value in bertus_vinyl_data.items():
            if key in vinyl.attr:
                vinyl.attr[key] = value

        return vinyl

    def bertus_api_import(self, bertus_vinyl_data):

        vinyl_list = []

        for item in bertus_vinyl_data['Collection']:
            vinyl = Vinyl()
            vinyl.attr = {}
            self._set_default_attrs(vinyl)
            categories = ""
            name = ""

            for key, attr in item.items():
                if key == 'Id':
                    vinyl.attr['product.model'] = attr
                if key == 'Artist':
                    vinyl.attr['attr_values.eloado.hu'] = attr
                    name += f"{attr} - "
                if key == 'EANCode':
                    vinyl.attr['product.gtin'] = attr
                if key == 'GenreDescription':
                    categories += f"{attr}"
                if key == 'Title':
                    vinyl.attr['product_description.name.hu'] = name + attr
                if key == 'ListPrice':
                    vinyl.attr['product.alapar'] = attr['Amount']

            vinyl.attr['product_to_category.category_name'] = categories
            vinyl_list.append(vinyl)

        return vinyl_list

    def _set_default_attrs(self, vinyl):
        vinyl.attr['product.sku'] = self._generate_bb_id()
        vinyl.attr['product.status'] = 0
        vinyl.attr['product.free_shipping'] = False
        vinyl.attr['product.sort_order'] = 0
        vinyl.attr['product.manufacturer_id'] = "Bertus"
        vinyl.attr['product.szorzo'] = self.config['product.szorzo']

    def _generate_bb_id(self):
        self.config['current_bb_id'] += 1
        return 'BB' + str(self.config['current_bb_id']).rjust(6, '0')
