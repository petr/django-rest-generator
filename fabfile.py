from fabric.api import local


def build_package():
    local('python setup.py sdist')

