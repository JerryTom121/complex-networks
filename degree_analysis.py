#!/usr/bin/python
# -*- coding: utf-8 -*-

import graph_tool.all as gt

import argparse
import numpy as np
import matplotlib.pyplot as plt


def load(filename):
    return gt.load_graph(filename)


def extract_degrees(g):
    deg_in = g.get_in_degrees(g.get_vertices())
    deg_out = g.get_out_degrees(g.get_vertices())
    return deg_in, deg_out


def basic_statistics(degrees, sid):
    mean = np.mean(degrees)
    max_deg = np.max(degrees)
    min_deg = np.min(degrees)
    std_dev = np.std(degrees)
    print "{} Degree Mean: {}".format(sid, mean)
    print "{} Degree Std.Deviation: {}".format(sid, std_dev)
    print "{} Degree Max: {}".format(sid, max_deg)
    print "{} Degree Min: {}".format(sid, min_deg)


def draw_distribution(degrees, sid, filename_core):
    slash_index = filename_core.index("/")
    basefilename = filename_core[slash_index+1:]
    basefilename = "outputs/degrees/" + basefilename
    unique, counts = np.unique(degrees, return_counts=True)
    pdf = counts.astype("double") / degrees.size
    cdf = np.cumsum(pdf)

    plt.plot(unique, pdf)
    plt.title(u"Distribuição empírica de grau")
    plt.xlabel(u"Grau")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+sid+"-dist.png", bbox_inches='tight')
    plt.clf()

    plt.semilogy(unique, pdf)
    plt.title(u"Distribuição empírica de grau (Escala log em Y)")
    plt.xlabel(u"Grau")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+sid+"-dist-logy.png", bbox_inches='tight')
    plt.clf()

    plt.plot(unique, cdf)
    plt.title(u"Distribuição empírica cumulativa de grau")
    plt.xlabel(u"Grau")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+sid+"-cumdist.png", bbox_inches='tight')
    plt.clf()

    print "Saved plots for {} degrees".format(sid)

if __name__ == '__main__':

    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-f', help="filename to load from")
    ARGS = ARGPARSER.parse_args()

    filename = ARGS.f
    dot_index = filename.index(".")
    filename_core = filename[:dot_index]
    g = load(filename)
    deg_in, deg_out = extract_degrees(g)

    print "----------"
    basic_statistics(deg_in, "In")
    print "----------"
    basic_statistics(deg_out, "Out")
    print "----------"
    draw_distribution(deg_in, "in", filename_core)
    draw_distribution(deg_out, "out", filename_core)
    print "----------"
    print "DONE!"
