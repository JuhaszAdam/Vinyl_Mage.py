import ast
import json
import os
import sys
import time
import urllib.request
from urllib.error import HTTPError

import requests
from dateutil import parser

from Adapter.AbstractAdapter import AbstractAdapter
from Model.Vinyl import Vinyl


class BertusAdapter(AbstractAdapter):
    config = {}

    def __init__(self):
        try:
            with open('Resources/config.json', 'r', encoding='utf-8') as file:
                self.config = json.load(file)

        except FileNotFoundError as e:
            print('Configuration file not found! (Resources/config.py)')
            raise e

    def adapt(self, bertus_vinyl_data: dict):

        if (type(bertus_vinyl_data) == dict and 'Collection' in bertus_vinyl_data) and ('Links' in bertus_vinyl_data):
            return self.bertus_api_import(bertus_vinyl_data)

        if type(bertus_vinyl_data) == list and "\ufeffArtNo" in bertus_vinyl_data[0]:
            return self.bertus_wishlist_import(bertus_vinyl_data)

        vinyl = Vinyl

        for key, value in bertus_vinyl_data.items():
            if key in vinyl.attr:
                vinyl.attr[key] = value

        return vinyl

    def bertus_wishlist_import(self, bertus_vinyl_data):
        vinyl_list = []
        for wishlist_item in bertus_vinyl_data:
            account = self.config['account_id']
            response = self._fetch_from_api(f'/api/v1/accounts/{account}/articles/{wishlist_item['\ufeffArtNo']}')
            if response == 404:
                print(
                    f'HTTP 404 error (Not Found) at \nhttps://my.bertus.com/detail/{wishlist_item['\ufeffArtNo']}\n')
                print(f'Artist: {wishlist_item.get('Artist')}\n')
                print(f'Title: {wishlist_item.get('Title')}\n')
                continue
            response = json.loads(response.read().decode('utf-8'))

            vinyl_list.append(self._do_create_vinyl(response))

        return vinyl_list

    def bertus_api_import(self, bertus_vinyl_data):
        vinyl_list = []

        for item in bertus_vinyl_data['Collection']:
            vinyl_list.append(self._do_create_vinyl(item))

        return vinyl_list

    def _do_create_vinyl(self, item):
        vinyl = Vinyl()
        vinyl.attr = {}
        self._set_default_attrs(vinyl)
        categories = []
        category_ids = []
        short_description = []
        label = []
        description_tags = []
        name = ""
        for key, attr in item.items():
            if key == 'ReleaseDate':
                short_description.insert(0, f"Megjelenés: {parser.parse(attr).strftime('%Y. %m. %d')}")
            if key == 'Artist':
                vinyl.attr['attr_values.eloado.hu'] = attr
                name += f"{attr} - "
                short_description.insert(1, f"Előadó: {attr}")
                description_tags.insert(1, attr)
            if key == 'Genre':
                category_key = self.config['bertus_categories'].get(attr)
                if category_key:
                    categories.append(self.config['bb_categories'][str(category_key)])
                    category_ids.append(str(category_key))
                    category_name = self.config['bb_categories'][str(category_key)]
                    description_tags.insert(2, category_name)
                    short_description.insert(2, f"Műfaj: {category_name}")
                else:
                    print(f'Genre key not configured: {attr}')
            if key == 'MediaId':
                short_description.insert(3, f"Formátum: {attr}")
            if key == 'OriginDescription':
                short_description.insert(4, f"Származás: {attr}")
            if key == 'MajorDescription':
                if not str(attr) == "0":
                    label.insert(0, str(attr))
                    vinyl.attr['product.manufacturer_id'] = str(attr)

            if key == 'LabelDescription':
                label.insert(1, str(attr))
                description_tags.insert(0, str(attr))

            if key == 'Id':
                vinyl.attr['product.model'] = attr
                if self.config['_get_info_from_api']['tracklist'] == "1":
                    tracklist = self._fetch_from_api(f'/api/v1/articles/{attr}/tracks').read()
                    tracklist = self._generate_html_from_tracklist(tracklist)
                    vinyl.attr['product_description.custom_content.hu'] = tracklist
            if key == 'EANCode':
                vinyl.attr['product.gtin'] = attr
            if key == 'Title':
                vinyl.attr['product_description.name.hu'] = name + attr
            if key == 'ListPrice':
                vinyl.attr['product.alapar'] = attr['Amount']

            if key == 'Links':
                for subkey, link in attr.items():
                    if subkey == 'dvdInfo' and self.config['_get_info_from_api']['dvdInfo'] == "1":
                        dvd_info = self._fetch_from_api(link['Href']).read()
                        vinyl.attr['dvdInfo'] = dvd_info
                    if subkey == 'extraInfo' and self.config['_get_info_from_api']['extraInfo'] == "1":
                        dvd_info = self._fetch_from_api(link['Href']).read()
                        vinyl.attr['extraInfo'] = dvd_info
                    if subkey == 'classicalInfo' and self.config['_get_info_from_api']['classicalInfo'] == "1":
                        dvd_info = self._fetch_from_api(link['Href']).read()
                        vinyl.attr['classicalInfo'] = dvd_info
                    if (subkey == 'cover'
                            and not link['Href'] == 'https://my.bertus.com/assets/images/imcomingsoonbertus.svg'):
                        file_name = os.path.basename(link['Href'])
                        pre, ext = os.path.splitext(file_name)
                        file_name = pre + '.jpg'
                        if self.config['_get_info_from_api']['getMainImage'] == "1":
                            img_data = requests.get(link['Href']).content
                            with open(f"Resources/_upload_images/{file_name}", 'wb') as handler:
                                handler.write(img_data)
                            handler.close()
                        vinyl.attr['product.image'] = 'product/' + file_name
        short_description.insert(6, f"Kiadó: {" - ".join(label)}")
        vinyl.attr['product_to_category.category_name'] = ";".join(categories)
        vinyl.attr['product_to_category.category_id'] = ";".join(category_ids)
        vinyl.attr['product_description.meta_keywords.hu'] = ",".join(description_tags)
        vinyl.attr['product_description.short_description.hu'] = "\n".join(short_description)
        vinyl.attr['product_description.parameters.hu'] = "\n".join(short_description)

        return vinyl

    def _set_default_attrs(self, vinyl):
        vinyl.attr['product.sku'] = self._generate_bb_id()
        vinyl.attr['product.status'] = 0
        vinyl.attr['product.free_shipping'] = False
        vinyl.attr['product.sort_order'] = 0
        vinyl.attr['product.product_ring_id'] = 0
        vinyl.attr['product.szorzo'] = self.config['product.szorzo']
        vinyl.attr['product_description.meta_description.hu'] = "[CATEGORY]"
        vinyl.attr['product_description.custom_title.hu'] = "[PRODUCT]"
        vinyl.attr['product_description.quantity_name.hu'] = "db"
        vinyl.attr['product_description.custom_content_title.hu'] = "Tracklista"
        ##testing
        # vinyl.attr['product_description.custom_content.title.hu'] = "product_description.custom_content.title.hu"
        # vinyl.attr['product_description.custom_content.title'] = "product_description.custom_content.title"
        # vinyl.attr['product_description.custom_content_title'] = "product_description.custom_content_title"
        # vinyl.attr['product_tags'] = "product_tags"
        # vinyl.attr['product_tags.hu'] = "product_tags.hu"
        # vinyl.attr['product.custom_content1'] = "product.custom_content1"
        # vinyl.attr['product.custom_content1.hu'] = "product.custom_content1.hu"
        # vinyl.attr['product_custom_content1'] = "product_custom_content1"
        # vinyl.attr['product_custom_content1.hu'] = "product_custom_content1.hu"

    def _generate_bb_id(self):
        self.config['current_bb_id'] += 1
        return 'BB' + str(self.config['current_bb_id']).rjust(6, '0')

    def _fetch_from_api(self, url):
        original_url = url
        try:
            headers = {
                'Cache-Control': 'no-cache',
                'Authorization': self.config['Authorization'],
                'Ocp-Apim-Subscription-Key': self.config['Ocp-Apim-Subscription-Key']
            }
            url = f"https://myapi.bertus.com/prod{url}"
            req = urllib.request.Request(url, headers=headers)

            req.get_method = lambda: 'GET'
            response = urllib.request.urlopen(req)

            return response
        except HTTPError as e:
            status_code = e.code
            if status_code == 404:
                return 404
            if status_code == 429:
                self._verbose_sleep(int(e.hdrs["Retry-After"]))

                return self._fetch_from_api(original_url)
        except Exception as e:
            print(e)

    @staticmethod
    def _generate_html_from_tracklist(tracklist):
        html_tracklist = ""
        ordered_tracks = {}
        tracklist = ast.literal_eval(tracklist.decode('utf-8'))
        for track in tracklist['Tracks']:
            unit_number = str(track['UnitNumber'])
            if not unit_number in ordered_tracks:
                ordered_tracks[unit_number] = []
            ordered_tracks[unit_number].append(track['Description'])

        for i, unit in ordered_tracks.items():
            html_tracklist += f"<hr><p> - {i} - </p>"
            html_tracklist += "<ol>"
            for track in unit:
                html_tracklist += f"<li>{track}"
            html_tracklist += "</ol>"

        return html_tracklist

    @staticmethod
    def _verbose_sleep(seconds):
        for remaining in range(seconds, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("Api lockout, {:2d} seconds remaining.".format(remaining))
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r")
        sys.stdout.write("")
        sys.stdout.flush()
