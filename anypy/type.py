class Type:
    def __init__(self, type, id, unique_key, name, icon, recommended_layout):
        self.type = type
        self.id = id
        self.unique_key = unique_key
        self.name = name
        self.icon = icon
        self.recommended_layout = recommended_layout

    def __repr__(self):
        return f"<Item(name={self.name}, icon={self.icon})>"

