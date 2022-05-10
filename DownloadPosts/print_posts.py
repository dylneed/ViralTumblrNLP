from bs4 import BeautifulSoup
import argparse
import json

def print_post(post):
  print(post["short_url"])
  print(post["id"])
  print(post["blog_name"])
  print(post["date"])
  print(post["timestamp"])
  print(BeautifulSoup(post["body"],features="lxml").get_text('\n'))
  notes = post["note_count"]
  note_str = str(notes) + " note" if notes == 1 else str(notes) + " notes"
  print(note_str)
  print("#" + " #".join(post["tags"]))
  print()
  print("--------------------")
  print()

def print_posts(posts):
  for post in posts:
    print_post(post)
  print(str(len(posts)), "total posts")

def main(args):
  posts = json.load(args.JSONFile)
  print_posts(posts)

if __name__ == "__main__":
  # Lets this be used with the command line
  parser = argparse.ArgumentParser(description="Takes the raw JSON files and prints out the useful functions, works on both the raw data and the cleaned data")
  parser.add_argument(
    "JSONFile",
    type=argparse.FileType("r"),
    help="The JSON file of posts to be printed"
  )

  args = parser.parse_args()
  main(args)