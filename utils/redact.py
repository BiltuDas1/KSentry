def redact_text(secret: str):
  """
  Returns redact text from the range of 0 and 14

  :param secret: The text which will be redact
  :type secret: str
  """
  if len(secret) <= 8:
    return "*" * len(secret)
  elif len(secret) > 8 and len(secret) <= 14:
    if len(secret) <= 11:
      return secret[: len(secret) - 8] + "********"
    else:
      return secret[:3] + "********" + secret[(11 - len(secret)) :]
  else:
    return secret[:3] + "********" + secret[-3:]


def replace_redact(redact_text: str, secret: str, message: str):
  """
  Replace the redact text in the position of the secret
  """
  return message.replace(secret, redact_text)
