import argparse
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot
import os

def scatter(x_axis, y_axis, x_label, y_label, test_name, tag, x_scale="linear", y_scale="linear", boundaries=[],trendline=[]):
  pyplot.xscale(x_scale)
  pyplot.yscale(y_scale)
  pyplot.plot(x_axis, y_axis,"b+")
  pyplot.plot([n + 1 for n in range(len(trendline) - 1)], trendline[1:],"r-")
  if (boundaries == []): pyplot.margins(0.2, 0.2)
  else: pyplot.axis(boundaries)
  pyplot.xscale(x_scale)
  pyplot.yscale(y_scale)
  pyplot.xlabel(x_label)
  pyplot.ylabel(y_label)
  pyplot.title("Effects of " + test_name + " on " + tag)
  if not os.path.exists("../Graphs/" + tag): os.makedirs("../Graphs/" + tag)
  pyplot.savefig("../Graphs/" + tag + "/" + test_name.replace(" ", "_").lower() + ".png")

def main(args):
  ...

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="")
  args = parser.parse_args()
  main(args)