
import json

from zipfile import ZipFile

from jsonschema import validate as jsonschema_validate

from django.core.management.base import BaseCommand

__all__ = (
    'PackageCommand',
)


BASE_PACKAGE_NAME = 'package.json'
BASE_PACKAGE_JSON_SCHEMA = 'package.schema.json'


class PackageCommand(BaseCommand):
    args = '<build_name>'

    def handle(self, *args, **options):
        filename = args[0]
        with ZipFile(filename, 'r') as zf:
            self.validate_package(zf)
            self.work_with_package(zf)

    @staticmethod
    def validate_package(zf):
        package_info = json.loads(zf.read(BASE_PACKAGE_NAME))
        package_schema = json.loads(zf.read(BASE_PACKAGE_JSON_SCHEMA))
        jsonschema_validate(package_info, package_schema)

    @staticmethod
    def get_package_info(zf):
        return json.loads(zf.read(BASE_PACKAGE_NAME))

    @staticmethod
    def get_data(zf, path):
        return json.loads(zf.read(path))

    def work_with_package(self, zf):
        raise NotImplementedError
