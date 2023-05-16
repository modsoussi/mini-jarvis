import kernel
import os
import re
from bs4 import BeautifulSoup
import json

from dotenv import load_dotenv

load_dotenv()

system_prompt = """1. You are a helpful AI agent called MARKI. When the context has enough data to address the user's need,
output your final answer prefixed with [final-answer], otherwise generate an action to perform 
to get you closer to addressing the user's need.
2. Do not repeat the same action twice.
3. When the Context is empty or None, simply ignore it. 
4. Do not repeat actions that have already been done.
5. Actions must accomplish a singular goal. You must be as specific as you possibly can, and do not combine actions.
6. If you don't need to browse the web or perform a google search to address the user's need, then directly output the final answer.
7. For every action you generate, start with one of the following action types:
  * [google-search]: when you need to perform a google search
  * [web-browse]: when you need to browse the web
  * [ask-for-info]: when there's missing data needed from the user to complete their request
  * [final-answer]: when you have an aswer to the user's input from the context.
  * [other]: when the action is none of the above

  - Only when the action type is [google-search], output a [query].
  - Only when the action type is [web-browse], output a [url], [method], and [params], where method is an http method, and [params] are double-quoted JSON.
  - Only when the action type is [ask-for-info], you must output a [prompt] param.
  - Only when the action type is [final-answer], output the source of your final answer.
8. When giving your final answer, cite your source either from context or from what you know.

Examples:

User: What's the weather in miami beach today?

[google-search]
[query] weather in miami beach

---

User: What's the largest social app?

[google-search]
[query] largest social app

---
"""

if __name__ == "__main__":
  action_agent = kernel.CompletionAgent(
    config=kernel.Config(
      openai_key=os.getenv("OPENAI_API_KEY"),
      model="gpt-3.5-turbo",
      system_prompt=system_prompt
    )
  )

  try:
    user_input = input(">> ")

    context = {"Past Actions and Results": [] }
    
    action_ord = 0
    while True:
      results = {}
      # print(f"***\nContext:\n{context}\n***")
      
      action = action_agent.get_completion(user_input, context)
      action_ord += 1
      results[f"Action #{action_ord}"] = action
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
            search_results = kernel.web.search(query)
            results[f"Action #{action_ord} Results"] = search_results
        elif action_type == "[web-browse]":
          method = None
          url = None
          params = None
          for line in parts[1:]:
            m = re.search(r"(?s)(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", line)
            if not m is None:
              param, val = m.group(1), m.group(2)
              if param == "[url]":
                url = val
              elif param == "[method]":
                method = val
              elif param == "[params]":
                m = re.search(r"(\{.*\})", val)
                if not m is None:
                  val = m.group(1)
                  if val != "None":
                    params = json.loads(val)
          
          if url is None or method is None:
            raise Exception("missing url or method")
          
          response = None
          if method == "GET":
            print(f"Clicked on {url} with {params}")
            soup = kernel.web.get(url, params=params)
            if not soup.body is None:
              text = re.sub(r"[ \r\n\xa0]+", " ", soup.body.text)
              forms = [
                {
                  "form_action": form.get("action"), 
                  "form_method": form.get("method"),
                  "form_params": [
                    {
                      inp.get("name"): inp.get("value")
                    } for inp in form.find_all("input") if inp["type"] != "hidden" and not inp.get("name") is None]
                } for form in soup.find_all("form")]
              results[f"Action #{action_ord} Results"] = [text, forms]
            else:
              print(soup.body)
          elif method == "POST":
            print(f"POST {url} with params: {params}")
            post_result = kernel.web.post(url, data=params)
            if type(post_result) is BeautifulSoup:
              post_result = re.sub(r"[ \r\t\n]+", " ", post_result.body.text)
            
            results[f"Action #{action_ord} Results"] = post_result
        elif action_type == "[ask-for-info]":
          m = re.search(r"(?s)(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", parts[1])
          if m.group(1) == "[prompt]":
            prompt = m.group(2)
            print(f"{prompt}")
            results[f"Action #{action_ord} Results"] = input("> ")
        elif action_type == "[final-answer]":
          exit(0)
            
      context["Past Actions and Results"] = [results] + context["Past Actions and Results"]
      print("----")
  except EOFError:
    exit(0)
  except KeyboardInterrupt:
    exit(0)
