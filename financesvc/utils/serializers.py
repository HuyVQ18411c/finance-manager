from datetime import datetime, date

from copy import deepcopy

from financesvc.domain.models import Base


class Serializer:
    def __init__(
        self,
        data: Base | list[Base],
        fields: list[str] = [],
        exclude_fields: list[str] = [],
        relationship_fields: list[str] = [],
        include_relationship: bool = False
    ):
        self.data = data
        self.serialized_data: dict | list[dict] = None
        self.fields = fields
        self.exclude_fields = exclude_fields
        self.relationship_fields = relationship_fields
        self._is_list = isinstance(data, list)
        # Include relationship should be use with dataset that has already been join by query
        # Instead of using lazy load, for performance.
        self._include_relationship = include_relationship

        # if not all([include_relationship, relationship_fields]):
        #     raise ValueError('Missing parameter when serializing objects.')

    @property
    def is_model_instance(self):
        if self._is_list and isinstance(self.data[0], Base):
            return True

        if isinstance(self.data, Base):
            return True

        return False

    def to_dict(self) -> dict | list[dict]:
        result = None
        if self.is_model_instance:
            if self._is_list:
                if self._include_relationship:
                    result = [instance.as_dict(True) for instance in self.data]
                else:
                    result = [instance.as_dict() for instance in self.data]
            else:
                if self._include_relationship:
                    result = self.data.as_dict(True)
                else:
                    result = self.data.as_dict()

        return result

    def _is_date_value(self, value):
        if(
            isinstance(value, date)
            or isinstance(value, datetime)
        ):
            return True
        return False

    def _seralize_fields(self, data: dict) -> dict:
        """
        Serialize fields with data types:
        - Datetime
        - Base (Model)
        Parameters
        ----------
        data (dict)

        Returns
        -------

        """
        for key, value in data.items():
            if self._is_date_value(value):
                data[key] = str(value)

            if self._include_relationship and isinstance(value, Base):
                data[key] = Serializer(value).to_dict()
        return data

    def to_representation(self) -> dict | list[dict]:
        if not self.data:
            return []

        data: dict | list[dict] = self.to_dict()

        if isinstance(data, dict):
            if self.fields:
                # Since del will change keys() values during iteration
                # Use list to enforce a copy of that list
                for field in list(data.keys()):
                    if field not in self.fields:
                        del data[field]

            elif self.exclude_fields:
                for field in self.exclude_fields:
                    if field in list(data.keys()):
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
