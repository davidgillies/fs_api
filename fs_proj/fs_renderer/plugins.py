import fs_querysets



class TestPlugin():
    def __init__(self, caller, data):
        self.template = 'fs_renderer/testplugin.html'

    def hey(self):
        return 'Hey!'

class SurgeryList():
    def __init__(self, caller, data):
        self.template = 'fs_renderer/surgery_list.html'

    def surgery_list(self):
       surgeries = fs_querysets.QuerySet(table_name='surgeries').all()
       result = []
       for surgery in surgeries:
           result.append({'text': surgery['full_name'], 'value': surgery['id']})
       return result


PLUGINS = {'testplugin': TestPlugin, 'surgery_list': SurgeryList}
