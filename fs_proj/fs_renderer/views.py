from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_logic import CustomApplication
from django.views import generic
from .models import *
import local_settings
if local_settings.CUSTOM is True:
    from api_renderer.custom_logic import CustomDataPrep as DataPrep
else:
    from api_renderer.fs_apps import DataPrep

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


class StandardView(generic.ListView): 
    model = Volunteer
