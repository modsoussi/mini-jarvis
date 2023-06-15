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

    context = {"Past Actions and Results": [] }
    
    action_ord = 0
    while True:
      results = {}
      # print(f"***\nContext:\n{context}\n***")
      
      action = action_agent.get_completion(user_input, context)
      action_ord += 1
      results[f"Action #{action_ord}"] = action
      # print(action)
      parts = action.strip("\n").split("\n")
      
      m = re.search(r"(?s)(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", parts[0])
      if not m is None:
        action_type, action_text = m.group(1), m.group(2)
        # print(f"Action Type: {action_type}")
        
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
              text = re.sub(r"[ \r\n\xa0\t]+", " ", soup.body.text)
              forms = [
                {
                  "form_action": form.get("action"), 
                  "form_method": form.get("method"),
                  "form_params": [
                    {
                      inp.get("name"): inp.get("value")
                    } for inp in form.find_all("input") if inp["type"] != "hidden" and not inp.get("name") is None]
                } for form in soup.find_all("form")]
              links = [(a.text, a.get("href")) for a in soup.body.find_all("a") if not a.get("href") is None and a.get("href") != "javascript:void(0)"]
              results[f"Action #{action_ord} Results"] = [text, forms]
            else:
              print(soup.body)
          elif method == "POST":
            print(f"POST {url} with params: {params}")
            post_result = kernel.web.post(url, data=params)
            if type(post_result) is BeautifulSoup:
              post_result = re.sub(r"[ \r\t\n\xa0]+", " ", post_result.body.text)
            
            results[f"Action #{action_ord} Results"] = post_result
        elif action_type == "[ask-for-info]":
          m = re.search(r"(?s)(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", parts[1])
          if m.group(1) == "[prompt]":
            prompt = m.group(2)
            print(f"{prompt}")
            results[f"Action #{action_ord} Results"] = input("> ")
        elif action_type == "[final-answer]":
          print(action)
          exit(0)
            
      context["Past Actions and Results"] = [results] + context["Past Actions and Results"]
      print("----")
  except EOFError:
    exit(0)
  except KeyboardInterrupt:
    exit(0)
