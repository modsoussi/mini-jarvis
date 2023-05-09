import kernel
import os
import re

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
  action_agent = kernel.CompletionAgent(
    config=kernel.Config(
      openai_key=os.getenv("OPENAI_API_KEY"),
      # model="text-davinci-003",
      model="gpt-3.5-turbo",
      system_prompt="""You are a helpful AI agent called MARKI. Given an input from the user, your job is to 
      generate an action to perform next to address the user's need, taking into account any previous action and results. 
      Actions must accomplish a singular goal. You must be as specific as you possibly can.
      For every action you generate, prefix with it with one of the following action types:
      [google-search]
      [web-browse]
      [ask-for-info]
      [final-answer]
      [other]

      If the action type is [google-search], output a [query].
      If the action type is [web-browse], output a [url] and [method].
      If the action type is [ask-for-info], include a [prompt] param.
      
      Examples:
      
      User: What's the weather in miami beach today?

      [google-search]
      [query] weather in miami beach
      
      User: What's the largest social app?
      
      [google-search]
      [query] largest social app
      """
    )
  )

  try:
    # user_input = "What's the status of my uscis case?"
    user_input = input(">> ")

    context = dict()
    
    for i in range(0, 6):
      action = action_agent.get_completion(user_input, context)
      print(action)
      parts = action.strip("\n").split("\n")
      
      m = re.search(r"(?s)(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", parts[0])
      if not m is None:
        action_type, action_text = m.group(1), m.group(2)
        print(f"Action Type: {action_type}")
        
        if action_type == "[google-search]":
          query = None
          m = re.search(r"(?s)(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", parts[1])
          if len(m.groups()) == 2 and m.group(1) == "[query]":
            query = m.group(2)
            print(f"Searching on Google: {query}")
            results = kernel.web.search(query)
            context["Last Results"] = results
        elif action_type == "[web-browse]":
          method = None
          url = None
          for line in parts[1:]:
            m = re.search(r"(?s)(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", line)
            if not m is None:
              param, val = m.group(1), m.group(2)
              if param == "[url]":
                url = val
              elif param == "[method]":
                method = val
              elif param == "[inputs]":
                print(val)
          
          if url is None or method is None:
            raise Exception("missing url or method")
          
          response = None
          if method == "GET":
            print(f"Clicked on {url}")
            soup = kernel.web.get(url)
            text = soup.body.text
            forms = [
              {
                "action": form.get("action"), 
                "method": form.get("method"),
                "inputs": [
                  {
                    "name": inp.get("name"),
                    "value": inp.get("value")
                  } for inp in form.find_all("input") if inp["type"] != "hidden"]
              } for form in soup.find_all("form")]
            context["Last Results"] = [text, forms]
          elif method == "POST":
            result = kernel.web.post(url, data=None)
            context["Last Results"] = result
        elif action_type == "[ask-for-info]":
          m = re.search(r"(?s)(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", parts[1])
          if m.group(1) == "[prompt]":
            prompt = m.group(2)
            print(f"{prompt}")
            context["Last Results"] = input("> ")
        elif action_type == "[final-answer]":
          print(parts[1:])
          exit(0)
            
      context["Past Action"] = action
      print("----")
  except EOFError:
    exit(0)
