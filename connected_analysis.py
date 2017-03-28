#!/usr/bin/python
# -*- coding: utf-8 -*-

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


def count_and_save_connected_components(g, filename):
    reach_dist = []
    n = len(list(g.vertices()))
    for v in g.get_vertices():
        if g.vertex_index[v] % 2000 == 0:
            print g.vertex_index[v]
        label = gt.label_out_component(g, v)
        label = label.get_array()
        reach = np.sum(label)
        reach_dist.append(int(reach))
    add_property(g, "reach_dist", "vector<int32_t>", reach_dist)
    g.save(filename)


def basic_statistics(reaches, name):
    print "Number of vertices: {}".format(reaches.size)
    mean = np.mean(reaches)
    max_deg = np.max(reaches)
    min_deg = np.min(reaches)
    std_dev = np.std(reaches)
    print "{} Mean: {}".format(name, mean)
    print "{} Std.Deviation: {}".format(name, std_dev)
    print "{} Max: {}".format(name, max_deg)
    print "{} Min: {}".format(name, min_deg)


def draw_distribution(reaches, name, filename_core):
    slash_index = filename_core.index("/")
    basefilename = filename_core[slash_index+1:]
    basefilename = "outputs/reaches/" + basefilename
    unique, counts = np.unique(reaches, return_counts=True)
    nunique = range(np.max(unique)+1)
    ncounts = []
    for i in range(np.max(unique)+1):
        if i in unique:
            ncounts.append(counts[np.where(unique == i)[0][0]])
        else:
            ncounts.append(0)
    ncounts = np.array(ncounts, dtype="double")
    pdf = ncounts / reaches.size
    cdf = np.cumsum(pdf)

    plt.plot(nunique, pdf)
    plt.title(u"Distribuição empírica de alcance")
    plt.xlabel(u"Alcance")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+name+"-dist.png", bbox_inches='tight')
    plt.clf()

    plt.semilogy(nunique, pdf)
    plt.title(u"Distribuição empírica de alcance (Escala log em Y)")
    plt.xlabel(u"Alcance")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+name+"-dist-logy.png", bbox_inches='tight')
    plt.clf()

    plt.plot(nunique, cdf)
    plt.title(u"Distribuição empírica cumulativa de alcance")
    plt.xlabel(u"Alcance")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+name+"-cumdist.png", bbox_inches='tight')
    plt.clf()

    print "Saved plots for {}".format(name)

if __name__ == '__main__':

    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-f', help="filename to load from")
    ARGPARSER.add_argument('-d', help="compute connected components",
                           default=False, action='store_true')
    ARGS = ARGPARSER.parse_args()

    filename = ARGS.f
    dot_index = filename.index(".")
    filename_core = filename[:dot_index]
    g = load(filename)

    if ARGS.d:
        count_and_save_connected_components(g, filename)
        print "DONE!"
    else:
        reach_dist = g.gp.reach_dist.get_array()

        print "-------------"
        basic_statistics(reach_dist, "Reach")
        print "-------------"
        draw_distribution(reach_dist, "reach", filename_core)
        print "-------------"
        print "DONE!"
