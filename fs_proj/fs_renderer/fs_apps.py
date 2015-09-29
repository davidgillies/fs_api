from copy import deepcopy
from itertools import chain
from xml_objectifier import objectifier
import datetime
import simplejson
import local_settings
from django.forms.models import model_to_dict
from .fs_validator import Validator
from .fs_querysets import QuerySet

class Question(objectifier.Question):
    def __init__(self, question_object, app_object, section_object):
        self.plugin = ''
        super(Question, self).__init__(question_object, app_object, section_object)
        self.model = self.set_model()

    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
            if key == '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}plugin':
                self.section.plugins.append(self)
                self.plugin = self.rendering_hints[key].strip()
                # self.app_object.plugins['questioon_plugins'].append(self.rendering_hints[key].strip())
                # self.section.plugins.append(self.rendering_hints[key].strip())
        self.rendering_hints[key] = self.rendering_hints[key].strip()

    def set_model(self):
        if self.variable in self.app_object.db_mapping.keys():
            variable = self.app_object.db_mapping[self.variable]
        else:
            variable = self.variable
        if self.app_object.models:
            section_model = self.app_object.model_mapping[int(self.section.position)]
            if variable in section_model._meta.get_all_field_names():
                self.model = section_model
            elif 'multi' in self.rendering_hints.keys():
                if variable in self.app_object.table_model_mapping[self.rendering_hints['multi']]._meta.get_all_field_names():
                    self.model = self.app_object.table_model_mapping[self.rendering_hints['multi']]
            else:
                self.model = None

    def get_template(self, selection):
        return {'radio': 'fs_renderer/radio.html',
                'dropdown': 'fs_renderer/select.html',
                'text': 'fs_renderer/text.html',
                'multiline': 'fs_renderer/textarea.html',
                'range': 'fs_renderer/range.html',
                'datalist': 'fs_renderer/datalist.html',
                'search': 'fs_renderer/search.html',
                'altradio': 'fs_renderer/alt_radio.html',
                'altdropdown': 'fs_renderer/alt_select.html',
                'alttext': 'fs_renderer/alt_text.html',
                'altmultiline': 'fs_renderer/alt_textarea.html',
                'altrange': 'fs_renderer/alt_range.html',
                'altdatalist': 'fs_renderer/alt_datalist.html',
                'altsearch': 'fs_renderer/alt_search.html'}[selection]

    def set_template(self):
        if local_settings.QUESTIONNAIRE:
            qtype = 'alt' + self.rendering_hints['qtype']
            self.template = self.get_template(qtype)
        else:
            self.template = self.get_template(self.rendering_hints['qtype'])


class QuestionGroup(objectifier.QuestionGroup):
    def __init__(self, question_group_object, app_object, section_object):
        self.testing = local_settings.TESTING
        self.plugin = ''
        self.question_group_level_plugin = False
        super(QuestionGroup, self).__init__(question_group_object, app_object, section_object)

    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
            if key == 'plugin':
                # self.plugins.append(self.rendering_hints[key].strip())
                self.question_group_level_plugin = True
                self.section.plugins.append(self)
                self.plugin = self.rendering_hints[key].strip()
        self.rendering_hints[key] = self.rendering_hints[key].strip()


class Section(objectifier.Section):
    def __init__(self, section_xml_object, app_object):
        self.testing = local_settings.TESTING
        self.plugins = []
        self.plugin = ''
        self.section_level_plugin = False
        super(Section, self).__init__(section_xml_object, app_object)

    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
            if key == 'plugin':
                self.plugins.append(self)
                self.plugin = self.rendering_hints[key].strip()
                self.section_level_plugin = True
                # self.app_object.plugins['section_plugins'].append(self.rendering_hints[key].strip())
        self.rendering_hints[key] = self.rendering_hints[key].strip()

    def section_to_dict(self):
        data = {}
        multi = False
        for qg in self.section_objects:
            data_dict = {}
            for q in qg.question_group_objects:
                if isinstance(q, Question):
                    if 'multi' in q.rendering_hints.keys() or multi is True:
                        if multi is False:
                            multi = True
                            multi_name = q.rendering_hints['multi']
                            if multi_name not in data.keys():
                                data[multi_name] = []
                        data_dict['id'] = q.var_id
                        if isinstance(q.var_value, datetime.timedelta):
                            data_dict[q.variable[:-2]] = str(q.var_value)
                        else:
                            data_dict[q.variable[:-2]] = q.var_value
                        if 'endoftr' in q.rendering_hints.keys():
                            multi = False
                            data[multi_name].append(data_dict)
                            data_dict = {}
                    else:
                        if isinstance(q.var_value, datetime.timedelta):
                            data[q.variable] = str(q.var_value)
                        else:
                            data[q.variable] = q.var_value
        return data


class Application(objectifier.Application):
    def __init__(self, name, xml_path):
        self.models = local_settings.MODELS
        self.custom = local_settings.CUSTOM
        self.mapping = local_settings.SECTION_MAPPING
        self.db_mapping = local_settings.DB_MAPPING
        self.model_mapping = local_settings.MODEL_MAPPING
        self.model_form_mapping = local_settings.MODEL_FORM_MAPPING
        self.table_model_mapping = local_settings.TABLE_MODEL_MAPPING
        self.testing = local_settings.TESTING
        # self.plugins = {'section_plugins': [], 'question_group_plugins': [], 'question_plugins': []}
        super(Application, self).__init__(name, xml_path)

    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
            if key == '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}plugin':
                self.plugins.append(self.rendering_hints[key].strip())
        self.rendering_hints[key] = self.rendering_hints[key].strip()

    def get_data(self, section_number, id_variable, id_variable_value):
        if self.models:
            data = model_to_dict(self.model_mapping[int(section_number)].objects.get(id=id_variable_value))
        else:
            queryset = QuerySet(table_name=self.get_table_name(section_number),
                                id_variable_value=id_variable_value)
            data = queryset.get()
        return data

    def insert_data(self, section_number, id_variable, body):
        json_dict = simplejson.JSONDecoder().decode(body)
        if self.models:
            json_dict = self.pre_process_keys(json_dict)
            validator = self.model_form_mapping[int(section_number)](json_dict)
            if validator.is_valid():
                json_dict = self.post_process_keys(json_dict)
                model = self.model_mapping[int(section_number)].objects.create(**json_dict)
                data = model_to_dict(model)
            else:
                errors = {}
                for field in validator:
                    errors[field.label] = field.errors
                data = json_dict
                data['errors'] = 'errors'
        else:
            if 'search' in json_dict.keys():
                data = self.search(json_dict['search'], section_number)
            else:
                validator = Validator(self.validator, json_dict)
                print json_dict, self.validator
                if validator.is_valid():
                    for k in json_dict.keys():
                        if k in self.db_mapping.keys():
                            json_dict[self.db_mapping[k]] = json_dict[k]
                            json_dict.pop(k)
                    queryset = QuerySet(table_name=self.get_table_name(section_number))
                    data = queryset.create(json_dict)
                else:
                    for k in json_dict.keys():
                        if k in self.db_mapping.keys():
                            json_dict[self.db_mapping[k]] = json_dict[k]
                            json_dict.pop(k)
                    data = json_dict
                    data['errors'] = validator.errors
        return data

    def pre_process_keys(self, json_dict):
        pass

    def post_process_keys(self, json_dict):
        pass

    def update_data(self, section_number, id_variable, id_variable_value,
                    body):
        if self.models:
            json_dict = simplejson.JSONDecoder().decode(body)
            orig_json_dict = json_dict
            json_dict = self.pre_process_keys(json_dict)
            for k in json_dict.keys():
                if k in self.db_mapping.keys():
                    json_dict[self.db_mapping[k]] = json_dict[k]
                    json_dict.pop(k)
            validator_form = self.model_form_mapping[int(section_number)](json_dict)
            if validator_form.is_valid():
                self.model_mapping[int(section_number)].objects.filter(pk=id_variable_value).update(**json_dict)
                data = model_to_dict(self.model_mapping[int(section_number)].objects.get(id=id_variable_value))
            else:
                errors = {}
                for field in validator_form:
                    errors[field.label] = field.errors.as_text()
                data = orig_json_dict
                data['errors'] = errors
        else:
            json_dict = simplejson.JSONDecoder().decode(body)
            validator = Validator(self.validator, json_dict)
            if validator.is_valid():
                for k in json_dict.keys():
                    if k in self.db_mapping.keys():
                        json_dict[self.db_mapping[k]] = json_dict[k]
                        json_dict.pop(k)
                queryset = QuerySet(table_name=self.get_table_name(section_number))
                queryset.update(json_dict, id_variable_value)
                data = queryset.data
            else:
                for k in json_dict.keys():
                    if k in self.db_mapping.keys():
                        json_dict[self.db_mapping[k]] = json_dict[k]
                        json_dict.pop(k)
                data = json_dict
                data['errors'] = validator.errors
        return data

    def delete_data(self, section_number, id_variable, id_variable_value):
        if self.models:
            self.model_mapping[int(section)].objects.get(id=id_variable_value).delete()
        else:
            queryset = QuerySet(table_name=self.get_table_name(section_number),
                                id_variable_value=id_variable_value)
            queryset.delete()
        return

    def get_table_name(self, section_number):
        return self.mapping[int(section_number)]

    def search(self, search_term, section_number):
        pass

    def get_section(self, section_number):
        return deepcopy(self.sections[str(section_number)])


class DataPrep(object):
    def __init__(self, section, data):
        self.data = data
        self.section = section
        self.Question = Question

    def data_prep(self):
        if 'errors' in self.data.keys():
            self.section.errors = self.data['errors']

        try:
            for qg in self.section.section_objects:
                multi_lines = []
                multi = False
                multi_line = []
                for q in qg.question_group_objects:
                    if 'multi' in q.rendering_hints.keys() or multi:
                        if multi is False:
                            multi_index = qg.question_group_objects.index(q)
                        multi_line.append(q)
                        multi = True
                        if 'endoftr' in q.rendering_hints.keys():
                            multi = False
                            multi_data = self.get_multi_data(multi_line[0].rendering_hints['multi'], self.data['id'])
                            multi_line_adder = []
                            for i in range(len(multi_data)):
                                multi_line_adder.append(deepcopy(multi_line))
                            multi_line = multi_line_adder
                            for index in range(len(multi_line)):
                                for i in range(len(multi_line[index])):
                                    if isinstance(multi_line[index][i], self.Question):
                                        try:
                                            multi_line[index][i].var_value = multi_data[index][multi_line[index][i].variable]
                                            multi_line[index][i].multi = True
                                        except:
                                            multi_line[index][i].required = False
                                        try:
                                            multi_line[index][i].var_id = multi_data[index]['id']
                                        except:
                                            pass
                                        multi_line[index][i].variable = 'multi_' + multi_line[index][i].variable + '_' + str(index)
                            multi_line = list(chain.from_iterable(multi_line))
                            multi_lines.append([multi_line, multi_index])
                    elif isinstance(q, self.Question):
                        self.add_question_value(q)
                for ml in multi_lines:
                    qg.question_group_objects[ml[1]:ml[1]+(len(ml[0])/len(multi_data))] = ml[0]
            return self.section
        except:
            return self.section

    def get_multi_data(self, table, id):
        pass

    def add_question_value(self, q):
        q.var_value = self.data[q.variable]
        # self.section.api[q.variable] = q.var_value
        # not using thw api variable at present
