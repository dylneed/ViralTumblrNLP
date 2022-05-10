import argparse
import json
import numpy

import readability
import graph
import naive_bayes

def generate_trendline(x_axis,y_axis):
  trend_func = numpy.polynomial.polynomial.polyfit(x_axis, y_axis, 1)
  trendline = []
  for x in range(int(max(x_axis) + (0.2 * max(x_axis)))):
    point = 0
    for exp in range(len(trend_func)):
      point += trend_func[exp] * (x ** exp)
    trendline.append(point)
  return trendline

def time_test(posts, tag):
  notes = [post["note_count"] for post in posts]
  timestamp = [int(post["timestamp"]/10000) for post in posts]
  trendline = generate_trendline(timestamp,notes)
  graph.scatter(timestamp, notes, "Tumblr Timestamp", "Notes", "Time", tag, "linear","log",[min(timestamp)-int(0.0001 * min(timestamp)),max(timestamp)+int(0.0001 * min(timestamp)),1,max(notes)], trendline=trendline)
  return trendline

def num_tags_test(posts, tag):
  notes = [post["note_count"] for post in posts]
  tags = [len(post["tags"]) for post in posts]
  trendline = generate_trendline(tags,notes)
  graph.scatter(tags, notes, "Number of Tags", "Notes", "Number of Tags", tag, "linear","log",[0,max(tags)+1,1,max(notes)], trendline=trendline)
  return trendline


def readability_test(posts, tag, index_type="fog"):
  notes = [post["note_count"] for post in posts]
  if (index_type == "fog"):
    fog = [readability.fog(post["body"]) for post in posts]
    notes = [post["note_count"] for post in posts]
    fog_trendline = generate_trendline(fog,notes)
    graph.scatter(fog, notes, "Fog Index", "Notes", "Fog Index", tag, "linear","log", [0,45,1,110000], trendline=fog_trendline)
    return fog_trendline
  if (index_type == "flesch"):
    flesch = [readability.flesch(post["body"]) for post in posts]
    notes = [post["note_count"] for post in posts]
    flesch_trendline = generate_trendline(fog,notes)
    graph.scatter(flesch, notes, "Flesch Index", "Notes", "Flesch Index", tag, "linear","log", [0,45,1,110000], trendline=flesch_trendline)
    return flesch_trendline
  if (index_type == "kincaid"):
    kincaid = [readability.kincaid(post["body"]) for post in posts]
    notes = [post["note_count"] for post in posts]
    kincaid_trendline = generate_trendline(fog,notes)
    graph.scatter(kincaid, notes, "Kincaid Index", "Notes", "Kincaid Index", tag, "linear","log", [0,45,1,110000], trendline=kincaid_trendline)
    return kincaid_trendline
  return None

def report_accuracy(test, actual):
  if len(test) != len(actual): return None
  differences = []
  for i in range(len(actual)):
    # act = 1 if actual[i] == 0 else actual[i]
    if actual[i] == test[i]:
      differences.append(1)
    else:
      differences.append(1-(abs(actual[i] - abs(test[i])) / max(actual[i],abs(test[i]))))
  return sum(differences)/len(differences)
  

def perform_test(test_posts,test_data,trendline):
  test_notes = []
  run_test = []
  for i in range(len(test_posts)):
    data = int(test_data[i])
    if data >= len(trendline) or data < 0 or data == None: continue
    len(trendline)
    test_notes.append(test_posts[i]["note_count"])
    run_test.append(trendline[data])
  return report_accuracy(run_test, test_notes)

def main(args):
  with open("../Train/" + args.tag+ ".json","r") as f: train_posts = json.load(f)
  with open("../Test/"+ args.tag + ".json","r") as f: test_posts = json.load(f)

  print("Timestamp accuracy: " + str(
    perform_test(
      test_posts, 
      [int(post["timestamp"]/10000)for post in test_posts], 
      time_test(train_posts, args.tag)) * 100) + "%")
  print("Number of Tags Accuracy: " + str(
    perform_test(
      test_posts,
      [len(post["tags"]) for post in test_posts],
      num_tags_test(train_posts,args.tag)) * 100) +"%")
  print("Fog accuracy: " + str(
    perform_test(
      test_posts, 
      [readability.fog(post["body"]) for post in test_posts], 
      readability_test(train_posts, args.tag, "fog")) * 100) + "%")
  classifier = naive_bayes.classifier(train_posts)
  print("Naive-Bayes Accuracy: " + str(
    report_accuracy(
      naive_bayes.generate_labels(classifier, test_posts),
      [post["note_count"] for post in test_posts]
    ) * 100) + "%")
  with open("../Graphs/" + args.tag + "/Naive_Bayes_Classifier.txt", "w") as f: f.write("\n".join([str(a) + "  " + str(b) for a,b in classifier.most_informative_features(100)]))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="")
  parser.add_argument(
    "tag",
    help="tag to run the experiment on"
  )
  args = parser.parse_args()
  main(args)