#!/usr/bin/python

from graph_tool.all import *

import argparse


def parse_file(filename_names, filename_links, filename_target, directed):
    names = {}
    with open(filename_names, 'r') as fn:
        for line, content in enumerate(fn):
            if line < 12:
                continue
            endl_index = content.index("\n")
            name = content[:endl_index]
            names[name] = line-12

    with open(filename_links, 'r') as fl:
        g = Graph()
        g.add_vertex(len(names.keys()))
        for line, content in enumerate(fl):
            if line < 12:
                continue
            tab_index = content.index("\t")
            source = names[content[:tab_index]]
            content = content[tab_index+1:]
            endl_index = content.index("\n")
            dest = names[content[:endl_index]]
            g.add_edge(g.vertex(source), g.vertex(dest))
            if not directed:
                source, dest = dest, source
                g.add_edge(g.vertex(source), g.vertex(dest))
        print len(list(g.vertices())), "vertices loaded"
        print len(list(g.edges())), "edges loaded"
        g.save(filename_target)

if __name__ == '__main__':

    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-fn', help="filename with names to parse")
    ARGPARSER.add_argument('-fl', help="filename with links to parse")
    ARGPARSER.add_argument('-ft', help="filename to save to")
    ARGPARSER.add_argument('-d', help="directed graph",
                           default=False, action='store_true')
    ARGS = ARGPARSER.parse_args()

    parse_file(ARGS.fn, ARGS.fl, ARGS.ft, ARGS.d)
