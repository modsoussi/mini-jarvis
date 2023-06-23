import kernel.actions.web as web
from bs4 import BeautifulSoup
import re
import json

ACTION_TYPE_ASK_FOR_INFO = "[ask-for-info]"
ACTION_TYPE_WEB_BROWSE = "[web-browse]"
ACTION_TYPE_SEARCH = "[google-search]"
ACTION_TYPE_FINAL = "[final-answer]"

class Action:
  def __init__(self, action):
    self.raw = json.loads(action)
    self.action_type = self.raw["action_type"]
    
    if self.action_type == ACTION_TYPE_ASK_FOR_INFO:
      self.prompt = self.raw["prompt"]
    elif self.action_type == ACTION_TYPE_WEB_BROWSE:
      self.url = self.raw["url"]
      self.method = self.raw["method"]
      
      self.params = None
      if not self.raw.get("params") is None:
        self.params = self.raw["params"]
    elif self.action_type == ACTION_TYPE_FINAL:
      self.answer = self.raw["answer"]
      
  def exec(self):
    if self.action_type == ACTION_TYPE_ASK_FOR_INFO:
      return input(f"<< {self.prompt}\n>> ")
    elif self.action_type == ACTION_TYPE_WEB_BROWSE:
      if self.method == "POST":
        result =  web.post(self.url, self.params)
        if type(result) is BeautifulSoup:
          return re.sub(r"[ \r\t\n\xa0]+", " ", result.body.text)
        
      elif self.method == "GET":
        soup = web.get(self.url, self.params)
        if not soup.body is None:
          text = re.sub(r"[ \r\n\xa0\t]+", " ", soup.body.text)
          forms = [
            {
              "form_action": form.get("action"), 
              "form_method": form.get("method"),
              "form_params": [
                {
                  inp.get("name"): inp.get("value")
                } for inp in form.find_all("input") if inp["type"] != "hidden" and not inp.get("name") is None]
            } for form in soup.find_all("form")]
          links = [(re.sub(r"[ \r\n\xa0\t]+", "", a.text), a.get("href")) for a in soup.body.find_all("a") if not a.get("href") is None and a.get("href") != "javascript:void(0)"]
          return {
            "text": text,
            "forms": forms,
            # "links": links
          }
    elif self.action_type == ACTION_TYPE_FINAL:
      return self.answer
      
  def desc(self) -> str:
    if self.action_type == ACTION_TYPE_ASK_FOR_INFO:
      return self.prompt
    elif self.action_type == ACTION_TYPE_WEB_BROWSE:
      if self.method == "GET":
        return f"Clicked on {self.url}"
      elif self.method == "POST":
        return f"POST {self.url}"
      
  def __str__(self) -> str:
    return self.raw