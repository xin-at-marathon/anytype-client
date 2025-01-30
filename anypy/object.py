class Object:
    def __init__(self):
        self.id = id
        self.type = 'Page'
        self.name = ''
        self.icon = ''
        self.body= ''
        self.description = ''
        self.blocks=[]
        self.details = []
        self.layout='basic'
        self.root_id=''
        self.snippet=''
        self.space_id=''

    def __repr__(self):
        return f"<Object(name={self.name},type_id={self.type})>"


