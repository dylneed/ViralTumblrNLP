import argparse
import random
import json

def split(arr,ratio):
  random.shuffle(arr)
  arr_len = len(arr)
  split_point = int(arr_len * ratio)
  return (arr[:split_point],arr[split_point:])

def main(args):
  with open(args.data,"r") as f: posts = json.load(f)
  (train,test) = split(posts, 0.9)
  with open("../Train/" + args.data, "w") as f:json.dump(train, f)
  with open("../Test/" + args.data, "w") as f:json.dump(test, f)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Splits a JSON file of data into a test group and a train group")
  parser.add_argument(
    "data",
    help="The JSON file containing all the data for a certain tag"
  )
  args = parser.parse_args()
  main(args)