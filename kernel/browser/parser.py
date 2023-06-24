import html
import re

class Parser(html.parser.HTMLParser):
  def __init__(self):
    super().__init__()
    
    self.output = ""
    self.tags = []
  
  def handle_starttag(self, tag, attrs):
    self.tags.append(tag)
    
  def handle_endtag(self, tag):
    self.tags.pop()
    
  def handle_startendtag(self, tag, attrs):
    print(f"encountered self enclosed tag: {tag}")
    
  def handle_data(self, data):
    if len(self.tags) == 0:
      return
    
    data = re.sub(r"[ \r\n\xa0\t]+", "", data)
    current_tag = self.tags[-1]
    
    if current_tag in ["p", "div"]:
      self.output = self.output + "\n" + data
    elif current_tag in ["a"]:
      self.output = self.output + f"[{data}] (potential link)"
    elif current_tag not in ["script", "style"]:
      self.output = self.output + " -- " + data
    
  def feed(self, data: str):
    super().feed(data)
  
  def handle(self, data: str) -> str:
    self.feed(data)
    
    return self.output