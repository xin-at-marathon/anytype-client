import requests


class Object:
    def __init__(self):
        self._headers = ''
        self._space_id = ''
        self.id = id
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
        url = f"{api_url}/spaces/{self._space_id}/objects/{self.id}"
        response = requests.delete(url, headers=self._headers)
        response.raise_for_status()  

        pass
