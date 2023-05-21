from kernel.agents.config import Config
from typing import Dict
import openai
import tiktoken

class Agent:
  def __init__(self, config: Config):
    self.config = config
    openai.api_key = self.config.openai_key
    
    if self.config.model is None:
      raise Exception("Agent configuration model cannot be None")
      
    
class CompletionAgent(Agent):
  def __init__(self, 
               config: Config,
               ):
    super().__init__(config)
    self.tokenizer = tiktoken.encoding_for_model(self.config.model)
  
  def check_prompt_length(self, prompt):
    total_tokens = len(self.tokenizer.encode(prompt))
    if total_tokens > (4097 - 1024):
      print(prompt)
      raise Exception("Too many tokens")
  
  def get_completion(self, user_prompt: str, context: Dict = None) -> str:
    prompt = user_prompt
    
    if not context is None:
      prompt = """{}
      
Context:
{}
""".format(prompt, '\n - '.join([""]+[f"{k}:{v}" for k,v in context.items()]))
    
    # print(prompt)
    
    self.check_prompt_length(prompt)
    
    if self.config.model.startswith('text-'):
      response = openai.Completion.create(
        model=self.config.model,
        prompt="""{}
        
        User: {}
        """.format(self.config.system_prompt, prompt),
        max_tokens=self.config.max_tokens,
        temperature=.2,
      )
      
      return response.choices[0].text
    elif self.config.model.startswith('gpt-'):
      messages = [
        {
          "role": "system",
          "content": self.config.system_prompt,
        },
        {
          "role": "user",
          "content": prompt,
        }
      ]
      
      response = openai.ChatCompletion.create(
        model=self.config.model,
        messages=messages,
        temperature=.2
      )
      
      return response.choices[0].message.content
    
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
      model=self.config.model,
      messages=self.messages,
      stream=self.config.stream,
    )
        
    agent_response = {"role": "", "content": ""}
    for line in response:
      if "role" in line.choices[0].delta:
        agent_response["role"] = line.choices[0].delta.role
      if "content" in line.choices[0].delta.keys():
        agent_response["content"] = agent_response["content"] + line.choices[0].delta.content
          
      yield line.choices[0].delta
        
    self.messages.append(agent_response)