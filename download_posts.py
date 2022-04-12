import pytumblr
import argparse
import time
import json
import importlib.util       
 
# This is a file outside the git storage
# Kept private so no one can use the secret keys
spec = importlib.util.spec_from_file_location("api_keys", "../api_keys.py")
api_keys = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_keys)

client = pytumblr.TumblrRestClient(
  api_keys.consumer_key,
  api_keys.consumer_secret,
  api_keys.oauth_token,
  api_keys.oauth_secret
)

def posts_by_tag(tag, n=20, outname="raw_data.json"):
  # Keeps track of the number of successfully grabbed text only posts, as well as every post that was passed over
  total_posts = 0
  non_text_count = 0

  # The way to recur through more than 20 posts at a time, and not have repeats
  current_timestamp = None

  # Holds each post from the api call, so be fed into a JSON file after collection
  posts = []

  # When the code is waiting for the API to allow it back in, note which attempt is the first pass
  first_pass_waiting = True

  while(True):
    for post in client.tagged(tag=tag, filter="raw", before=current_timestamp, limit=20):
      try:
        # Tests if the hourly/daily limit has been reached
        if post == "response" or post == "meta" or post == "errors":
          # Saves the collected data into the json file when the limit is reached so if it's cancelled the data is still usable
          with open(outname,"w") as f: json.dump(posts,f)

          # On the first pass, print how many posts have been grabbed and how many have been skipped
          if first_pass_waiting:
            first_pass_waiting = False
            print("Number of posts:", total_posts)
            print(non_text_count, "posts skipped")
            print()
          
          # If it the limit has been reached, wait a minute to not stress out the servers, then try again
          time.sleep(60)
          continue

        # Resets first_pass_waiting because it;s no longer waiting
        if not first_pass_waiting: first_pass_waiting = True

        if post["type"] != "text" or "<figure class=" in post["body"] or "<img src" in post["body"]: non_text_count += 1
        else:
          # Update the running total and now look before this post was posted
          total_posts += 1
          current_timestamp = post["timestamp"]

          # Add the post to the running list of posts
          posts.append(post)

          # If we've colleceted the number of posts we want go here
          if total_posts >= n:
            # Tells us how many posts as a quick check that it did it correctly, and tells us how many were skipped
            print("Number of posts: ", total_posts)
            print(non_text_count, "posts skipped")

            # Save the array we've been collecting posts in into a json file we can use with other files
            with open(outname,"w") as f: json.dump(posts,f)
            return
      except Exception as e:
        # When an error is reached, print the error, and what the post data looked like
        print("Error:")
        print(e)
        print(post)

        # Even when there is an error, take the rest of the posts collected and put them in the JSON file
        with open(outname,"w") as f: json.dump(posts,f)
        return

def main(args):
  outname = args.tag + "_raw_data.json" if args.output == None else args.output
  posts_by_tag(args.tag, n=args.num, outname=outname)

if __name__ == "__main__":
  # Lets this be used with the command line
  parser = argparse.ArgumentParser(description="Downloads the JSON for a certain amount of text only posts within a tag")
  parser.add_argument(
    "--tag",
    "-t",
    default="submission",
    help="The tag to grab the most recent text-only posts from"
  )
  parser.add_argument(
    "--num",
    "-n",
    type=int,
    default=10000,
    help="The number of text-only posts to grab from with the specified tag"
  )
  parser.add_argument(
    "--output",
    "-o",
    required=False,
    help="The JSON file to dump the data from the API call into"
  )
  
  args = parser.parse_args()
  main(args)