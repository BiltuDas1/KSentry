import hmac
import hashlib


def verify_signature(payload_body, signature_header, secret):
  sha_name, signature = signature_header.split("=")
  if sha_name != "sha256":
    return False

  # Compute the HMAC
  hash_object = hmac.new(secret.encode(), msg=payload_body, digestmod=hashlib.sha256)
  expected_signature = hash_object.hexdigest()

  # Use secure comparison to prevent timing attacks
  return hmac.compare_digest(expected_signature, signature)
