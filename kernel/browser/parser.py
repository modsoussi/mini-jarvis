import html.parser
import re
from typing import Dict

class Parser(html.parser.HTMLParser):
  def __init__(self):
    super().__init__()
    
    self.output = ""
    self.tags = []
    self.cur_attrs = {}
    self.pre_tabs = 0
    self.current_href = None
    
  def handle_tag(self, tag: str, attrs: Dict[str, str], start: bool):
    if start:
      self.tags.append(tag)
      self.cur_attrs = attrs
      
      if tag == "form":
        self.output = self.output + "\n" + f"[form"
        
        if "method" in self.cur_attrs.keys():
          self.output = self.output + f" method={self.cur_attrs['method']}"
        
        if "action" in self.cur_attrs.keys():
          self.output = self.output + f" action={self.cur_attrs['action']}"
          
        self.output = self.output + "]"
        self.pre_tabs += 2
      elif tag == "input":
        self.output = self.output + "\n" + "\t"*self.pre_tabs + f"[input"
        
        if "name" in self.cur_attrs.keys():
          self.output = self.output + f" name={self.cur_attrs['name']}"
        
        if "value" in self.cur_attrs.keys():
          self.output = self.output + f" value={self.cur_attrs['value']}"
        
        if "type" in self.cur_attrs.keys():
          self.output = self.output + f" type={self.cur_attrs['type']}"
          
        self.output = self.output + "]"
      elif tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        self.output = self.output + "\n"
      elif tag == "a":
        if "href" in attrs.keys():
          self.current_href = attrs["href"]
    else:
      self.tags.pop()
    
      if tag == "form":
        self.output = self.output + "\n" + "[endform]" + "\n"
        self.pre_tabs -= 2
      elif tag in ["tr", "p"]:
        self.output = self.output + "\n"
      elif tag == "span":
        self.output = self.output + " "
      elif tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        self.output = self.output + "\n"
      elif tag == "a":
        self.current_href = None
  
  def handle_starttag(self, tag, attrs):
    self.handle_tag(tag, attrs=dict(attrs), start=True)
    
  def handle_endtag(self, tag):
    self.handle_tag(tag, attrs=None, start=False)
    
  def handle_startendtag(self, tag, attrs):
    self.cur_attrs = dict(attrs)
    
    if tag == "input":
      self.output = self.output + "\n" + "\t"*self.pre_tabs + f"[input"
      
      if "name" in self.cur_attrs.keys():
        self.output = self.output + f" name={self.cur_attrs['name']}"
      
      if "value" in self.cur_attrs.keys():
        self.output = self.output + f" value={self.cur_attrs['value']}"
      
      if "type" in self.cur_attrs.keys():
        self.output = self.output + f" type={self.cur_attrs['type']}"
        
      self.output = self.output + "]"
    
  def handle_data(self, data):
    if len(self.tags) == 0:
      return
    
    data = re.sub(r"[\r\n\xa0\t]+", "", data).strip(" ")
    if data == "":
      return
    
    current_tag = self.tags[-1]
    # print(current_tag, data, self.tags)
    
    if current_tag in ["h1", "h2", "h3", "h4", "h5", "h6", "span", "div", "p", "a"]:
      if "a" in self.tags:
        self.output = self.output + "\t"*self.pre_tabs + f" [{data}] ({self.current_href})"
        # if "href" in self.cur_attrs.keys():
        #   self.output = self.output + f"({self.cur_attrs['href']})"
      else:
        self.output = self.output + "\t"*self.pre_tabs + data
    elif current_tag not in ["script", "style"]:
      self.output = self.output + "\n" + "\t"*self.pre_tabs + data
    
  def feed(self, data: str):
    super().feed(data)
  
  def handle(self, data: str) -> str:
    self.feed(data)
    
    return self.output