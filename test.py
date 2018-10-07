from re import split

from rdflib import BNode, ConjunctiveGraph, Graph, Literal, Namespace, XSD, BNode, RDF
from rdflib.namespace import FOAF
from rdflib.serializer import Serializer


graph = ConjunctiveGraph('Sleepycat', identifier='mygraph')

graph.open('foaf_flask/static/rdf/sleepycat', create = False)

n = Namespace("http://127.0.0.1:5000/ldp")

graph.bind('foaf', FOAF)
graph.bind('local', n)

graph.add( (n.bob, RDF.type, FOAF.Person) )
graph.set( (n.bob, FOAF.age, XSD.int(42)) )

query = """ SELECT * WHERE { ?s ?p ?o } """
query_result = graph.query(query)



graph.close()