from .parser import Parser
from typing import Dict
import urllib
import requests
from playwright.sync_api import sync_playwright

class Browser:
  def __init__(self):
    self.parser = Parser()
    self.browser_context = None
    
  def get(self, url: str, params: Dict = None) -> str:
    if url.startswith('/url?'):
      url = f"https://www.google.com{url}"
      
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.goto(url)
        
        response = self.parser.handle(page.content())
        b.close()
        return response
    
  def post(self, url: str, data: Dict = None):
    response = requests.post(url, data=data)
    
    if response.headers.get("content-type").startswith("text/html"):
      return self.parser.handle(response.text)

    return response
  
  def google_search(self, q: str) -> str:
    return self.get(f"https://www.google.com/search?q={urllib.parse.urlencode(dict(q=q))}")