
from django.conf import settings as app_settings

default_settings = {
    'VIEWSPY_TEMPLATE': 'restgenerator/pagehtml.template',
    'URLSPY_TEMPLATE': 'restgenerator/urlspy.template',
    'PAGEHTML_TEMPLATE': 'restgenerator/pagehtml.template',
    'APPJS_TEMPLATE': 'restgenerator/appjs.template',
    'JSPACK_TEMPLATE': 'restgenerator/jspack.template',

    'APPJS_OUTPUT_DIR': app_settings.BASE_DIR,
    'JSPACK_OUTPUT_DIR': app_settings.BASE_DIR,
    'JSPACK_NAME_PATTERN': '%(app_name)s.lmd.json',
    'APPJS_NAME_PATTERN': '%(app_name)s.js',
}


class Settings(object):
    def __init__(self, default_settings):
        for k, v in default_settings.items():
            setattr(self, k, getattr(app_settings, 'RESTGENERATOR_' + k, v))

settings = Settings(default_settings)

