import anytype
from anytype import Anytype
from pathlib import Path

any = Anytype()
any.auth()


def get_apispace() -> anytype.Space | None:
    spaces = any.get_spaces()
    for space in spaces:
        if space.name == "API":
            return space
    return None


def test_create_space():
    if get_apispace():
        return
    any.create_space("API")
    assert get_apispace()


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
    objs = space.get_objects()
    obj = objs[0]
    assert len(objs) > 0
    obj.export("export")
    assert Path("export").exists()
