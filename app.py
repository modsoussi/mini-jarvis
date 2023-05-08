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
      model="text-davinci-003",
      # model="gpt-3.5-turbo",
      system_prompt="""You are a helpful AI agent called MARKI. Given an input from the user, your job is to 
      generate an action to perform next to address the user's need. 
      Actions must accomplish a singular goal. You must be as specific as you possibly can.
      For every action you generate, prefix with it with one of the following action types:
      [google-search]
      [web-browse]
      [other]

      If the action type is [google-search], output a [query].
      If the action type is [web-browse], output a [url] and http [method] and any [params] needed.
      
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
    
    for i in range(0, 3):
      action = action_agent.get_completion(user_input, context)
      
      m = re.search(r"(?:\w\s)*:?\s*(\[.*?\])\s*(.*)", action)
      if not m is None:
        action_type, action_text = m.group(1), m.group(2)
        print(f"Action: {action}")
        print(f"Action Type: {action_type}")
        print(f"Action Text: {action_text}")
        
        if action_type == "[google-search]" and action_text.startswith("[query] "):
          query = action_text[8:]
          print(f"Searching Google for: {query}")
          results = kernel.web.search(query)
          print(results)
          context["Results"] = results
        elif action_type == "[web-browse]" and action_text.startswith("[url] "):
          url = action_text[6:]
          soup = kernel.web.get(url)
          forms = [(form["action"], form["method"], form.find_all("input")) for form in soup.find_all("form")]
          context["Results"] = forms
      
      context["Past Action"] = action
      print("----")
  except EOFError:
    exit(0)
