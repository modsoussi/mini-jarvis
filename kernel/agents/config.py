class Config:
  def __init__(
    self, 
    openai_key=None, 
    system_prompt=None,
    chat_model="gpt-3.5-turbo",
    completion_model="text-davinci-003",
    max_tokens=1024,
    stream_chat=False,
    ):
    if openai_key is None:
      print("missing openai_key")
    else:
      self.openai_key = openai_key
    
    if system_prompt is None:
      self.system_prompt = "You are an AI agent called MarkI."
    else:
      self.system_prompt = system_prompt
      
    self.chat_model = chat_model
    self.completion_model = completion_model
    self.max_tokens = max_tokens
    self.stream_chat = stream_chat