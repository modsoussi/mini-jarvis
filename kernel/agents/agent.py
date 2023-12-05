from kernel.agents.config import Config
from kernel.context import Context
from openai import OpenAI
import tiktoken

class Agent:
  def __init__(self, openai_key: str, config: Config) -> None:
    self.config = config
    self.openai_client = OpenAI(api_key=openai_key)
    if self.config.model is None:
      raise Exception("Agent configuration model cannot be None")
    
class ChatCompletionAgent(Agent):
  def __init__(self,
               openai_key: str,
               config: Config,
               ):
    super().__init__(openai_key, config)
    self.tokenizer = tiktoken.encoding_for_model(self.config.model)
  
  def validate_prompt_length(self, prompt):
    total_tokens = len(self.tokenizer.encode(prompt))
    if total_tokens > (self.config.max_len_context - self.config.max_tokens):
      print(prompt)
      raise Exception(f"Too many tokens: {total_tokens + self.config.max_tokens}")
    
  def handle_prompt(self, prompt: str) -> str:
    if self.config.model.startswith('text-'):
      response = self.openai_client.chat.completions.create(
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
      
      response = self.openai_client.chat.completions.create(
        model=self.config.model,
        messages=messages,
        temperature=.2
      )
      
      return response.choices[0].message.content
  
  def get_completion(self, user_prompt: str, context: Context = None) -> str:
    prompt = user_prompt
    
    if context is not None:
      prompt = """{}
   
Memory:
{}

Action Input:
{}
""".format(
    prompt,
    "\n".join([f"* {mem}" for mem in context.memory]),
    context.input,
    )
    
    # self.validate_prompt_length(prompt)
    
    return self.handle_prompt(prompt)