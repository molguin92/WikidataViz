import threading
import multiprocessing

import networkx
import rdflib
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from networkx.readwrite.json_graph import node_link_data
from networkx import set_node_attributes, compose
from rdflib import Namespace, RDF
from rdflib.exceptions import UniquenessError
import requests

wikibase = Namespace('http://wikiba.se/ontology-beta#')
wd = Namespace('http://www.wikidata.org/entity/')
schema = Namespace('http://schema.org/')
wdata = Namespace('https://www.wikidata.org/wiki/Special:EntityData/')


def extract_literal_value(node):
    t, l = node
    return l.value


def populate_network_graph(uriref, depth=2):
    """
    This functions populates the network graph for a specific RDF entity in
    a recursive manner.

    :param uriref: The rdf entity which is to be considered as the root for
    this level.
    :param depth: How many recursive steps to perform.
    :return: The networkX graph representing the given entity.
    """

    vg = networkx.Graph()
    vg.add_node(uriref)

    if depth < 1:
        return vg

    g = rdflib.Graph()
    g.load(uriref)

    for prop, p, o in g.triples((None, RDF.type, wikibase.Property)):
        dclaim = g.value(subject=prop, predicate=wikibase.directClaim)

        try:
            value = g.value(subject=uriref, predicate=dclaim, any=False)
            if not value:
                continue

            if value in g.subjects(RDF.type, wikibase.Item):
                vg.add_node(value)
                vg.add_edge(uriref, value)

                if depth - 1 > 0:
                    vg2 = populate_network_graph(depth - 1)(value)
                    vg = compose(vg, vg2)

        except UniquenessError:
            for s, p, value in g.triples((uriref, dclaim, None)):

                if value in g.subjects(RDF.type, wikibase.Item):
                    vg.add_node(value)
                    vg.add_edge(uriref, value)

                    if depth - 1 > 0:
                        vg2 = populate_network_graph(depth - 1)(value)
                        vg = compose(vg, vg2)

    return vg


def paralellized_populate_network_graph(uriref, depth=2):
    vg = networkx.Graph()
    vg.add_node(uriref)

    if depth < 1:
        return vg

    item_l = []

    g = rdflib.Graph()
    g.load(uriref)

    for prop, p, o in g.triples((None, RDF.type, wikibase.Property)):
        dclaim = g.value(subject=prop, predicate=wikibase.directClaim)

        try:
            value = g.value(subject=uriref, predicate=dclaim,
                            any=False)
            if not value:
                continue

            if value in g.subjects(RDF.type, wikibase.Item):
                vg.add_node(value)
                vg.add_edge(uriref, value)

                if depth - 1 > 0:
                    item_l.append((value, depth - 1))

        except UniquenessError:
            for s, p, value in g.triples((uriref, dclaim, None)):

                if value in g.subjects(RDF.type, wikibase.Item):
                    vg.add_node(value)
                    vg.add_edge(uriref, value)

                    if depth - 1 > 0:
                        item_l.append((value, depth - 1))

    with multiprocessing.Pool(processes=4) as pool:
        vgraphs = pool.starmap(populate_network_graph, item_l)
        for vg2 in vgraphs:
            vg = compose(vg, vg2)

    return vg


def get_label(node):
    q_id = node.split('/')[-1]
    rv = requests.get(node, headers={'Accept': 'application/json'})
    info = rv.json()
    label = info.get('entities', {}) \
        .get(q_id, {}).get('labels', {}) \
        .get('en', {}).get('value', None)

    return label


def get_node_labels(vgraph):
    nodes = vgraph.nodes()
    with multiprocessing.Pool(processes=4) as pool:
        labels = pool.map(get_label, nodes)
        nodes_labels = dict(zip(nodes, labels))
        set_node_attributes(vgraph, 'label', nodes_labels)


class GraphView(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('id', type=str, required=True)
        self.lock = threading.RLock()

    def get(self):
        args = self.parser.parse_args()
        id = args['id']

        vgraph = paralellized_populate_network_graph(wd[id])
        get_node_labels(vgraph)

        return node_link_data(vgraph)
