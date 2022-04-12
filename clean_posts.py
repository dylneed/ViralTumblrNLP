import json
import argparse
from bs4 import BeautifulSoup

# Grabs the parts I think will be necessary for any NLP experiment I want to run on the data, and gets rid of the rest.
def clean_post(post):
  out = dict()
  for i in ["blog_name", "id", "date", "timestamp", "tags", "short_url", "note_count"]:
    out[i] = post[i]
  # Converts the HTML text into just plain text
  out["body"] = BeautifulSoup(post["body"],features="lxml").get_text('\n')

  # Adds the title field to the 'body' because it's still text and thus will be important to look at
  try:
    out["body"] = post["title"] + "\n" + out["body"] if post["title"] != "" else out["body"]
  except:
    # I was occasionally getting an error when trying to access the file, and this is a quick and dirty fix
    ...
  return out

def clean_posts(posts): 
  out = []
  for post in posts:
    out.append(clean_post(post))
  return out

def main(args):
  posts = json.load(args.RawJSONFile)
  json.dump(clean_posts(posts), args.output)

if __name__ == "__main__":
  # Lets this be used with the command line
  parser = argparse.ArgumentParser(description="Takes the raw JSON file and pares it down to something much more managable")
  parser.add_argument(
    "RawJSONFile",
    type=argparse.FileType("r"),
    help="The raw JSON file made by taking data directly from the API call"
  )
  parser.add_argument(
    "--output",
    "-o",
    type=argparse.FileType("w"),
    default="clean_posts.json",
    help="The JSON file to dump the cleaned data into"
  )

  args = parser.parse_args()
  main(args)