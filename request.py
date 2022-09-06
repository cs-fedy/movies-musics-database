import requests
from time import sleep


def request():
  MAX_WINDOW_LENGTH = 20
  window_length: int = 0

  def get(url: str) -> str:
    nonlocal window_length
    print('requesting:', url)
    if window_length == MAX_WINDOW_LENGTH:
      print('window length exceeded waiting...', f'max length: {MAX_WINDOW_LENGTH}')
      window_length = 0
      sleep(60)

    request = requests.get(url)

    window_length += 1
    return request.content

  return get