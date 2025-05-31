
import json

from Transformer.AbstractTransformer import Transformer


class JsonTransformer(Transformer):

    def transform(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return self.adapter.adapt(json.load(file))

        except FileNotFoundError as error:
            return error.strerror

