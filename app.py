import kernel
import os
import re
from bs4 import BeautifulSoup
import json

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
  # read system prompt from prompts folder
  system_prompt = ""
  with open("prompts/sys.txt") as f:
    system_prompt = f.read()
  
  action_agent = kernel.CompletionAgent(
    config=kernel.Config(
      openai_key=os.getenv("OPENAI_API_KEY"),
      model="gpt-3.5-turbo-0613",
      system_prompt=system_prompt
    )
  )

  try:
    user_input = input(">> ")
    if user_input == ":q":
      exit(0)

    context = [()]
    
    action_ord = 0
    while True:
      results = {}
      # print(f"***\nContext:\n{context}\n***")
      
      action = kernel.Action(action_agent.get_completion(user_input, context))
      result = action.exec()
      
      if action.action_type == kernel.ACTION_TYPE_FINAL:
        print(result)
        exit(0)
      
      context.append((action.desc(), result))
      # print("----")
  except EOFError:
    exit(0)
  except KeyboardInterrupt:
    exit(0)
