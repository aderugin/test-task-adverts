# -*- coding: utf-8 -*-
from fabric.api import task, local


# ==============================================================================
# Docker
# ==============================================================================

@task
def build():
    local('docker-compose build')


@task
def start():
    local('docker-compose up -d')


@task
def stop():
    local('docker-compose down')


@task
def status():
    local('docker-compose ps')


@task
def migrate(app='', fake=False):
    local('docker-compose exec webapp python manage.py migrate %s %s' % (
        app, '--fake-initial' if fake else ''
    ))


@task
def makemigrations(app=''):
    local('docker-compose exec webapp python manage.py makemigrations %s' % app)


@task
def runserver():
    local('docker-compose exec webapp python manage.py runserver 0.0.0.0:8000')


@task
def shell():
    local('docker-compose exec webapp python manage.py shell')


@task
def manage(command):
    local('docker-compose exec webapp python manage.py %s' % command)


@task
def sqlshell():
    local('docker-compose exec webapp python manage.py shell_plus --print-sql')


@task
def run_tests(app=''):
    local('docker-compose exec webapp python manage.py test %s --keepdb' % app)
