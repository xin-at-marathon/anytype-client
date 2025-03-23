
from anytype import Anytype

any = Anytype()
any.auth()

# Get Spaces
spaces = any.get_spaces()
my_space = spaces[0]
obj = my_space.get_object('bafyreiaa7av3ok4bcshf6q6rsvlieo6xqjyvplwx3zwfpz2oztm7wxa65e')
print(obj.space_id)
for block in obj.blocks:
    print(block)