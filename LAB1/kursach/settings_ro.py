from .settings import *

INSTALLED_APPS.append('readonly')

SITE_READ_ONLY = True

MIDDLEWARE.append('readonly.middleware.DatabaseReadOnlyMiddleware')

DB_READ_ONLY_MIDDLEWARE_MESSAGE = True

TEMPLATE_CONTEXT_PROCESSORS = ('readonly.context_processors.readonly',)