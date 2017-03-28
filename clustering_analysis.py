#!/usr/bin/python

import graph_tool.all as gt

import argparse
import numpy as np
import matplotlib.pyplot as plt


def load(filename):
    return gt.load_graph(filename)


def add_property(g, name, gtype, content):
    gproperty = g.new_graph_property(gtype)
    g.graph_properties[name] = gproperty
    g.graph_properties[name] = content


def compute_and_save_global_clustering(g, filename):
    clust = gt.local_clustering(g, undirected=False)[0]
    add_property(g, "clustering", "double", clust)
    g.save(filename)

if __name__ == '__main__':

    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-f', help="filename to load from")
    ARGPARSER.add_argument('-d', help="compute clustering",
                           default=False, action='store_true')
    ARGS = ARGPARSER.parse_args()

    filename = ARGS.f
    dot_index = filename.index(".")
    filename_core = filename[:dot_index]
    g = load(filename)

    if ARGS.d:
        compute_and_save_global_clustering(g, filename)
        print "DONE!"
    else:
        print "Clustering factor:", g.gp.clustering
        print "DONE!"
