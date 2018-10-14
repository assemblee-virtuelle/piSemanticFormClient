from rdflib import BNode, ConjunctiveGraph, Graph,  Namespace
from rdflib import Literal, XSD, URIRef
from rdflib.namespace import FOAF, RDF, RDFS
from rdflib.serializer import Serializer


store='Sleepycat'
graph = ConjunctiveGraph(store=store, identifier='mygraph')
graph.open('foaf_flask/static/rdf/sleepycat', create = False)

n = Namespace("http://127.0.0.1:5000/ldp/")

graph.bind('foaf', FOAF)
graph.bind('local', n)

graph.add( (n.bob, RDF.type, FOAF.Person) )
graph.add( (n.bob, FOAF.age, Literal('42', datatype=XSD.integer)) )

g = graph.get_context(identifier=n.linda)
g.add( (n.linda, RDF.type,      FOAF.Person) )
g.add( (n.bob,   FOAF.knows,    n.donna) )
g.add( (n.donna, FOAF.name,     Literal("Donna Fales")) )
g.add( (n.donna, FOAF.firstName,Literal("Donna")) )
g.add( (n.donna, FOAF.lastName, Literal("Fales")) )
g.add( (n.bob,   FOAF.age,      Literal('42', datatype=XSD.integer)) )
g.add( (n.bob,   RDFS.label,    Literal('Bob',    lang='en') ) )
g.add( (n.bob,   RDFS.label,    Literal('Robert', lang='fr') ) )
g.add( (n.donna, FOAF.nick,     Literal("Doudie", lang="en")) )
g.add( (n.donna, FOAF.nick,     Literal("Dudu", lang="es")) )
g.add( (n.donna, FOAF.mbox,     URIRef("mailto:donna@example.org")) )
g.add( (n.bob,   FOAF.name,     Literal('Bob')) )
g.add( (n.linda, FOAF.name,     Literal('Linda') ) )
g.add( (n.bob,   FOAF.knows,    n.linda) )

query = """ SELECT * WHERE { ?s ?p ?o } """
query_result = graph.query(query)
print(query_result)#.serialize(format='n3').decode('utf-8'))

graph.close()