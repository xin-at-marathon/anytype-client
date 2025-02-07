class Member:
    def __init__(self):
        self._headers = {}
        self.type = ""
        self.id = ""
        self.icon = ""

    def __repr__(self):
        return f"<Member(type={self.name})>"
