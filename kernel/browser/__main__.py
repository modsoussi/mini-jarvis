from . import Browser
from playwright.sync_api import sync_playwright

def main():
  with sync_playwright() as p:
    browser = Browser(p)
    while True:
      try:
        response = browser.get(input(">> Enter a URL:"))
        print(response)
      except EOFError:
        exit(0)
      except KeyboardInterrupt:
        exit(0)
    
if __name__ == "__main__":
  main()