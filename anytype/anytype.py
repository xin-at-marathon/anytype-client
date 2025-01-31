import os
import requests
import json
import plataform

from .space import Space
from .const import CONST


class Anytype:
    def __init__(self) -> None:
        self.app_name = ""
        self.space_id = ""
        self.token = ""
        self.app_key = ""
        self._headers = {}

    def auth(self) -> None:
        userdata = self._get_userdata_folder()
        anytoken = os.path.join(userdata, "any_token.json")
        if self.app_name == "":
            self.app_name = CONST.get("apiAppName")

        api_url = CONST.get("apiUrl")
        if os.path.exists(anytoken):
            auth_json = json.load(open(anytoken))
            self.token = auth_json.get("session_token")
            self.app_key = auth_json.get("app_key")
            if self._validate_token():
                return

        url = f"{api_url}/auth/display_code?app_name={self.app_name}"
        response = requests.post(url)
        if response.status_code != 200:
            raise Exception("Error: ", response.json())

        api_four_digit_code = input("Enter the 4 digit code: ")
        challenge_id = response.json().get("challenge_id")
        parameters = {
            "challenge_id": challenge_id,
            "code": api_four_digit_code,
        }
        url = f"{api_url}/auth/token"
        response = requests.post(url, json=parameters)
        if response.status_code != 200:
            raise Exception("Error: ", response.json())

        with open(anytoken, "w") as file:
            json.dump(response.json(), file, indent=4)
        self.token = response.json().get("session_token")
        self.app_key = response.json().get("app_key")
        self._validate_token()

    def _validate_token(self) -> bool:
        api_url = CONST.get("apiUrl")
        url = f"{api_url}/spaces"
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}",
        }
        try:
            response = requests.get(url, headers=self._headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Token validation failed: {e}")
            return False

    def _get_userdata_folder(self) -> str:
        userdata = os.path.join(os.path.expanduser("~"), ".anytype")
        if not os.path.exists(userdata):
            os.makedirs(userdata)

        if plataform.system() == "Windows":
            os.system(f"attrib +h {userdata}")

        return userdata

    def get_spaces(self, offset=0, limit=10) -> list[Space]:
        api_url = CONST.get("apiUrl")
        url = f"{api_url}/spaces/"
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        if response.status_code != 200:
            raise Exception("Error: ", response.json())

        results = []
        for data in response.json().get("data", []):
            new_item = Space()
            new_item._headers = self._headers
            for key, value in data.items():
                if key == "blocks":
                    new_item.__dict__[key] = value
                else:
                    new_item.__dict__[key] = value
            results.append(new_item)

        return results

    def create_space(self, name: str) -> Space:
        api_url = CONST.get("apiUrl")
        url = f"{api_url}/spaces/"
        object_data = {
            "name": name,
        }

        response = requests.post(url, headers=self._headers, json=object_data)
        response.raise_for_status()

        data = response.json()
        new_space = Space()
        for key, value in data["space"].items():
            new_space._headers = self._headers
            new_space.__dict__[key] = value

        return new_space
