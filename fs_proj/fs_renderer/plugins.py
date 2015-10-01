
class TestPlugin():
    def __init__(self, caller):
        self.template = 'fs_renderer/testplugin.html'

    def hey(self):
        return 'Hey!'