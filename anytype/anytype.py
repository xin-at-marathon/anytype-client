import os
import requests
import json

from .space import Space
from .object import Object
from .config import END_POINTS


class Anytype:
    def __init__(self) -> None:
        self.app_name = ""
        self.space_id = ""
        self.token = ""
        self.app_key = ""
        self._headers = {}

    def auth(self, force=False) -> None:
        userdata = self._get_userdata_folder()
        anytoken = os.path.join(userdata, "any_token.json")

        if force and os.path.exists(anytoken):
            os.remove(anytoken)

        if self.app_name == "":
            self.app_name = "Python API"
        if os.path.exists(anytoken):
            auth_json = json.load(open(anytoken))
            self.token = auth_json.get("session_token")
            self.app_key = auth_json.get("app_key")
            if self._validate_token():
                return

        url = END_POINTS["displayCode"]
        payload = {"app_name": self.app_name}
        response = requests.post(url, params=payload)
        response.raise_for_status()

        api_four_digit_code = input("Enter the 4 digit code: ")
        challenge_id = response.json().get("challenge_id")
        url = END_POINTS["auth"]
        payload = {"challenge_id": challenge_id, "code": api_four_digit_code}
        response = requests.post(url, params=payload)
        response.raise_for_status()

        with open(anytoken, "w") as file:
            json.dump(response.json(), file, indent=4)
        self.token = response.json().get("session_token")
        self.app_key = response.json().get("app_key")
        self._validate_token()

    def _validate_token(self) -> bool:
        url = END_POINTS["getSpaces"]
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}",
        }
        response = requests.get(url, headers=self._headers)
        if response.status_code != 200:
            return False
        else:
            return True

    def _get_userdata_folder(self) -> str:
        userdata = os.path.join(os.path.expanduser("~"), ".anytype")
        if not os.path.exists(userdata):
            os.makedirs(userdata)
        if os.name == "nt":
            os.system(f"attrib +h {userdata}")
        return userdata

    def get_spaces(self, offset=0, limit=10) -> list[Space]:
        url = END_POINTS["getSpaces"]
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        results = []
        for data in response.json().get("data", []):
            new_item = Space()
            new_item._headers = self._headers
            for key, value in data.items():
                new_item.__dict__[key] = value
            results.append(new_item)

        return results

    def create_space(self, name: str) -> Space:
        url = END_POINTS["createSpace"]
        object_data = {
            "name": name,
        }
        response = requests.post(url, headers=self._headers, json=object_data)
        response.raise_for_status()
        data = response.json()
        new_space = Space()
        new_space._headers = self._headers
        for key, value in data["space"].items():
            new_space.__dict__[key] = value

        return new_space

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
                new_item.__dict__[key] = value
            results.append(new_item)

        return results
