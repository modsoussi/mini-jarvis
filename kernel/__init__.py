import os
from kernel.agents.config import Config
from kernel.agents import CompletionAgent
from kernel.actions.action import Action, ACTION_TYPE_FINAL, ACTION_TYPE_ASK_FOR_INFO, ACTION_TYPE_SEARCH, ACTION_TYPE_WEB_BROWSE
from kernel.browser import Browser
from kernel.context import Context

from dotenv import load_dotenv

load_dotenv()

class Kernel:
  def __init__(self) -> None:
    self.openai_key = os.getenv("OPENAI_API_KEY")
  
  def new_completion_agent(self, config: Config) -> CompletionAgent:
    return CompletionAgent(self.openai_key, config)

__all__ = [
  'CompletionAgent',
  'Config',
  'Action',
  'ACTION_TYPE_ASK_FOR_INFO',
  'ACTION_TYPE_FINAL',
  'ACTION_TYPE_SEARCH',
  'ACTION_TYPE_WEB_BROWSE',
  'Browser',
  'Context',
  'Kernel'
]