from kernel.agents.config import Config
from colorama import Fore
from typing import Dict
import openai
import tiktoken

class Agent:
  def __init__(self, config: Config):
    self.config = config
    openai.api_key = self.config.openai_key
    
class CompletionAgent(Agent):
  def __init__(self, 
               config: Config,
               ):
    super().__init__(config)
    self.tokenizer = tiktoken.encoding_for_model(self.config.completion_model)
  
  def check_prompt_length(self, prompt):
    total_tokens = len(self.tokenizer.encode(prompt))
    if total_tokens > 4097:
      raise Exception("Too many tokens")
  
  def get_completion(self, prompt, context: Dict = None) -> str:
    _prompt = """{}

Input: 
{}
""".format(
  self.config.system_prompt, 
  prompt)

    if not context is None:
      _prompt = """{}

Context:{}      
""".format(_prompt, '\n'.join([f"{k}:{v}" for k,v in context.items()]))

    self.check_prompt_length(_prompt)
    
    response = openai.Completion.create(
      model=self.config.completion_model,
      prompt=_prompt,
      temperature=.2,
      max_tokens=self.config.max_tokens,
    )
    
    return response.choices[0].text
    
class ChatAgent(Agent):
  def __init__(self,
               config: Config,
               ):
    super().__init__(config)
    self.messages = [
      {
        "role": "system",
        "content": self.config.system_prompt,
      }
    ]
    self.tokenizer = tiktoken.encoding_for_model(self.config.chat_model)
  
  def check_messages_length(self):
    total_tokens = 0
    for message in self.messages:
      total_tokens += len(self.tokenizer.encode(message["content"]))
    
    print(total_tokens)
  
  def chat(self, user_input):
    self.messages.append({"role":"user", "content": user_input})
    self.check_messages_length()
        
    response = openai.ChatCompletion.create(
      model=self.config.chat_model,
      messages=self.messages,
      stream=self.config.stream_chat,
    )
        
    agent_response = {"role": "", "content": ""}
    for line in response:
      if "role" in line.choices[0].delta:
        agent_response["role"] = line.choices[0].delta.role
      if "content" in line.choices[0].delta.keys():
        agent_response["content"] = agent_response["content"] + line.choices[0].delta.content
          
      yield line.choices[0].delta
        
    self.messages.append(agent_response)