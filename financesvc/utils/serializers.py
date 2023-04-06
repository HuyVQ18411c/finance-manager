from datetime import datetime, date

from copy import deepcopy


class Serializer:
    def __init__(self, data: dict | list[dict], fields=[], exclude_fields=[]):
        self.data = data
        self.fields = fields
        self.exclude_fields = exclude_fields

    def _is_date_value(self, value):
        if(
            isinstance(value, date)
            or isinstance(value, datetime)
        ):
            return True
        return False

    def to_representation(self) -> dict | list[dict]:
        data: dict | list[dict] = deepcopy(self.data)

        if isinstance(data, dict):
            if self.fields:
                for field in self.fields:
                    if field not in data.keys():
                        del data[field]

            elif self.exclude_fields:
                for field in self.fields:
                    if field in data.keys():
                        del data[field]

            for key, value in data.items():
                if self._is_date_value(value):
                    data[key] = str(value)
        else:
            if self.fields:
                for row in data:
                    for field in self.fields:
                        if field not in row.keys():
                            del row[field]

            elif self.exclude_fields:
                for row in data:
                    for field in self.fields:
                        if field in row.keys():
                            del row[field]

            for row in data:
                for key, value in row.items():
                    if self._is_date_value(value):
                        row[key] = str(value)

        return data
