import kernel
import os
import re
import traceback

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
  action_agent = kernel.CompletionAgent(
    config=kernel.Config(
      openai_key=os.getenv("OPENAI_API_KEY"),
      system_prompt="""Given an input from the user, your job is to suggest what action to perform next to address
the user's need. Every action you suggest must accomplish a singular goal. Be as specific and comprehensive
as you possibly can. Start every action with a "#" followed by a ".".
"""
    )
  )
  
  chat_agent = kernel.ChatAgent(
    config=kernel.Config(
      openai_key=os.getenv("OPENAI_API_KEY"),
      stream_chat=True,
      system_prompt="""
You are an extended AI agent called MarkI.
"""
    )
  )

  try:
    user_input = "What's the status of my uscis case?"

    context = None
    
    for i in range(0, 3):
      action = action_agent.get_completion(user_input, context)
      
      print(action, re.match(r"(?i)check|visit|website", action))
      if not re.match(r"(?i)check|visit|website", action) is None:
        print("Need to visit a website")
      
      context = {
        "Past Action": action,
      }
      
    
    # results = kernel.web.search(query)
    # relevant = completion_agent.get_completion(
    #   user_input, 
    #   dict(search_results=[(result.string, result["href"]) for result in results[:5]])
    # ) 

    # # print(relevant)
    # match = re.search(r"\('([a-zA-Z0-9\s.:|]+)',\s*'([a-zA-Z0-9?/=.:&_%-]+)'\)", relevant)
    # title, url = match.group(1), match.group(2)
    # soup = kernel.web.get(url)
    # print(f"Clicked on '{title}'")
    
    # # context = [p.text for p in soup.find_all('p')]
    # context = soup.text
    # # print(context)
    
    # response = chat_agent.chat(f"{user_input}\r\nWeb Result:{context}")
    # print("<<", end=" ")
    # for line in response:
    #   if "content" in line:
    #     print(line.content, flush=True, end="")
    # print()
  except EOFError:
    exit(0)
  except AttributeError:
    # print(relevant)
    # if not match is None:
    #   print(match)
      
    traceback.print_exc()
    exit(1)
