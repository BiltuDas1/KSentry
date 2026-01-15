from . import debug

PRODUCTION = not debug.DEBUG
DOCS_URL = "/docs" if not PRODUCTION else None
REDOC_URL = "/redoc" if not PRODUCTION else None
OPENAPI_URL = "/openapi.json" if not PRODUCTION else None
