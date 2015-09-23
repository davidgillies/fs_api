import json
from django.http import HttpResponseNotFound
from django.views.generic import View
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_logic import CustomApplication
from django.views import generic
from .models import *
import local_settings
if local_settings.CUSTOM is True:
    from fs_renderer.custom_logic import CustomDataPrep as DataPrep
else:
    from fs_renderer.fs_apps import DataPrep

# xml_string = open(local_settings.XML_FILE, 'r').read()
if local_settings.CUSTOM:
    fenland_app = CustomApplication('fenland', local_settings.XML_FILE)
else:
    from fs_apps import Application
    fenland_app = Application('fenland', local_settings.XML_FILE)


class APIView(APIView):
    def get(self, request, section=None, id_variable=None,
            id_variable_value=None):
        if id_variable is None or id_variable_value is None:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            data = fenland_app.get_data(section, id_variable, id_variable_value)
            section_obj = fenland_app.get_section(section)
            section_obj = DataPrep(section_obj, data)
            section_obj = section_obj.data_prep()
            data = section_obj.section_to_dict()
            response = Response(data, status=status.HTTP_200_OK)
            return response

    def post(self, request, section=None, id_variable=None,
             id_variable_value=None):
        data = fenland_app.insert_data(section, id_variable, request.body)
        response = Response(data, status=status.HTTP_201_CREATED)
        return response

    def put(self, request, section=None, id_variable=None,
            id_variable_value=None):
        data = fenland_app.update_data(section, id_variable, id_variable_value, request.body)
        response = Response(data, status=status.HTTP_200_OK)
        return response

    def delete(self, request, section=None, id_variable=None,
               id_variable_value=None):
        fenland_app.delete_data(section, id_variable, id_variable_value)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Index(View):
    def get(self, request):
        return render(request, 'fs_renderer/index.html', {'settings': local_settings})
        
# class StandardView(generic.ListView): 
#     model = Volunteer


class HTMLView(View):
    def get(self, request, section=None, question_group=None, question=None):
        result = {}
        if section is None:
            return HttpResponseNotFound('Page Not Found')
        section_obj = fenland_app.get_section(section)
        if request.GET:
            id_variable_value = request.GET['id']
            result['id_variable_value'] = id_variable_value
            data = fenland_app.get_data(section, 'id', id_variable_value)
            section_obj = DataPrep(section_obj, data)
            section_obj = section_obj.data_prep()
        else:
            data = {}
            data['id'] = None
        if question_group is None:
            result['section'] = section_obj
            result['data_id'] = data['id']
            return render(request, 'fs_renderer/base.html', result)
        question_group = section_obj.get_question_group(question_group)
        if question is None:
            result['question_group'] = question_group
            return render(request, 'fs_renderer/question_group.html', result)
        question = question_group.get_question(question)
        result['question'] = question
        return render(request, 'fs_renderer/question.html', result)

    def post(self, request, section=None, question_group=None, question=None):
        result = {}
        if section is None:
            return HttpResponseNotFound('Page Not Found')
        section_obj = fenland_app.get_section(section)
        myDict = dict(request.POST.iterlists())
        for k in myDict.keys():
            myDict[k] = myDict[k][0]
        if 'id' not in myDict.keys():
            myDict[u'id'] = request.GET['id']
        if 'search' in myDict.keys():
            result['search_results'] = fenland_app.search(myDict['search'], section)
            data = {}
        else:
            myDict_json = json.dumps(myDict)
            data = fenland_app.update_data(section, 'id_variable',
                                           myDict['id'], myDict_json)
            result['data_id'] = data['id']
        section_obj = DataPrep(section_obj, data)
        section_obj = section_obj.data_prep()
        result['section'] = section_obj
        return render(request, 'fs_renderer/base.html', result)