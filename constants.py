class Texts:
    IS_NOT_PRIVATE_MESSAGE = """<b>This command is not allowed to be used outside of dms.
Please send this command in my DMs!</b>"""

    IS_NOT_ADMIN = """<b>You are not admin!</b>"""

    HELP_MESSAGE = """<b>Available commands:</b>
/start - start bot
"""

    HAVE_CLONE_LIST = """<b>Clone list:</b>
{}"""

    HAVE_NO_CLONE_LIST = """<b>Clone list is empty!</b>"""

    CREATE_CLONE = """<b>Creating clone...</b>"""

    CREATE_CLONE_SUCCESS = """<b>Clone created!</b>
<b>Email:</b> {}
<b>Password:</b> {}"""

    CREATE_CLONE_FAILED = """<b>Clone creation failed!</b>"""



class Constants:
    pass


constants = Constants()
texts = Texts()