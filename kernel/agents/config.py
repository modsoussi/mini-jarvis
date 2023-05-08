class Config:
  def __init__(
    self, 
    openai_key=None, 
    system_prompt=None,
    model=None,
    max_tokens=1024,
    stream=False,
    ):
    if openai_key is None:
      print("missing openai_key")
    else:
      self.openai_key = openai_key
    
    if system_prompt is None:
      self.system_prompt = "You are an AI agent called MarkI."
    else:
      self.system_prompt = system_prompt
      
    self.model = model
    self.max_tokens = max_tokens
    self.stream = stream