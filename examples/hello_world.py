from anypy import Anytype
from anypy import Object

# Need Anytype-0.44.13-beta or higher
# Auth, on first type you need to type the 4 digit code that will popup on Anytype App
any = Anytype()
any.auth()

# Get Spaces
spaces = any.get_spaces()
my_space = spaces[0]
found_objects = (my_space.search_object("Math"))
# print(found_objects)

# Create Object
note_type = my_space.get_type("Page")
new_object = Object()
new_object.name = "Hello World!"
new_object.icon = "🐍"
new_object.description = "This is an object created from Python Api"

# Body is a markdown string
new_object.body = ''' 
# Hello
## From 
### Python 

`code string` 
**Bold Text**
_Italic Text_

'''

# Add to my_space
created_object = my_space.create_object(new_object, note_type)
created_object.delete()
