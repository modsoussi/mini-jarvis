class Config:
  def __init__(
    self, 
    system_prompt=None,
    model=None,
    max_tokens=1024,
    stream=False,
    ):
    
    if system_prompt is None:
      self.system_prompt = "You are an AI agent called MarkI."
    else:
      self.system_prompt = system_prompt
      
    self.model = model
    self.max_tokens = max_tokens
    self.stream = stream
    
    self.max_len_context = 8092
    if self.model == 'gpt-2.3-turbo-16k':
      self.max_len_context = 16384