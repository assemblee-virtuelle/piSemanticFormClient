from flask import Flask, render_template, request
from rdflib import Graph, ConjunctiveGraph
from rdflib.namespace import FOAF
from rdflib.serializer import Serializer

app = Flask(__name__)

graph = ConjunctiveGraph('Sleepycat', identifier='mygraph')
graph.open('foaf_flask/static/rdf/sleepycat', create = True)

@app.teardown_appcontext
def close_db(error):
    """Closes the graph"""
    #graph.close()
    pass

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route('/sparql', methods=['POST'])
def sparql():
    query = request.form['query']
    query_result = graph.query(query)
    return app.response_class(
        response=query_result.serialize(format='json'),
        status=200,
        mimetype='application/json', 
    )

@app.route('/test_sparql')
def test_sparql():
    return render_template("test_sparql.html")

@app.route('/ldp')
def ldp():
    context = {"foaf": "http://xmlns.com/foaf/0.1/", }
    query = """
        SELECT * WHERE 
        {
            BIND (<{domain}/{id}> as ?B )
            GRAPH ?g1 { ?B  ?p1 ?o1 . }
            GRAPH ?g2 { ?s2 ?p2 ?B . }

        }
        """.format(domain='http://127.0.0.1:5000/', id='test')

    
    
    data = query_result.serialize(format='json')
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response