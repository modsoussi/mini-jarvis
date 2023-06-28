from kernel.browser import Browser
import urllib
import json

ACTION_TYPE_ASK_FOR_INFO = "[ask-for-info]"
ACTION_TYPE_WEB_BROWSE = "[web-browse]"
ACTION_TYPE_SEARCH = "[google-search]"
ACTION_TYPE_FINAL = "[final-answer]"

class Action:
  def __init__(self, action):
    try:
      self.raw = json.loads(action)
      self.action_type = self.raw["action_type"]
    except json.JSONDecodeError:
      print(f"json.JSONDecodeError: {self.raw}")
    
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
    elif self.action_type == ACTION_TYPE_SEARCH:
      self.query = self.raw["query"]
      
  def exec(self):
    if self.action_type == ACTION_TYPE_ASK_FOR_INFO:
      return input(f"<< {self.prompt}\n>> ")
    elif self.action_type == ACTION_TYPE_WEB_BROWSE:
      if self.method == "POST":
        result = Browser().post(self.url, self.params)
        return result.strip("\n")
      elif self.method == "GET":
        soup = Browser().get(self.url, self.params)
        return soup.strip("\n ")
    elif self.action_type == ACTION_TYPE_SEARCH:
      return Browser().google_search(self.query)
    elif self.action_type == ACTION_TYPE_FINAL:
      return self.answer
      
  def desc(self) -> str:
    if self.action_type == ACTION_TYPE_ASK_FOR_INFO:
      return self.prompt
    elif self.action_type == ACTION_TYPE_WEB_BROWSE:
      if self.method == "GET":
        desc = f"Clicked on {self.url}"
        if self.params is not None:
          desc = desc + f"/?{urllib.parse.urlencode(self.params)}"
        return desc
      elif self.method == "POST":
        return f"Submitting form on {self.url}"
    elif self.action_type == ACTION_TYPE_SEARCH:
      return f"Google Search for \"{self.query}\""
    elif self.action_type == ACTION_TYPE_FINAL:
      return "Final Answer:"
      
  def __str__(self) -> str:
    return self.raw