#!/usr/bin/python

from graph_tool.all import *

import argparse


def parse_file(filename, directed):
    with open(filename, 'r') as f:
        first_one = True
        g = Graph()
        for line, content in enumerate(f):
            if line in [0, 1, 3]:
                continue
            elif line == 2:
                sc_index = content.index(":")
                content = content[sc_index+2:]
                sp_index = content.index(" ")
                n = int(content[:sp_index])
                g.add_vertex(n)
                continue
            tab_index = content.index("\t")
            source = int(content[:tab_index])
            if source == 0:
                first_one = False
            content = content[tab_index+1:]
            endl_index = content.index("\r")
            dest = int(content[:endl_index])
            g.add_edge(g.vertex(source-first_one), g.vertex(dest-first_one))
            if not directed:
                source, dest = dest, source
                g.add_edge(g.vertex(source-first_one), g.vertex(dest-first_one))
        print len(list(g.vertices())), "vertices loaded"
        print len(list(g.edges())), "edges loaded"
        dot_index = filename.index(".")
        filename_core = filename[:dot_index]
        new_filename = filename_core + ".gt"
        g.save(new_filename)

if __name__ == '__main__':

    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-f', help="filename to parse")
    ARGPARSER.add_argument('-d', help="directed graph",
                           default=False, action='store_true')
    ARGS = ARGPARSER.parse_args()

    parse_file(ARGS.f, ARGS.d)
