from anypy import Anytype
from anypy import Object

# Need Anytype-0.44.13-beta or higher
# Auth, on first type you need to type the 4 digit code that will popup on Anytype App
any = Anytype()
any.auth()

# Get Spaces
spaces = any.get_spaces()
my_space = spaces[0]

# Create Object on the first space
note_type = my_space.get_type("Page")
new_object = Object()
new_object.name = "Hello World!"
new_object.icon = "🐍"
new_object.description = "This is an object created from Python Api"
new_object.add_title1("Hello")
new_object.add_title2("From")
new_object.add_title3("Python")
new_object.add_codeblock("print('Hello World!')", language="python")
new_object.add_bullet("1")
new_object.add_bullet("2")
new_object.add_bullet("3")


# Add to my_space
created_object = my_space.create_object(new_object, note_type)
# created_object.delete()





