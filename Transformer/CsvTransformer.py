import csv

from Transformer.AbstractTransformer import Transformer


class CsvTransformer(Transformer):
    config = {
        'newline': '',
        'encoding': 'utf-8'
    }

    def transform(self, file_name):
        try:
            with open(file_name, newline=self.config['newline'], encoding=self.config['encoding']) as file:
                dialect = csv.Sniffer().sniff(file.read())
                file.seek(0, 0)

                has_header = csv.Sniffer().has_header(file.read())
                file.seek(0, 0)
                reader = csv.reader(file, dialect)

                vinyl_list = []
                headers = {}
                for row in reader:
                    if has_header:
                        headers = row
                        has_header = False
                        continue

                    vinyl_list.append(dict(zip(headers, row)))

                return self.adapter.adapt(vinyl_list)

        except FileNotFoundError as error:
            return error.strerror
