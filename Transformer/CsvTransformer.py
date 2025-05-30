import csv

from Model.Vinyl import Vinyl


class CsvTransformer:
    config = {
        'newline': '',
        'delimiter': ' ',
        'quotechar': '|',
        'encoding': 'utf-8'
    }

    def transform(self, file_name):
        try:
            with open(file_name, newline=self.config['newline'], encoding=self.config['encoding']) as file:
                dialect = csv.Sniffer().sniff(file.read())
                file.seek(0, 0)

                has_header = csv.Sniffer().has_header(file.read())
                file.seek(0, 0)
                reader = csv.reader(
                    file,
                    dialect
                )

                vinyl_list = {}
                headers = {}
                i = 0
                for row in reader:
                    if has_header:
                        headers = row
                        has_header = False
                        continue

                    vinyl_list[i] = self.create_vinyl_from_row(row, headers)
                    i+=1

                return vinyl_list

        except FileNotFoundError as error:
            return error.strerror

    def create_vinyl_from_row(self, row, headers):
        # May not be enough. See: izip
        paired_list = dict(zip(headers, row))

        return row
        new_vinyl = Vinyl

        new_vinyl.product_sku = row[0]

