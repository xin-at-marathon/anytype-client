import os

from anytype import Anytype
from anytype import Object

# Need Anytype-0.44.13-beta or higher
# Auth, on first type you need to type the 4 digit code that will popup on Anytype App
any = Anytype()
any.auth()

# Get Spaces
spaces = any.get_spaces()
my_space = spaces[0]

obj = my_space.search("a")
print(obj[0].export("export"))
