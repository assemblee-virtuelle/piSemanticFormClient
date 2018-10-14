from rdflib import BNode, ConjunctiveGraph, Graph,  Namespace
from rdflib import Literal, XSD, URIRef
from rdflib.namespace import FOAF, RDF, RDFS
from rdflib.serializer import Serializer
from rdflib import plugin


def pprint(msg):
    msg = msg.decode('utf-8')
    for l in msg.split('\n'):
        if l.strip():
            print(l)

store='Sleepycat'
graph = ConjunctiveGraph(store=store, identifier='mygraph')
graph.open('foaf_flask/static/rdf/sleepycat', create = False)

#CONSTRUCT {{ ?uri  ?p ?o . }}
query = """CONSTRUCT { ?uri ?p ?o . }
WHERE {
    {GRAPH ?g { ?uri ?p ?o } }
    UNION { ?uri ?p ?o }
}"""
# query = """CONSTRUCT { ?uri  ?p ?o . }
# WHERE  { ?uri ?p ?o } """
bind = {'uri': URIRef('http://127.0.0.1:5000/ldp/donna')}
context = dict(graph.namespaces())
query_result = graph.query(query, initBindings=bind, initNs=context)
newg = Graph().parse(data=query_result.serialize(format='xml'))
data = newg.serialize(format='turtle', context=context)
pprint(data)