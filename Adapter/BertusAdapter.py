from typing import Type

from Model.Vinyl import Vinyl


class BertusAdapter:

    @staticmethod
    def adapt(bertus_vinyl_data) -> Type[Vinyl]:
        vinyl = Vinyl

        for key, value in bertus_vinyl_data.items():
            if key in vinyl.attr:
                vinyl.attr[key] = value

        return vinyl
