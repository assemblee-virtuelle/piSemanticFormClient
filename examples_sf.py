import semantic_form

### example 1 :
# retrieve data from a semanticform graph and instance a rdflibGraph with it
import rdflib
import json, rdflib_jsonld
# prerequisite to use JSON-LD when building a rdflib.Graph
rdflib.plugin.register('json-ld', rdflib.plugin.Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')

sfc = semantic_form.Client(domaine='http://locahost:9111')
serialized_rdf = sfc.get('1234567890-1234567890')
g = rdflib.Graph()
g.parse(data=serialized_rdf, format='json-ld')
#display graph
for s, p, o in g:
    print('subject={}, predicate={}, object={}'.format(s,p,o))

## example 2
# insert an organization into the semanticform
sfc = semantic_form.Client(domaine='http://locahost:9111')
query_format = """
    INSERT DATA {{
        GRAPH <{2}/ldp/{0}>
        {{
            <{2}/ldp/{0}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://virtual-assembly.org/pair#Organization> .
            <{2}/ldp/{0}> <http://virtual-assembly.org/pair#preferedLabel> "{1}" .
        }}
    }}
"""
query = query_format.format('1234567890-1234567890', 'Assemblée virtuelle', 'http://localhost:9111')
sfc.register()
sfc.update(query)

## example 3 
# remove a graph
sfc = semantic_form.Client(domaine='http://locahost:9111')
sfc.register()
sfc.update('1234567890-1234567890')