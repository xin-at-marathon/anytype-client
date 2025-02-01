import requests
from copy import deepcopy

from .type import Type
from .object import Object
from .template import Template
from .config import END_POINT


class Space:
    def __init__(self):
        self._headers = {}
        self.name = ""
        self.id = ""
        self.all_types = []

    def get_object(self, objectId: str, offset=0, limit=100) -> Object:
        url = END_POINT["getObject"].format(self.id, objectId)
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        obj = Object()
        for key, value in response_data.items():
            if key == "blocks":
                obj.__dict__[key] = value
            else:
                obj.__dict__[key] = value
        return obj

    def get_objects(self, offset=0, limit=100) -> list[Object]:
        url = END_POINT["getObjects"].format(self.id)
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
        self.all_types = results
        return results

    def get_types(self, offset=0, limit=100) -> list[Type]:
        url = END_POINT["getTypes"].format(self.id)
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        results = []
        for data in response_data.get("data", []):
            new_item = Type()
            for key, value in data.items():
                if key == "blocks":
                    new_item.__dict__[key] = value
                else:
                    new_item.__dict__[key] = value
            results.append(new_item)
        self.all_types = results
        return results

    def get_type(self, type_name: str) -> Type:
        if len(self.all_types) == 0:
            self.all_types = self.get_types()
        for type in self.all_types:
            if type.name == type_name:
                return type
        raise Exception("Type not found")

    def get_templates(self, type: Type, offset=0, limit=100) -> list[Template]:
        url = END_POINT["getTemplates"].format(self.id, type.id)
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        results = []
        for data in response_data.get("data", []):
            new_item = Template()
            for key, value in data.items():
                if key == "blocks":
                    new_item.__dict__[key] = value
                else:
                    new_item.__dict__[key] = value
            results.append(new_item)

        return results

    def search(self, query, offset=0, limit=10) -> list[Object]:
        if self.id == "":
            raise Exception("Space ID is required")
        url = END_POINT["search"].format(self.id)
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
                if key == "blocks":
                    new_item.__dict__[key] = value
                else:
                    new_item.__dict__[key] = value
            results.append(new_item)

        return results

    def global_search(self, query, offset=0, limit=10) -> list[Object]:
        url = END_POINT["globalSearch"]
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
        url = END_POINT["createObject"].format(self.id)
        object_data = {
            "icon": obj.icon,
            "name": obj.name,
            "description": obj.description,
            "body": obj.body,
            "source": "",
            "template_id": "",
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
