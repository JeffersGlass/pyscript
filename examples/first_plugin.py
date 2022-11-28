from pyscript import Plugin


class my_first_plugin(Plugin):
    def configure(*args):
        print("Plugin being configured")


plugin = my_first_plugin("myFirstPlugin")
