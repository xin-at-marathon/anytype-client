# Anytype Python Client

An unnoficial Python Client for [Anytype](https://anytype.io/).

## Install 

``` bash
pip install git+https://github.com/charlesneimog/anytype-client
```

## Use 

``` python
from anytype import Anytype
from anytype import Object

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
new_object.add_title1("Hello From Python")

# Add to my_space
created_object = my_space.create_object(new_object, note_type)
```
