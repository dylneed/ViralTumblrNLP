import nltk
import argparse

def gen_feats(post_text):
  features = {}
  unigrams = nltk.tokenize.word_tokenize(post_text)
  bigrams = [(a + "-" + b) for a,b in (list(zip(unigrams, unigrams[1:])))]
  trigrams = [(a + "-" + b + "-" + c) for a,b,c in (list(zip(unigrams, unigrams[1:],unigrams[2:])))]
  ngrams = nltk.FreqDist(w.lower() for w in (unigrams + bigrams + trigrams))
  limit = 5 if len(ngrams) > 5 else len(ngrams)
  for w in list(ngrams)[:limit]:
    features["contains-" + w.lower()] = 1
  return features

def classifier(train_posts):
  training = [(gen_feats(post["body"]), post["note_count"]) for post in train_posts]
  return nltk.NaiveBayesClassifier.train(training)

def generate_labels(classifier,test_posts):
  feature_sets = [gen_feats(post["body"]) for post in test_posts]
  return [classifier.classify(feature_set) for feature_set in feature_sets]

def accuracy(trained, test):
  return nltk.classify.accuracy(trained, test)

def main(args):
  ...

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="")
  args = parser.parse_args()
  main(args)