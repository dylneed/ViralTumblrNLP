import argparse
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import string
from syllables import estimate as syll_count
import re

# Fog Index
def fog(body):
  words = 0
  sents = 0
  cpx = 0
  for sent in sent_tokenize(re.sub(r"\n",". ",body)):
    for word in word_tokenize(re.sub(r"["+string.punctuation+"]","",sent)):
      words += 1
      if syll_count(word) > 2: cpx += 1
    sents += 1
  if words == 0 or sents == 0: return 0
  return 0.4 * ((words / sents) + (100 * (cpx / words)))

# Flesch Index
def flesch(body):
  words = 0
  sents = 0
  sylls = 0
  for sent in sent_tokenize(re.sub(r"\n",". ",body)):
    for word in word_tokenize(re.sub(r"["+string.punctuation+"]","",sent)):
      words += 1
      sylls += syll_count(word)
    sents += 1
  if words == 0 or sents == 0: return 0
  return 206.835 - (1.015 * (words / sents)) - (84.6 * (sylls / words))

# Kincaid Index
# Flesch–Kincaid Grade Level Formula
def kincaid(body):
  words = 0
  sents = 0
  sylls = 0
  for sent in sent_tokenize(re.sub(r"\n",". ",body)):
    for word in word_tokenize(re.sub(r"["+string.punctuation+"]","",sent)):
      words += 1
      sylls += syll_count(word)
    sents += 1
  if words == 0 or sents == 0: return 0
  return (0.39 * (words / sents)) + (11.8 * (sylls / words)) - 15.59

def main(args):
  ...

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="")
  args = parser.parse_args()
  main(args)