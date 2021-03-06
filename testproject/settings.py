# -*- coding: utf-8 -*-
import django
import os
import sys

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

PYTHON_VERSION = '%s.%s' % sys.version_info[:2]
DJANGO_VERSION = django.get_version()

JUNIT_OUTPUT_DIR = os.path.join(
    PROJECT_PATH,
    '..',
    'junit-dj%s-py%s' % (DJANGO_VERSION, PYTHON_VERSION)
)

TEST_RUNNER = 'testproject.testrunner.TestSuiteRunner'

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'nani.sqlite'

TEST_DATABASE_CHARSET = "utf8"
TEST_DATABASE_COLLATION = "utf8_general_ci"

DATABASE_SUPPORTS_TRANSACTIONS = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    
    'testproject.app',
    'nani',
)

LANGUAGE_CODE = "en"

LANGUAGES = (
    ('en', 'English'),
    ('ja', u'日本語'),
)

SOUTH_TESTS_MIGRATE = False

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

ROOT_URLCONF = 'testproject.urls'

DEBUG = True
TEMPLATE_DEBUG = True