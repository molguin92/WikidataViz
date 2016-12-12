from flask import json
from unittest import TestCase

import time
from networkx.readwrite.json_graph import node_link_graph

from wikidataviz import app

q1 = """
{
"directed": false,
"graph": {
"name": "compose( ,  )"
},
"links": [
{
"label": "has part",
"source": 25,
"target": 23
},
{
"label": "part of",
"source": 26,
"target": 2
},
{
"label": "topic's main category",
"source": 16,
"target": 29
},
{
"label": "facet of",
"property": "http://www.wikidata.org/entity/P1419",
"source": 16,
"target": 17
},
{
"label": "instance of",
"source": 16,
"target": 46
},
{
"label": "subclass of",
"source": 16,
"target": 35
},
{
"label": "field of work",
"source": 27,
"target": 49
},
{
"label": "topic's main category",
"source": 28,
"target": 1
},
{
"label": "opposite of",
"source": 41,
"target": 33
},
{
"label": "topic's main category",
"source": 31,
"target": 13
},
{
"label": "instance of",
"source": 32,
"target": 1
},
{
"label": "discoverer or inventor",
"source": 2,
"target": 22
},
{
"label": "topic's main category",
"source": 2,
"target": 20
},
{
"label": "instance of",
"source": 2,
"target": 36
},
{
"label": "instance of",
"source": 2,
"target": 37
},
{
"property": "http://www.wikidata.org/entity/P793",
"source": 2,
"target": 17
},
{
"label": "has part",
"source": 3,
"target": 23
},
{
"label": "described by source",
"source": 30,
"target": 23
},
{
"label": "described by source",
"source": 30,
"target": 21
},
{
"label": "part of",
"source": 33,
"target": 12
},
{
"label": "discoverer or inventor",
"source": 33,
"target": 4
},
{
"label": "instance of",
"source": 33,
"target": 37
},
{
"label": "topic's main category",
"source": 33,
"target": 43
},
{
"label": "cause of",
"property": "http://www.wikidata.org/entity/P793",
"source": 33,
"target": 17
},
{
"label": "instance of",
"source": 34,
"target": 54
},
{
"label": "category's main topic",
"property": "http://www.wikidata.org/entity/P910",
"source": 34,
"target": 17
},
{
"label": "subclass of",
"source": 5,
"target": 51
},
{
"label": "has part",
"source": 0,
"target": 49
},
{
"label": "topic's main category",
"source": 7,
"target": 8
},
{
"label": "part of",
"source": 8,
"target": 18
},
{
"label": "topic's main template",
"source": 8,
"target": 45
},
{
"label": "instance of",
"source": 8,
"target": 53
},
{
"property": "http://www.wikidata.org/entity/P2670",
"source": 8,
"target": 17
},
{
"label": "described by source",
"source": 8,
"target": 11
},
{
"label": "subclass of",
"source": 8,
"target": 52
},
{
"property": "http://www.wikidata.org/entity/P793",
"source": 9,
"target": 17
},
{
"label": "topic's main category",
"source": 10,
"target": 21
},
{
"label": "instance of",
"source": 37,
"target": 14
},
{
"label": "instance of",
"source": 37,
"target": 51
},
{
"label": "described by source",
"source": 11,
"target": 13
},
{
"label": "part of",
"source": 38,
"target": 51
},
{
"label": "instance of",
"source": 39,
"target": 40
},
{
"label": "part of",
"property": "http://www.wikidata.org/entity/P527",
"source": 17,
"target": 23
},
{
"label": "part of",
"property": "http://www.wikidata.org/entity/P31",
"source": 17,
"target": 49
},
{
"property": "http://www.wikidata.org/entity/P793",
"source": 17,
"target": 19
},
{
"property": "http://www.wikidata.org/entity/P793",
"source": 17,
"target": 6
},
{
"property": "http://www.wikidata.org/entity/P2670",
"source": 17,
"target": 13
},
{
"property": "http://www.wikidata.org/entity/P1552",
"source": 17,
"target": 21
},
{
"property": "http://www.wikidata.org/entity/P793",
"source": 17,
"target": 14
},
{
"property": "http://www.wikidata.org/entity/P793",
"source": 17,
"target": 51
},
{
"label": "facet of",
"property": "http://www.wikidata.org/entity/P2184",
"source": 17,
"target": 1
},
{
"label": "permanent duplicated item",
"property": "http://www.wikidata.org/entity/P2959",
"source": 17,
"target": 40
},
{
"label": "instance of",
"source": 47,
"target": 1
},
{
"label": "has part",
"source": 42,
"target": 23
},
{
"label": "instance of",
"source": 13,
"target": 53
},
{
"label": "part of",
"source": 13,
"target": 50
},
{
"label": "subclass of",
"source": 13,
"target": 24
},
{
"label": "part of",
"source": 14,
"target": 51
},
{
"label": "subclass of",
"source": 15,
"target": 49
},
{
"label": "instance of",
"source": 44,
"target": 21
},
{
"label": "topic's main category",
"source": 48,
"target": 49
}
],
"multigraph": false,
"nodes": [
{
"id": "http://www.wikidata.org/entity/Q223557",
"label": "physical object"
},
{
"id": "http://www.wikidata.org/entity/Q136407",
"label": "chronology of the universe"
},
{
"id": "http://www.wikidata.org/entity/Q273508",
"label": "inflation"
},
{
"id": "http://www.wikidata.org/entity/Q35758",
"label": "matter"
},
{
"id": "http://www.wikidata.org/entity/Q12998",
"label": "Georges Lema\u00eetre"
},
{
"id": "http://www.wikidata.org/entity/Q471702",
"label": "nucleosynthesis"
},
{
"id": "http://www.wikidata.org/entity/Q1079826",
"label": "Lepton epoch"
},
{
"id": "http://www.wikidata.org/entity/Q7037",
"label": "Category:Stars"
},
{
"id": "http://www.wikidata.org/entity/Q523",
"label": "star"
},
{
"id": "http://www.wikidata.org/entity/Q1208634",
"label": "Quark epoch"
},
{
"id": "http://www.wikidata.org/entity/Q6429350",
"label": "Category:Gravitation"
},
{
"id": "http://www.wikidata.org/entity/Q2041543",
"label": "Otto's encyclopedia"
},
{
"id": "http://www.wikidata.org/entity/Q11452",
"label": "general relativity"
},
{
"id": "http://www.wikidata.org/entity/Q634",
"label": "planet"
},
{
"id": "http://www.wikidata.org/entity/Q3491753",
"label": "Hadron epoch"
},
{
"id": "http://www.wikidata.org/entity/Q58778",
"label": "system"
},
{
"id": "http://www.wikidata.org/entity/Q1647152",
"label": "shape of the universe"
},
{
"id": "http://www.wikidata.org/entity/Q1",
"label": "universe",
"root": true
},
{
"id": "http://www.wikidata.org/entity/Q595871",
"label": "star system"
},
{
"id": "http://www.wikidata.org/entity/Q1079806",
"label": "Photon epoch"
},
{
"id": "http://www.wikidata.org/entity/Q8419869",
"label": "Category:Inflation (cosmology)"
},
{
"id": "http://www.wikidata.org/entity/Q11412",
"label": "gravity"
},
{
"id": "http://www.wikidata.org/entity/Q323316",
"label": "Alan Guth"
},
{
"id": "http://www.wikidata.org/entity/Q221392",
"label": "observable universe"
},
{
"id": "http://www.wikidata.org/entity/Q400144",
"label": "planemo"
},
{
"id": "http://www.wikidata.org/entity/Q79925",
"label": "dark matter"
},
{
"id": "http://www.wikidata.org/entity/Q1129469",
"label": "Metric expansion of space"
},
{
"id": "http://www.wikidata.org/entity/Q413",
"label": "physics"
},
{
"id": "http://www.wikidata.org/entity/Q9440523",
"label": "Category:Chronology of the universe"
},
{
"id": "http://www.wikidata.org/entity/Q19796660",
"label": null
},
{
"id": "http://www.wikidata.org/entity/Q2657718",
"label": "Armenian Soviet Encyclopedia"
},
{
"id": "http://www.wikidata.org/entity/Q2944685",
"label": "Category:Planets"
},
{
"id": "http://www.wikidata.org/entity/Q130788",
"label": "chronology"
},
{
"id": "http://www.wikidata.org/entity/Q323",
"label": "Big Bang"
},
{
"id": "http://www.wikidata.org/entity/Q5551050",
"label": "Category:Physical universe"
},
{
"id": "http://www.wikidata.org/entity/Q12149837",
"label": "physical model"
},
{
"id": "http://www.wikidata.org/entity/Q17737",
"label": "theory"
},
{
"id": "http://www.wikidata.org/entity/Q1190554",
"label": "event"
},
{
"id": "http://www.wikidata.org/entity/Q18346",
"label": "physical cosmology"
},
{
"id": "http://www.wikidata.org/entity/Q21286738",
"label": "Wikimedia permanent duplicated page"
},
{
"id": "http://www.wikidata.org/entity/Q22924128",
"label": null
},
{
"id": "http://www.wikidata.org/entity/Q272612",
"label": "Steady State theory"
},
{
"id": "http://www.wikidata.org/entity/Q18343",
"label": "dark energy"
},
{
"id": "http://www.wikidata.org/entity/Q6398965",
"label": "Category:Big Bang"
},
{
"id": "http://www.wikidata.org/entity/Q104934",
"label": "fundamental interaction"
},
{
"id": "http://www.wikidata.org/entity/Q6259679",
"label": "Template:Infobox star"
},
{
"id": "http://www.wikidata.org/entity/Q207961",
"label": "shape"
},
{
"id": "http://www.wikidata.org/entity/Q193946",
"label": "scientific model"
},
{
"id": "http://www.wikidata.org/entity/Q9239363",
"label": "Category:Physical systems"
},
{
"id": "http://www.wikidata.org/entity/Q1454986",
"label": "physical system"
},
{
"id": "http://www.wikidata.org/entity/Q206717",
"label": "planetary system"
},
{
"id": "http://www.wikidata.org/entity/Q837317",
"label": "Big Bang nucleosynthesis"
},
{
"id": "http://www.wikidata.org/entity/Q6999",
"label": "astronomical object"
},
{
"id": "http://www.wikidata.org/entity/Q17444909",
"label": "astronomical object type"
},
{
"id": "http://www.wikidata.org/entity/Q4167836",
"label": "Wikimedia category"
}
]
}
"""


class BaseTest(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()


class ServiceTest(BaseTest):
    def setUp(self):
        super(ServiceTest, self).setUp()
        self.lookup_uri = '/entity?id=Q1'
        self.job_uri = '/job?id='
        json_data = json.loads(q1)
        self.graph = node_link_graph(json_data)
        self.nodes = set(self.graph.nodes())
        self.edges = set(self.graph.edges())

    def test_complete(self):
        rv = self.client.get(self.lookup_uri)
        assert rv
        assert rv.data

        job_info = json.loads(rv.data)
        assert job_info

        job_id = job_info.get('job')
        assert job_id

        graph_data = None

        while True:

            rv = self.client.get(self.job_uri + job_id)
            assert rv
            assert rv.data

            jdata = json.loads(rv.data)
            assert jdata
            self.assertFalse(jdata.get('error'))

            if not jdata.get('done'):
                time.sleep(1)
                continue

            graph_data = jdata.get('result')
            break

        assert graph_data

        graph_model = node_link_graph(graph_data)
        nodes = set(graph_model.nodes())
        edges = set(graph_model.edges())

        self.assertNotEqual(nodes, set())
        self.assertNotEqual(edges, set())

        #self.assertEqual(self.nodes.difference(nodes), set())
        #self.assertEqual(self.edges.difference(edges), set())
