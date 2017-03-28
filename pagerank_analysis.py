#!/usr/bin/python
# -*- coding: utf-8 -*-

import graph_tool.all as gt

import argparse
import numpy as np
import matplotlib.pyplot as plt


def load(filename):
    return gt.load_graph(filename)


def compute_and_save_pagerank(g, filename):
    pr = gt.pagerank(g)
    g.vertex_properties["pagerank"] = pr
    g.save(filename)


def basic_statistics(pagerank, name):
    mean = np.mean(pagerank)
    max_deg = np.max(pagerank)
    min_deg = np.min(pagerank)
    std_dev = np.std(pagerank)
    print "{} Mean: {}".format(name, mean)
    print "{} Std.Deviation: {}".format(name, std_dev)
    print "{} Max: {}".format(name, max_deg)
    print "{} Min: {}".format(name, min_deg)


def draw_histogram(pagerank, name, filename_core):
    slash_index = filename_core.index("/")
    basefilename = filename_core[slash_index+1:]
    basefilename = "outputs/pagerank/" + basefilename

    plt.hist(pagerank, 80)
    plt.title(u"Histograma do Pagerank")
    plt.xlabel(u"Pagerank")
    plt.ylabel(u"Número de vértices")
    plt.savefig(basefilename+"-"+name+"-hist.png", bbox_inches='tight')
    plt.clf()

    plt.hist(pagerank, 80)
    plt.title(u"Histograma do Pagerank")
    plt.xlabel(u"Pagerank")
    plt.ylabel(u"Número de vértices")
    plt.ylim(0, 20)
    plt.savefig(basefilename+"-"+name+"-hist-zoom.png", bbox_inches='tight')
    plt.clf()

    print "Saved plots for {}".format(name)

if __name__ == '__main__':

    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-f', help="filename to load from")
    ARGPARSER.add_argument('-d', help="compute pagerank",
                           default=False, action='store_true')
    ARGS = ARGPARSER.parse_args()

    filename = ARGS.f
    dot_index = filename.index(".")
    filename_core = filename[:dot_index]
    g = load(filename)

    if ARGS.d:
        compute_and_save_pagerank(g, filename)
        print "DONE!"
    else:
        pagerank = g.vp.pagerank.get_array()

        print "-------------"
        basic_statistics(pagerank, "Pagerank")
        print "-------------"
        draw_histogram(pagerank, "pagerank", filename_core)
        print "-------------"
        print "DONE!"
