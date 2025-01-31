import anytype
from anytype import Anytype

any = Anytype()
any.auth()


def get_apispace() -> anytype.Space:
    spaces = any.get_spaces()
    for space in spaces:
        if space.name == "API":
            return space
    raise Exception("Space not found")


def test_create_space():
    space = any.create_space("API")
    print(space)


def test_get_spaces():
    spaces = any.get_spaces()
    assert len(spaces) > 0

    found_space = False
    for space in spaces:
        if space.name == "API":
            found_space = True
            break
    assert found_space


def test_createobj():
    space = get_apispace()
    if not space:
        raise Exception("Space not found")

    obj = anytype.Object()
    obj.name = "Hello World!"
    obj.icon = "🐍"
    obj.body = "`print('Hello World!')`"
    obj.description = "This is an object created from Python Api"
    objtype = space.get_type("Page")
    obj = space.create_object(obj, objtype)


def test_exportobj():
    space = get_apispace()
    if not space:
        raise Exception("Space not found")
    obj = space.get_objects()[0]
    obj.export("test.md", "md")
