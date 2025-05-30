from typing import Type

from Adapter.AbstractAdapter import AbstractAdapter
from Model.Vinyl import Vinyl


class BertusAdapter(AbstractAdapter):

    def adapt(self, bertus_vinyl_data: dict) -> Type[Vinyl]:
        vinyl = Vinyl

        for key, value in bertus_vinyl_data.items():
            if key in vinyl.attr:
                vinyl.attr[key] = value

        return vinyl
