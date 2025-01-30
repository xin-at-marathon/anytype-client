from anytype import Anytype

any = Anytype()
any.auth()

spaces = any.get_spaces()
my_space = spaces[0]
page_type = my_space.get_type("Note")
templates = my_space.get_templates(page_type)
