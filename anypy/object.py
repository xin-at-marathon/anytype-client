import requests
from copy import deepcopy


class Object:
    def __init__(self):
        self._headers = ''
        self.space_id = ''
        self.id = id
        self.source = ''
        self.type = 'Page'
        self.name = ''
        self.icon = ''
        self.body = ''
        self.description = ''
        self.blocks = []
        self.details = []
        self.layout = 'basic'
        self.root_id = ''
        self.snippet = ''
        self.space_id = ''

    def __repr__(self):
        return f"<Object(name={self.name},type_id={self.type})>"

    def delete(self):
        api_url = "http://localhost:31009/v1"
        url = f"{api_url}/spaces/{self.space_id}/objects/{self.id}"
        response = requests.delete(url, headers=self._headers)
        response.raise_for_status()  

    def create_child(self, obj, type):
        api_url = "http://localhost:31009/v1"
        url = f"{api_url}/spaces/{self.id}/objects"
        object_data = {
            "icon": obj.icon,
            "name": obj.name,
            "description": obj.description,
            "body": obj.body,
            "source": self.id,
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

    def add_title1(self, text):
        self.body += f"# {text}\n"

    def add_title2(self, text):
        self.body += f"## {text}\n"

    def add_title3(self, text):
        self.body += f"### {text}\n"

    def add_codeblock(self, code, language=""):
        self.body += f"``` {language}\n{code}\n```\n"

    def add_bullet(self, text):
        self.body += f"- {text}\n"

    def add_checkbox(self, text, checked=False):
        self.body += f"- [x] {text}\n" if checked else f"- [ ] {text}\n"





