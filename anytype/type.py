import requests

from .config import END_POINTS
from .template import Template


class Type:
    def __init__(self):
        self.type = ""
        self._headers = {}
        self._all_templates = []
        self.space_id = ""
        self.id = ""
        self.name = ""
        self.icon = ""
        self.unique_key = ""
        self.template_id = ""

    def get_templates(self, offset: int = 0, limit: int = 100) -> None:
        url = END_POINTS["getTemplates"].format(self.space_id, self.id)
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        for data in response_data.get("data", []):
            new_template = Template()
            new_template._headers = self._headers
            for key, value in data.items():
                new_template.__dict__[key] = value
                self._all_templates.append(new_template)

    def set_template(self, template_name: str) -> None:
        if not self._all_templates:
            self.get_templates()

        found = False
        for template in self._all_templates:
            if template.name == template_name:
                found = True
                self.template_id = template.id
                return
        if not found:
            raise ValueError(
                f"Type '{self.name}' does not have a template named '{template_name}'"
            )

    def __repr__(self):
        return f"<Type(name={self.name}, icon={self.icon})>"
