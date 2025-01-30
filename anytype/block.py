class Block:
    def __init__(self, **kwargs):
        self.id = id

    def __repr__(self):
        return f"<Block(name={self.name},type_id={self.type})>"
