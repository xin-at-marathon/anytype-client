import requests
from copy import deepcopy

from .type import Type
from .object import Object
from .template import Template
from .config import END_POINTS


class Space:
    def __init__(self):
        self._headers = {}
        self.name = ""
        self.id = ""
        self._all_types = []

    def get_object(self, objectId: str, offset=0, limit=100) -> Object:
        url = END_POINTS["getObject"].format(self.id, objectId)
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        obj = Object()
        for key, value in response_data.items():
            obj.__dict__[key] = value
        return obj

    def get_objects(self, offset=0, limit=100) -> list[Object]:
        url = END_POINTS["getObjects"].format(self.id)
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        results = []
        for data in response_data.get("data", []):
            new_item = Object()
            new_item._headers = self._headers
            for key, value in data.items():
                if key == "blocks":
                    new_item.__dict__[key] = value
                else:
                    new_item.__dict__[key] = value
            results.append(new_item)
        self._all_types = results
        return results

    def get_types(self, offset=0, limit=100) -> list[Type]:
        url = END_POINTS["getTypes"].format(self.id)
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        results = []
        for data in response_data.get("data", []):
            new_item = Type()
            new_item._headers = self._headers
            new_item.space_id = self.id
            for key, value in data.items():
                new_item.__dict__[key] = value
            results.append(new_item)
        self._all_types = results
        return results

    def get_type(self, type_name: str) -> Type:
        if len(self._all_types) == 0:
            self._all_types = self.get_types()
        for type in self._all_types:
            if type.name == type_name:
                return type
        raise ValueError("Type not found")

    def search(self, query, offset=0, limit=10) -> list[Object]:
        if self.id == "":
            raise ValueError("Space ID is required")
        url = END_POINTS["search"].format(self.id)
        search_request = {
            "query": query,
        }
        options = {"offset": offset, "limit": limit}
        response = requests.post(
            url, json=search_request, headers=self._headers, params=options
        )
        response.raise_for_status()

        response_data = response.json()
        results = []
        for data in response_data.get("data", []):
            new_item = Object()
            new_item._headers = self._headers
            for key, value in data.items():
                new_item.__dict__[key] = value
            results.append(new_item)

        return results

    def global_search(self, query, offset=0, limit=10) -> list[Object]:
        url = END_POINTS["globalSearch"]
        options = {"offset": offset, "limit": limit}
        search_request = {
            "query": query,
        }
        response = requests.post(
            url, json=search_request, headers=self._headers, params=options
        )
        response.raise_for_status()

        response_data = response.json()
        results = []

        for data in response_data.get("data", []):
            new_item = Object()
            new_item._headers = self._headers
            for key, value in data.items():
                if key == "blocks":
                    new_item.__dict__[key] = value
                else:
                    new_item.__dict__[key] = value
            results.append(new_item)

        return results

    def create_object(self, obj: Object, type: Type) -> Object:
        url = END_POINTS["createObject"].format(self.id)
        object_data = {
            "icon": obj.icon,
            "name": obj.name,
            "description": obj.description,
            "body": obj.body,
            "source": "",
            "template_id": type.template_id,
            "object_type_unique_key": type.unique_key,
        }

        obj_clone = deepcopy(obj)
        obj_clone._headers = self._headers
        obj_clone.space_id = self.id
        response = requests.post(url, headers=self._headers, json=object_data)
        response.raise_for_status()
        for key, value in response.json()["object"].items():
            obj_clone.__dict__[key] = value
        return obj_clone

    def __repr__(self):
        return f"<Space(name={self.name})>"
