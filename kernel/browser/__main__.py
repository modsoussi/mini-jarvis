from . import Browser

def main():
  while True:
    try:
      url = input("Enter a URL: ")
      print(Browser().get(url))
    except EOFError:
      exit(0)
    except KeyboardInterrupt:
      exit(0)
    
if __name__ == "__main__":
  main()