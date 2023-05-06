from typing import List, Any
import requests
import urllib
import bs4

def bs(html: str) -> bs4.BeautifulSoup:
  return bs4.BeautifulSoup(html, "html.parser")

def search(query: str) -> List[Any]:
  soup = get(f"https://www.google.com/search?q={urllib.parse.urlencode(dict(q=query))}")
  return [link for link in soup.body.find_all("a") if link["href"].startswith("/url?")]

def get(url: str) -> bs4.BeautifulSoup:
  if url.startswith('/url?'):
    url = f"https://www.google.com{url}"
  
  response = requests.get(url)
  return bs(response.text)