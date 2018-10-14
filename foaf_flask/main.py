from flask import Flask, render_template, request, g
from rdflib import Graph, ConjunctiveGraph, Namespace, URIRef
from rdflib.namespace import FOAF, RDF, RDFS
from rdflib.serializer import Serializer
# requiered to serialize in JSON-LD
from rdflib import plugin

app = Flask(__name__)

def get_graph():
    if 'graph' not in g:
        g.graph = ConjunctiveGraph('Sleepycat', identifier='mygraph')
        g.graph.open('foaf_flask/static/rdf/sleepycat', create = True)
        g.n = Namespace("http://127.0.0.1:5000/ldp/")
        g.graph.bind("", g.n)
    return g.graph

@app.teardown_appcontext
def teardown_db(error):
    graph = g.pop('graph', None)
    if graph is not None:
        graph.close()

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route('/sparql', methods=['POST', 'GET'])
def sparql():
    graph = get_graph()
    if request.method == 'POST':
        query = request.form['query']
        query_result = graph.query(query)
        reponse = app.response_class(
            response=query_result.serialize(format='json'),
            status=200,
            mimetype='application/json', 
        )
    else:
        reponse = test_sparql()
    return reponse

@app.route('/test_sparql')
def test_sparql():
    return render_template("test_sparql.html")

@app.route('/ldp/<path:subpath>')
def ldp(subpath):
    graph = get_graph()
    # inc_reverse = request.args.get('inc_reverse', default=False, type=bool)
    query = """CONSTRUCT { ?uri ?p ?o . }
                WHERE {
                    {GRAPH ?g { ?uri ?p ?o } }
                    UNION { ?uri ?p ?o } }"""
    bind = {'uri': URIRef(request.base_url)}
    context = dict(graph.namespaces())
    query_result = graph.query(query, initBindings=bind, initNs=context)
    to_parse = query_result.serialize(format='xml')
    new_graph = Graph().parse(data=to_parse)
    data = new_graph.serialize(format='json-ld', context=context)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/ld+json'
    )
    return response


@app.route('/connect', methods=['POST'])
def connect():
    if request.method == 'POST':
        login = request.form['username']
        pw = request.form['password']
    else:
        pass

@app.route('/admin/see_all/<int:max>')
def see_all(max):
    graph = get_graph()
    query = """CONSTRUCT {{ ?s ?p ?o . }} 
                WHERE
                {{
                    {{ GRAPH ?g {{ ?s  ?p ?o . }} }} 
                    UNION {{ ?s  ?p ?o . }} 
                }}
                LIMIT {max}
            """.format(max=max)
    query_result = graph.query(query)
    context = dict(graph.namespaces())
    data = query_result.serialize(format='json-ld', context=context)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/ld+json'
    )
    return response
