from flask import json
from unittest import TestCase

import time
from networkx.readwrite.json_graph import node_link_graph

from wikidataviz import app


class BaseTest(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()


class ServiceTest(BaseTest):

    def setUp(self):
        super(ServiceTest, self).setUp()
        self.lookup_uri = '/entity?id=Q1'
        self.job_uri = '/job?id='

        with open('./q1.json', 'r') as json_f:
            json_data = json.loads(json_f.read())
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

        self.assertEqual(self.nodes.difference(nodes), set())
        self.assertEqual(self.edges.difference(edges), set())

