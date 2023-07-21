from .parser import Parser
from typing import Dict
import urllib
import requests
from playwright.sync_api import sync_playwright, Playwright, BrowserContext, Page

class Browser:
  def __init__(self, playwright: Playwright):
    self.parser = Parser()
    self.__browser = playwright.chromium.launch()
    self.__pages: Dict[str, Page] = {}
      
  def close(self):
    for url, page in self.__pages.items():
      page.context.close()
    
    self.__browser.close()
    
  def get(self, url: str, params: Dict = None) -> str:
    if url.startswith('/url?'):
      url = f"https://www.google.com{url}"
      
    context = self.__browser.new_context()
    page = context.new_page()
    
    self.__pages[url] = page
    
    page.goto(url)
    page.wait_for_load_state()
    response = self.parser.handle(page.content())
    return response
  
  def input(self, url: str, attrs: Dict[str, str], value: str) -> str:
    try:
      page = self.__pages[url]
      
      if "id" in attrs.keys():
        page.locator(f"input#{attrs['id']}").fill(value)
      elif "name" in attrs.keys():
        page.locator(f"input[name=\"{attrs['name']}\"]").fill(value)
        
      response = self.parser.handle(page.content())
      
      return response
    except KeyError:
      raise Exception(f"Missing key from attrs {attrs}")
    
  def click(self, url: str, selector: str) -> str:
    page = self.__pages[url]
    
    page.locator(selector=selector).click()
    
    response = self.parser.handle(page.content())
    
    return response
    
  def post(self, url: str, data: Dict = None):
    response = requests.post(url, data=data)
    
    if response.headers.get("content-type").startswith("text/html"):
      return self.parser.handle(response.text)

    return "Impossible"
  
  def google_search(self, q: str) -> str:
    return self.get(f"https://www.google.com/search?q={urllib.parse.urlencode(dict(q=q))}")
