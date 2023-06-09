import kernel
import os

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
      model="gpt-3.5-turbo-16k",
      system_prompt=system_prompt
    )
  )

  try:
    user_input = input(">> ")
    if user_input == ":q":
      exit(0)

    context = []
    while True:
      action = kernel.Action(action_agent.get_completion(user_input, context))
      print(action.desc())
      result = action.exec()
      
      if action.action_type == kernel.ACTION_TYPE_FINAL:
        print(result)
        exit(0)
      
      context.append((action.desc(), result))
  
  
  except EOFError:
    exit(0)
  except KeyboardInterrupt:
    exit(0)
