

import os
import shutil
import json

from django.conf import settings as app_settings
from django.core.management.base import CommandError
from django.template.loader import render_to_string

from restgenerator import settings as restgenerator_settings
from restgenerator.management import PackageCommand


'''
TODO:
1. Make a Base command class to work with package - validation, get base data nad other
2. Unit tests ? Plz....
3. Make a frontend command to generate index.html with widgets
4. Make a command to generate javascript build with Widgets Code
5. Write a README file
'''

class Command(PackageCommand):
    args = '<build_name>'
    help = 'Makes application for build'


    def work_with_package(self, zf):
        '''
            Creates index.html
        '''
        package_info = self.get_package_info(zf)
        app_name = package_info['name']
        pages = package_info['pages']
        routes = []
        widgets = []
        pages_html = []
        js_classes = []
        files = []

        try:
            for page in pages:
                print 'Processing page %s \n' % page['name']
                for widget in page['widgets']:
                    print 'Processing widget %s \n' % widget['name']
                    routes.append(self.build_route(app_name, widget))
                    widgets.append(self.build_widget(app_name, widget))
                    js_classes.append('new %s({})' % widget['js_class'])

                page_html = render_to_string(restgenerator_settings.PAGEHTML_TEMPLATE, {
                    'routes': routes,
                    'widgets': widgets,
                    'app_name': app_name,
                })
                files.append(self.create_page_html(app_name, page['name'], page_html))

            js_pack = render_to_string(restgenerator_settings.JSPACK_TEMPLATE, {'app_name': app_name, })
            files.append(self.create_js_pack(app_name, js_pack))

            app_js = render_to_string(restgenerator_settings.APPJS_TEMPLATE, {'app_name': app_name, 'js_classes': js_classes, })
            files.append(self.create_app_js(app_name, app_js))
        except Exception:
            for file_name in files:
                os.remove(file_name)

            raise


    @staticmethod
    def build_route(app_name, widget):
        '''
            Builds route for the pagehtml.template
        '''
        route = '%(name)s:api:%(viewset_url_prefix)s-list' % {
            'name': app_name,
            'viewset_url_prefix': widget['url_prefix'],
        }
        return {
            'name': 'get_%s' % widget['url_prefix'],
            'route': route,
        }

    @staticmethod
    def build_widget(app_name, widget):
        '''
            Builds widget for pagehtml.template
        '''
        return {
            'name': widget['name'],
            'options': widget['options']
        }

    @staticmethod
    def create_page_html(app_name, page_name, page_html):
        file_name = os.path.join(app_settings.BASE_DIR, app_name, 'templates', app_name, '%s.html' % page_name)
        if os.path.exists(file_name):
            raise CommandError('%s already exists' % file_name)

        with open(file_name, 'w') as page_file:
            page_file.write(page_html)

        return file_name

    @staticmethod
    def create_js_pack(app_name, js_pack):
        file_name = os.path.join(
            restgenerator_settings.JSPACK_OUTPUT_DIR,
            restgenerator_settings.JSPACK_NAME_PATTERN % {'app_name': app_name},
        )
        if os.path.exists(file_name):
            raise CommandError('%s already exists' % file_name)

        with open(file_name, 'w') as js_pack_file:
            js_pack_file.write(js_pack)

        return file_name

    @staticmethod
    def create_app_js(app_name, app_js):
        file_name = os.path.join(
            restgenerator_settings.APPJS_OUTPUT_DIR,
            restgenerator_settings.APPJS_NAME_PATTERN % {'app_name': app_name},
        )
        if os.path.exists(file_name):
            raise CommandError('%s already exists' % file_name)

        with open(file_name, 'w') as app_js_file:
            app_js_file.write(app_js)

        return file_name
