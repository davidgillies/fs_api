"""
Plugins
"""
import fs_apps
from questionnaire.models import *

class ChildList():
    def __init__(self, data, caller):
        self.data = data
        self.caller = caller
        self.rows = self.get_rows()
        self.template = 'fs_renderer/childlist.html'

    def get_rows(self):
        no_rows = int(self.data['FH02_SisterTotal']) + int(self.data['FH03_BrotherTotal'])
        rows = []

        for number in range(1, no_rows+1):
            child_name = 'child_name' + '__' + str(number)
            child_age = 'child_age' + '__' + str(number)
            if child_name in self.data.keys():
                child_name_value = self.data[child_name]
            else:
                child_name_value = ''
            if child_age in self.data.keys():
                child_age_value = self.data[child_age]
            else:
                child_age_value = ''
            child_data = {'child_name': child_name_value, 'child_age': child_age_value}
            rows.append(child_data)
        return rows


class TestPlugin():
    def __init__(self, data, caller):
        self.data = data
        self.caller = caller
        if isinstance(caller,fs_apps.Question):
            self.template = 'fs_renderer/testplugin_q.html'
        else:
            self.template = 'fs_renderer/testplugin.html'

    def do_it(self):

        if isinstance(self.caller,fs_apps.Question):
            results = Results.objects.filter(var_name__startswith='child_age')
            tally = 0
            number = 0
            for result in results:
                if result.var_value != '':
                    tally = tally + int(result.var_value)
                    number = number + 1
            average = tally/number        
            return average
        if isinstance(self.caller,fs_apps.QuestionGroup):
            profile = {}
            profile['name'] = self.caller.title
            profile['type'] = 'QuestionGroup'
            profile['position'] = self.caller.position
            profile['section'] = self.caller.section.title
            return profile
