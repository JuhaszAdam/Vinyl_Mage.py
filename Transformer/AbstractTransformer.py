from abc import ABC, abstractmethod

from Adapter.BertusAdapter import BertusAdapter


class Transformer(ABC):
    adapter = ""

    def __init__(self):
        self.adapter = BertusAdapter()

    @abstractmethod
    def transform(self, file_name):
        pass
