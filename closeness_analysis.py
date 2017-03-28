#!/usr/bin/python
# -*- coding: utf-8 -*-

import graph_tool.all as gt

import argparse
import numpy as np
import matplotlib.pyplot as plt


def load(filename):
    return gt.load_graph(filename)


def compute_and_save_closeness(g, filename):
    cl = gt.closeness(g)
    g.vertex_properties["closeness"] = cl
    g.save(filename)


def basic_statistics(closeness, name):
    mean = np.mean(closeness)
    max_deg = np.max(closeness)
    min_deg = np.min(closeness)
    std_dev = np.std(closeness)
    print "{} Mean: {}".format(name, mean)
    print "{} Std.Deviation: {}".format(name, std_dev)
    print "{} Max: {}".format(name, max_deg)
    print "{} Min: {}".format(name, min_deg)


def draw_histogram(closeness, name, filename_core):
    slash_index = filename_core.index("/")
    basefilename = filename_core[slash_index+1:]
    basefilename = "outputs/closeness/" + basefilename

    plt.hist(closeness, 80)
    plt.title(u"Histograma do Closeness")
    plt.xlabel(u"Closeness")
    plt.ylabel(u"Número de vértices")
    plt.savefig(basefilename+"-"+name+"-hist.png", bbox_inches='tight')
    plt.clf()

    plt.hist(closeness, 80)
    plt.title(u"Histograma do Closeness")
    plt.xlabel(u"Closeness")
    plt.ylabel(u"Número de vértices")
    plt.ylim(0, 1000)
    plt.savefig(basefilename+"-"+name+"-hist-zoom.png", bbox_inches='tight')
    plt.clf()

    print "Saved plots for {}".format(name)

if __name__ == '__main__':

    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-f', help="filename to load from")
    ARGPARSER.add_argument('-d', help="compute closeness",
                           default=False, action='store_true')
    ARGS = ARGPARSER.parse_args()

    filename = ARGS.f
    dot_index = filename.index(".")
    filename_core = filename[:dot_index]
    g = load(filename)

    if ARGS.d:
        compute_and_save_closeness(g, filename)
        print "DONE!"
    else:
        closeness = g.vp.closeness.get_array()
        closeness = closeness[~np.isnan(closeness)]

        print "-------------"
        basic_statistics(closeness, "Closeness")
        print "-------------"
        draw_histogram(closeness, "closeness", filename_core)
        print "-------------"
        print "DONE!"
