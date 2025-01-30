class Type:
    def __init__(self):
        self.type = ''
        self.id = ''
        self.name = ''
        self.icon = ''
        self.unique_key = ''

    def __repr__(self):
        return f"<Type(name={self.name}, icon={self.icon})>"
