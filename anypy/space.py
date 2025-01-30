import requests

from anypy.type import Type 
from anypy.object import Object 

class Space:
    def __init__(self):
        self.headers = ''
        self.name = ''
        self.id = ''
        self.all_types = []
        pass

    def get_types(self,offset=0, limit=100):
        api_url = "http://localhost:31009/v1"
        url = f"{api_url}/spaces/{self.id}/types"
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self.headers,params=params)
        if response.status_code != 200:
            raise Exception("Error: ", response.json())

        data = response.json()["data"]
        self.all_types = []
        for item in data:
            self.all_types.append(Type(**item))
        return self.all_types 

    def get_type(self, type_name: str):
        if len(self.all_types) == 0:
            self.get_types()
        for type in self.all_types:
            if type.name == type_name:
                return type
        raise Exception("Type not found")




    def search_object(self, query, types=None, offset=0, limit=10):
        if self.id== "":
            raise Exception("Space ID is required")
        url = f"http://localhost:31009/v1/spaces/{self.id}/search"
        search_request = {
            "query": query,
        }
        # TODO: Add type filter 

        options = {"offset": offset, "limit": limit}
        response = requests.post(url, json=search_request, headers=self.headers, params=options)
        response_data = response.json()
        results=[]
        for data in response_data.get("data", []):
            new_item = Object()
            for key, value in data.items():
                if key == "blocks":
                    new_item.__dict__[key] = value
                else: 
                    new_item.__dict__[key] = value

            results.append(new_item)

        return results

    def create_object(self,obj:Object, type:Type):
        api_url = "http://localhost:31009/v1"
        url = f"{api_url}/spaces/{self.id}/objects"
        object_data = {
            "icon": obj.icon,
            "name": obj.name,
            "description": obj.description,
            "body": obj.body,
            "source": "",
            "template_id": "",
            "object_type_unique_key": type.unique_key,
        }
        response = requests.post(url, headers=self.headers, json=object_data)
        response.raise_for_status()  



    def __repr__(self):
        return f"<Space(name={self.name})>"


