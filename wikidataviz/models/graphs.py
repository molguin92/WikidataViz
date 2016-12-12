import multiprocessing

import networkx
import rdflib
from networkx import compose
from networkx.readwrite.json_graph import node_link_data
from rdflib import RDF
from rdflib.exceptions import UniquenessError

from wikidataviz.views.gview import wikibase


def get_english_label(rdf_g, subject):
    labels = rdf_g.preferredLabel(subject, lang='en')
    if len(labels) > 0:
        lprop, label = labels[0]
        return str(label)
    else:
        return None


def populate_network_graph(uriref, depth=2):
    """
    This functions populates the network graph for a specific RDF entity in
    a recursive manner.

    :param uriref: The rdf entity which is to be considered as the root for
    this level.
    :param depth: How many recursive steps to perform.
    :return: The networkX graph representing the given entity.
    """

    print('Building subgraph for {}. Depth = {}.'.format(uriref, depth))

    if depth < 1:
        return networkx.Graph()

    g = rdflib.Graph()
    g.load(uriref)

    vg = networkx.Graph()
    vg.add_node(uriref, label=get_english_label(g, uriref))

    for prop, p, o in g.triples((None, RDF.type, wikibase.Property)):
        dclaim = g.value(subject=prop, predicate=wikibase.directClaim)

        try:
            value = g.value(subject=uriref, predicate=dclaim, any=False)
            if not value:
                continue

            if value in g.subjects(RDF.type, wikibase.Item):
                vg.add_node(value, label=get_english_label(g, value))
                vg.add_edge(uriref, value, label=get_english_label(g, prop))

                if depth - 1 > 0:
                    vg2 = populate_network_graph(depth - 1)(value)
                    vg = compose(vg, vg2)

        except UniquenessError:
            for s, p, value in g.triples((uriref, dclaim, None)):

                if value in g.subjects(RDF.type, wikibase.Item):
                    vg.add_node(value, label=get_english_label(g, value))
                    vg.add_edge(uriref, value,
                                label=get_english_label(g, prop))

                    if depth - 1 > 0:
                        vg2 = populate_network_graph(depth - 1)(value)
                        vg = compose(vg, vg2)

    return vg


def parallel_populate_network_graph(uriref, depth=2):
    print('Building relationship graph for {}.'.format(uriref))

    item_l = []

    g = rdflib.Graph()
    g.load(uriref)

    vg = networkx.Graph()
    vg.add_node(uriref)
    if depth < 1:
        return vg

    for prop, p, o in g.triples((None, RDF.type, wikibase.Property)):
        dclaim = g.value(subject=prop, predicate=wikibase.directClaim)

        try:
            value = g.value(subject=uriref, predicate=dclaim,
                            any=False)
            if not value:
                continue

            if value in g.subjects(RDF.type, wikibase.Item):
                vg.add_node(value, label=get_english_label(g, value))
                vg.add_edge(uriref, value, property=prop)

                if depth - 1 > 0:
                    item_l.append((value, depth - 1))

        except UniquenessError:
            for s, p, value in g.triples((uriref, dclaim, None)):

                if value in g.subjects(RDF.type, wikibase.Item):
                    vg.add_node(value, label=get_english_label(g, value))
                    vg.add_edge(uriref, value, property=prop)

                    if depth - 1 > 0:
                        item_l.append((value, depth - 1))

    with multiprocessing.Pool(processes=6) as pool:
        vgraphs = pool.starmap(populate_network_graph, item_l)
        for vg2 in vgraphs:
            vg = compose(vg, vg2)

    vg.add_node(uriref, label=get_english_label(g, uriref), root=True)
    return vg


def deferred_graph_build(uriref):
    return node_link_data(parallel_populate_network_graph(uriref))
