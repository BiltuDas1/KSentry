import os
from .environ import ENV


# If .env file exist then it's development Environment
DEBUG = False
if os.path.isfile(".env"):
  DEBUG = True

# If PRODUCTION environment is not set then it's development Environment
if ENV.get("PRODUCTION") is None:
  DEBUG = True
