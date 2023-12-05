from kernel.browser import Browser
import urllib
import json

ACTION_TYPE_ASK_FOR_INFO = "[ask-for-info]"
ACTION_TYPE_WEB_BROWSE = "[browse]"
ACTION_TYPE_SEARCH = "[google-search]"
ACTION_TYPE_FINAL = "[final-answer]"
ACTION_TYPE_INPUT = "[input]"
ACTION_TYPE_CLICK = "[click]"

class Action:
  def __init__(self, action: str, browser: Browser = None ):
    try:
      if (action.startswith('```json')):
        action = action[7:len(action)-3]
      
      print(action)
      print('*** ----------------------- ***')
      self.raw = json.loads(action)
      self.action_type = self.raw["action_type"]
      
      self.browser = browser
      if self.browser is None:
        self.browser = Browser()
    except json.JSONDecodeError:
      print(f"json.JSONDecodeError: {action}")
    
    self.past_result = None
    if "past_result" in self.raw:
      self.past_result = self.raw["past_result"]
    
    if self.action_type == ACTION_TYPE_ASK_FOR_INFO:
      self.prompt = self.raw["prompt"]
    elif self.action_type == ACTION_TYPE_WEB_BROWSE:
      self.url = self.raw["url"]
      self.method = "GET"
      
      self.params = None
      if not self.raw.get("params") is None:
        self.params = self.raw["params"]
    elif self.action_type == ACTION_TYPE_SEARCH:
      self.query = self.raw["query"]
    elif self.action_type == ACTION_TYPE_INPUT:
      attrs = {}
      if "name" in self.raw:
        attrs["name"] = self.raw["name"]
      if "id" in self.raw:
        attrs["id"] = self.raw["id"]
        
      if "value" in self.raw:
        self.value = self.raw["value"]
      self.attrs = attrs
      if "url" in self.raw:
        self.url = self.raw["url"]
    elif self.action_type == ACTION_TYPE_CLICK:
      if "url" in self.raw:
        self.url = self.raw["url"]
      
      self.selector = self.raw["selector"]
    elif self.action_type == ACTION_TYPE_FINAL:
      self.answer = self.raw["answer"]
      
  def exec(self):
    if self.action_type == ACTION_TYPE_ASK_FOR_INFO:
      return input(f"<< {self.prompt}\n>> ")
    elif self.action_type == ACTION_TYPE_WEB_BROWSE:
      if self.method == "POST":
        result = self.browser.post(self.url, self.params)
        return result.strip("\n")
      elif self.method == "GET":
        result = self.browser.get(self.url, self.params)
        return result.strip("\n ")
    elif self.action_type == ACTION_TYPE_SEARCH:
      return self.browser.google_search(self.query)
    elif self.action_type == ACTION_TYPE_INPUT:
      return self.browser.input(self.url, attrs=self.attrs, value=self.value)
    elif self.action_type == ACTION_TYPE_CLICK:
      return self.browser.click(self.url, self.selector)
    elif self.action_type == ACTION_TYPE_FINAL:
      return self.answer
    else:
      raise Exception(f"Action type {self.action_type} not implemented:\n{self.raw}")
      
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
    elif self.action_type == ACTION_TYPE_INPUT:
      return f"Filling out form on {self.url}"
    elif self.action_type == ACTION_TYPE_CLICK:
      return f"Clicked {self.selector}"
    elif self.action_type == ACTION_TYPE_FINAL:
      return "Final Answer:"
      
  def __str__(self) -> str:
    return self.raw