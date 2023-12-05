import kernel
import prompts.sys
from playwright.sync_api import sync_playwright

k = kernel.Kernel()

if __name__ == "__main__":
  action_agent = k.new_completion_agent(
    config=kernel.Config(
      model="gpt-4-1106-preview",
      system_prompt=prompts.sys.action_gen
    )
  )

  with sync_playwright() as p:
    try:
      user_input = input(">> ")
      if user_input == ":q":
        exit(0)
      
      browser = kernel.Browser(p)
      context = kernel.Context()
      
      while True:
        action = kernel.Action(action_agent.get_completion(user_input, context), browser=browser)
        print(action.desc())
        result = action.exec()
        
        if action.action_type == kernel.ACTION_TYPE_FINAL:
          print(result)
          browser.close()
          exit(0)
        
        context.input = result
        if action.past_result is not None:
          context.add(action.past_result)
    
    except EOFError:
      if browser is not None:
        browser.close()
      exit(0)
    except KeyboardInterrupt:
      if browser is not None:
        browser.close()
      exit(0)
