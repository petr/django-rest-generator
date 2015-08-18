

import os
import shutil
import json

from django.conf import settings as app_settings
from django.core.management.base import CommandError
from django.template.loader import render_to_string

from restgenerator.management import PackageCommand


VIEWSPY_TEMPLATE = 'restgenerator/viewsetspy.template'
URLSPY_TEMPLATE = 'restgenerator/urlspy.template'

'''
TODO:
1. Make a Base command class to work with package - validation, get base data nad other
2. Unit tests ? Plz....
3. Make a frontend command to generate index.html with widgets
4. Make a command to generate javascript build with Widgets Code
5. Write a README file

REAL TODOS:
1. Create templates DIR
2. Make README
'''

class Command(PackageCommand):
    args = '<build_name>'
    help = 'Makes application for build'

    def generate_viewset(self, viewset_options, fake_data_ok):
        '''
            Generate view set.
            Returns viewset_name, viewset_file_body
        '''
        viewset_class_name = '%sViewSet' % viewset_options['name'].title().replace('_', '').replace(' ', '')
        return {
            'class_name': viewset_class_name,
            'result': json.dumps(fake_data_ok).replace('\'','\\\''),
            'source': viewset_options['source']
        }

    def work_with_package(self, zf):
        '''
            Builds directories,
            Creates views.py,
            Creates urls.py
        '''
        viewsets = self.get_viewsets_from_package(zf)
        viewspy_content = render_to_string(VIEWSPY_TEMPLATE, {'viewsets': viewsets, })

        app_name, urlspy_viewsets, routes = self.get_url_prefixes_from_package(zf)
        urlspy_content = render_to_string(URLSPY_TEMPLATE, {'routes': routes, 'app_name': app_name, 'viewsets': urlspy_viewsets, })

        self.create_dirs_and_files(zf, viewspy_content, urlspy_content)

    def create_dirs_and_files(self, zf, viewspy_content, urlspy_content):
        application_name = self.get_package_info(zf)['name']
        application_directory = os.path.join(app_settings.BASE_DIR, application_name)
        assert not os.path.exists(application_directory), 'Application \'%s\' already exists' % application_name
        os.mkdir(application_directory)

        try:
            with open(os.path.join(application_directory, '__init__.py'), 'w') as initpy:
                initpy.write('# -*- coding:utf-8 -*-\n')

            with open(os.path.join(application_directory, 'models.py'), 'w') as modelspy:
                modelspy.write('# -*- coding:utf-8 -*-\n')

            with open(os.path.join(application_directory, 'viewsets.py'), 'w') as viewspy:
                viewspy.write(viewspy_content)

            with open(os.path.join(application_directory, 'urls.py'), 'w') as urlspy:
                urlspy.write(urlspy_content)

        except Exception:
            shutil.rmtree(application_directory)
            raise

    def get_viewsets_from_package(self, zf):
        package_info = self.get_package_info(zf)
        viewsets_list = []
        for viewset_options in package_info['viewsets']:
            fake_data_ok = self.get_data(zf, viewset_options['fake_data_ok'])
            viewsets_list.append(self.generate_viewset(viewset_options, fake_data_ok))

        return viewsets_list

    def get_url_prefixes_from_package(self, zf):
        '''
            return app_name, viewsets, routes
        '''
        package_info = self.get_package_info(zf)
        routes = []
        viewsets = []
        for viewset_options in package_info['viewsets']:
            viewset_class_name = '%sViewSet' % viewset_options['name'].title().replace('_', '').replace(' ', '')
            routes.append({
                'viewset_class_name': viewset_class_name,
                'url_prefix': viewset_options['url_prefix'],
                'base_name': viewset_options['url_prefix'],
            })
            viewsets.append(viewset_class_name)

        return package_info['name'], viewsets, routes

