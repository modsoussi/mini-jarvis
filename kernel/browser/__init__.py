from .parser import Parser
from typing import Dict
import requests

class Browser:
  def __init__(self):
    self.parser = Parser()
    
  def get(self, url: str, params: Dict = None) -> str:
    if url.startswith('/url?'):
      url = f"https://www.google.com{url}"
  
    response = requests.get(url, params=params)
    content_type = response.headers.get("content-type")
    if content_type.startswith("text/html"):
      return self.parser.handle(response.text)
    elif content_type.startswith("application/json"):
      return response.text