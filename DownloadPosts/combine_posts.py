import json
import argparse

def combine(posts_arr):
  out_posts = []
  ids = []
  for posts in posts_arr:
    for post in posts:
      if post["id"] in ids: continue
      out_posts.append(post)
      ids.append(post["id"])
  return out_posts

def main(args):
  posts_arr = []
  for file in args.JSONFiles:
    posts_arr.append(json.load(file))
  json.dump(combine(posts_arr), args.output)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Takes multiple JSON files and combines them so that each post appears once")
  parser.add_argument(
    "JSONFiles",
    nargs="+",
    type=argparse.FileType("r"),
    help="All the raw JSON files that need to be combined"
  )
  parser.add_argument(
    "--output",
    "-o",
    type=argparse.FileType("w"),
    default="clean_posts.json",
    help="The JSON file to dump the combined data into"
  )

  args = parser.parse_args()
  main(args)