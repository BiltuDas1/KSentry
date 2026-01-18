import os
from .environ import ENV


# If .env file exist then it's development Environment
DEBUG = False
if os.path.isfile(".env"):
  DEBUG = True

# If PRODUCTION environment is not set then it's development Environment
if ENV.get("PRODUCTION") is None:
  DEBUG = True

# Check if SERVERLESS
if not ENV.exist("SERVERLESS"):
  if ENV.exist("VERCEL"):
    print("Auto-Detect: Running on Vercel. Setting SERVERLESS = True")
    SERVERLESS = True
  elif ENV.exist("RENDER"):
    print("Auto-Detect: Running on Render. Setting SERVERLESS = False")
    SERVERLESS = False
  else:
    raise EnvironmentError("SERVERLESS Environment can't be empty")
else:
  match str(ENV.get("SERVERLESS")).lower():
    case "true":
      SERVERLESS = True
    case "1":
      SERVERLESS = True
    case "false":
      SERVERLESS = False
    case "0":
      SERVERLESS = False
    case _:
      raise EnvironmentError(
        "SERVERLESS Environment can only between true, false, 1 or 0"
      )
