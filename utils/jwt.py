import time
import jwt
from core import settings


async def get_installation_token(installation_id: int):
  payload = {
    "iat": int(time.time()) - 60,  # Issued at (60s ago for clock drift)
    "exp": int(time.time()) + 600,  # Expires in 10 minutes
    "iss": settings.APP_ID,
  }

  encoded_jwt = jwt.encode(payload, settings.APP_PRIVATE_KEY, algorithm="RS256")

  # Exchange JWT for Installation Access Token
  url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
  headers = {
    "Authorization": f"Bearer {encoded_jwt}",
    "Accept": "application/vnd.github+json",
  }

  response = await settings.HTTPX.post(url, headers=headers)
  return response.json().get("token")
