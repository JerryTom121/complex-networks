#!/usr/bin/python
# -*- coding: utf-8 -*-

import graph_tool.all as gt

import argparse
import numpy as np
import matplotlib.pyplot as plt

MAX_INT = 2147483647


def load(filename):
    return gt.load_graph(filename)


def add_property(g, name, gtype, content):
    gproperty = g.new_graph_property(gtype)
    g.graph_properties[name] = gproperty
    g.graph_properties[name] = content


def compute_and_save_distance_info(g, filename):
    max_dist = []
    min_dist = []
    mean_dist = []
    stddev_dist = []
    overall_dist = {}
    for v in g.get_vertices():
        if g.vertex_index[v] % 2000 == 0:
            print g.vertex_index[v]
        dist_map = gt.shortest_distance(g, v)
        dist_map = dist_map.get_array().astype("int32")
        dist_map = dist_map[(dist_map != MAX_INT) & (dist_map != 0)]
        if dist_map.size:
            max_dist.append(int(np.max(dist_map)))
            min_dist.append(int(np.min(dist_map)))
            mean_dist.append(int(np.mean(dist_map)))
            stddev_dist.append(int(np.std(dist_map)))
            unique, counts = np.unique(dist_map, return_counts=True)
            for distance, count in zip(unique, counts):
                if distance not in overall_dist:
                    overall_dist[distance] = 0
                overall_dist[distance] += count
        else:
            max_dist.append(0)
            min_dist.append(0)
            mean_dist.append(0)
            stddev_dist.append(0)
    add_property(g, "max_distance_dist", "vector<int32_t>", max_dist)
    add_property(g, "min_distance_dist", "vector<int32_t>", min_dist)
    add_property(g, "mean_distance_dist", "vector<int32_t>", mean_dist)
    add_property(g, "stddev_distance_dist", "vector<int32_t>", stddev_dist)
    add_property(g, "overall_dist", "python::object", overall_dist)
    g.save(filename)


def basic_statistics(distances, name):
    distances = distances[np.nonzero(distances)]
    mean = np.mean(distances)
    max_deg = np.max(distances)
    min_deg = np.min(distances)
    std_dev = np.std(distances)
    print "{} Mean: {}".format(name, mean)
    print "{} Std.Deviation: {}".format(name, std_dev)
    print "{} Max: {}".format(name, max_deg)
    print "{} Min: {}".format(name, min_deg)


def draw_distribution(distances, name, filename_core):
    slash_index = filename_core.index("/")
    basefilename = filename_core[slash_index+1:]
    basefilename = "outputs/distances/" + basefilename
    unique, counts = np.unique(distances, return_counts=True)
    pdf = counts.astype("double") / distances.size
    cdf = np.cumsum(pdf)

    plt.plot(unique, pdf)
    plt.title(u"Distribuição empírica de distância")
    plt.xlabel(u"Distância")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+name+"-dist.png", bbox_inches='tight')
    plt.clf()

    plt.semilogy(unique, pdf)
    plt.title(u"Distribuição empírica de distância (Escala log em Y)")
    plt.xlabel(u"Distância")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+name+"-dist-logy.png", bbox_inches='tight')
    plt.clf()

    plt.plot(unique, cdf)
    plt.title(u"Distribuição empírica cumulativa de distância")
    plt.xlabel(u"Distância")
    plt.ylabel(u"Fração de vértices")
    plt.savefig(basefilename+"-"+name+"-cumdist.png", bbox_inches='tight')
    plt.clf()

    print "Saved plots for {}".format(name)


def draw_plot(distances, name, filename_core):
    slash_index = filename_core.index("/")
    basefilename = filename_core[slash_index+1:]
    basefilename = "outputs/distances/" + basefilename
    samples = [dist[0] for dist in distances]
    counts = [dist[1] for dist in distances]
    count_sum = sum(counts)
    pdf = [1.0*count/count_sum for count in counts]
    cdf = np.cumsum(pdf)

    plt.plot(samples, pdf)
    plt.title(u"Distribuição empírica de distância")
    plt.xlabel(u"Distância")
    plt.ylabel(u"Fração de caminhos")
    plt.savefig(basefilename+"-"+name+"-dist.png", bbox_inches='tight')
    plt.clf()

    plt.semilogy(samples, pdf)
    plt.title(u"Distribuição empírica de distância (Escala log em Y)")
    plt.xlabel(u"Distância")
    plt.ylabel(u"Fração de caminhos")
    plt.savefig(basefilename+"-"+name+"-dist-logy.png", bbox_inches='tight')
    plt.clf()

    plt.plot(samples, cdf)
    plt.title(u"Distribuição empírica cumulativa de distância")
    plt.xlabel(u"Distância")
    plt.ylabel(u"Fração de caminhos")
    plt.savefig(basefilename+"-"+name+"-cumdist.png", bbox_inches='tight')
    plt.clf()

    print "Saved plots for {}".format(name)

if __name__ == '__main__':

    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-f', help="filename to load from")
    ARGPARSER.add_argument('-d', help="compute distances",
                           default=False, action='store_true')
    ARGS = ARGPARSER.parse_args()

    filename = ARGS.f
    dot_index = filename.index(".")
    filename_core = filename[:dot_index]
    g = load(filename)

    if (ARGS.d):
        compute_and_save_distance_info(g, filename)
        print "DONE!"
    else:
        max_distance_dist = g.gp.max_distance_dist.get_array()
        min_distance_dist = g.gp.min_distance_dist.get_array()
        mean_distance_dist = g.gp.mean_distance_dist.get_array()
        stddev_distance_dist = g.gp.stddev_distance_dist.get_array()
        overall_dist = g.gp.overall_dist

        print "-------------"
        basic_statistics(max_distance_dist, "Max distance")
        print "-------------"
        basic_statistics(min_distance_dist, "Min distance")
        print "-------------"
        basic_statistics(mean_distance_dist, "Mean distance")
        print "-------------"
        draw_distribution(max_distance_dist, "max-distance", filename_core)
        draw_distribution(min_distance_dist, "min-distance", filename_core)
        print "-------------"
        draw_plot(overall_dist.items(), "overall-distance", filename_core)
        print "-------------"
        print "DONE!"
