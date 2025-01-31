import requests
from pathlib import Path
import platform

from .const import CONST


class Object:
    def __init__(self):
        self._headers = {}
        self.space_id = ""
        self.id = id
        self.source = ""
        self.type = "Page"
        self.name = ""
        self.icon = ""
        self.body = ""
        self.description = ""
        self.blocks = []
        self.details = []
        self.layout = "basic"
        self.root_id = ""
        self.snippet = ""
        self.space_id = ""

    def __repr__(self):
        return f"<Object(name={self.name},type_id={self.type})>"

    def delete(self) -> None:
        url = f"{CONST["apiUrl"]}/spaces/{self.space_id}/objects/{self.id}"
        response = requests.delete(url, headers=self._headers)
        response.raise_for_status()

    def export(self, folder: str, format: str = "markdown") -> None:
        path = Path(folder)
        if not path.is_absolute():
            path = Path.cwd() / path

        assert format in ["markdown", "protobuf"]
        url = f"{CONST["apiUrl"]}/spaces/{self.space_id}/objects/{self.id}/export/{format}"
        payload = {"path": str(path)}
        response = requests.post(url, headers=self._headers, json=payload)
        response.raise_for_status()
        if platform.system() == "Linux":
            print("Note that this will not work on Anytype for flatpak")

    def add_title1(self, text) -> None:
        self.body += f"# {text}\n"

    def add_title2(self, text) -> None:
        self.body += f"## {text}\n"

    def add_title3(self, text) -> None:
        self.body += f"### {text}\n"

    def add_text(self, text) -> None:
        self.body += f"{text}\n"

    def add_codeblock(self, code, language=""):
        self.body += f"``` {language}\n{code}\n```\n"

    def add_bullet(self, text) -> None:
        self.body += f"- {text}\n"

    def add_checkbox(self, text, checked=False) -> None:
        self.body += f"- [x] {text}\n" if checked else f"- [ ] {text}\n"
