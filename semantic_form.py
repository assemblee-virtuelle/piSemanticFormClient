"""
    Creative Commons: CC-BY
    Author : swann Bouvier-Muller (swann.bouviermuller[a]gmail.com)
    Publication : 2018-08-16

    This is a library to ease communication with semanticforms access when using python scripts
    The first use is to simplify data loading into the db when deploying SemApps stack
"""
import requests
import json

# TODO add no CredentialException
# TODO use wrong argument exception
# TODO check docstrings compliance
# TODO ajouter une logique de log
# TODO ajouter un fichier de paramétrage

class Client:

    def __init__(self, domaine=None, headers=None, credentials=None, sparql_endpoint='sparql2', max_history=1):
        """
        Create a client capable of communicating with SemanticForm (todo : add github repo url)
        :param domaine: url of the endpoint, example : http://data.assemblee-virtuelle.org:9800/
        :type domaine: string
        :param headers: dict 
        :type headers: string
        """
        # init the http session which will persists cookies and enable authentification
        self.session = None
        self.domaine = domaine
        self.default_credentials = credentials
        self.sparql_endpoint = sparql_endpoint
        self.is_authenticated = False
        self.max_history = max_history # TODO save all result requests into self.request_history = [] until max
        if headers:
            self.default_headers = headers
        else:
            self.default_headers = {
                'user-agent': 'SemanticFormsClient',
                'Accept' : 'application/json',
            }

    @property
    def s(self):
        """
        return the request session object (it's a singleton)
        if session not started yet, start it
        :return: session object
        :return type: requests.Session
        """
        if not self.session:
            self.session = requests.session()
        return self.session

                                                                        ################################
                                                                        #  PRIMITIVES (W3C compliant)  #
                                                                        ################################
    
    def sparql(self, query, mime=None, sparql_endpoint=None):
        """
        Executes a SELECT SPARQL query on sparql2 endpoint.
        Result is returned in json-ld unless indicate otherwise in mime parameter.
        :param query: the sparql query
        :type query: string
        :param mime: (optional) return format, example: 'text/turtle', 'application/json'...
        :type mime: string
        :param sparql_endpoint: (optional) endpoint where the query is sent. By default it's sparql2
        :type sparql_endpoint: string
        :param query: the sparql query
        :type query: string
        :return: response of the request
        :return type: requests.Response
        """
        headers = self.default_headers
        if mime:
            headers['accept']=mime
        payload = {'query' : query }
        endpoint = self.sparql_endpoint 
        if sparql_endpoint:
            endpoint = sparql_endpoint
        url = '{}/{}'.format(self.domaine, endpoint)
        r = self.s.post(url, headers=headers, data=payload)
        return r

    def register(self, credentials=None):
        """
        This function is used, first, to create new online account into semantic form, second, to retrieve the cookie that
        authorise insert/update/delete/drop manipulation (like authenticate)
        It uses the default credentials initialised in the constructor if none are passed
        There is no information returned
        :param credentials: (optional) a dictionnary of three information : userid, password and confirmPassword
        :type credentials: dictionnary
        :return: response of the request
        :return type: requests.Response
        """
        if not credentials:
            credentials = self.default_credentials
        url = '{}/register'.format(self.domaine)
        r = self.s.post(url, headers=self.default_headers, data=credentials)
        return r

    def authenticate(self, credentials=None):
        """
        retrive connection cookie for an existing account, enabling insert / delete manipulationsself.
        No return value
        :param credentials: specific credential with userid / password, if None are passed, use default credentials
        :type credentials: dict of string
        :return: response of the request
        :return type: requests.Response
        """
        if not credentials:
            credentials = self.default_credentials
        url = '{}/authenticate'.format(self.domaine)
        r = self.s.post(url, headers=self.default_headers, data=credentials)
        return r

    def update(self, query):
        """
        Used to send a sparql query to /update endpoint 
        with payload = { 'query' : query' }. 
        Query examples : DROP GRAPH <name>, INSERT DATA { GRAPH <name> ...}
        :param query: the sparql query
        :type query: string
        :return: response of the request
        :return type: requests.Response
        """
        if not query:
            raise Exception('Query argument canot be None')
        payload = {'query' : query }
        url = '{}/update'.format(self.domaine)
        r = self.s.post(url, headers=self.default_headers, data=payload)
        return r

                                                                        ##################################################
                                                                        #   Advanced methods to ease data manipulations  #
                                                                        ##################################################

    def auth(self, credentials=None, register=False):
        """
        Call either authenticate or register primitive, then set the flag is_authenticated to true to avoid doing it again
        :param credentials: specific credential with userid / password, if None are passed, use default credentials
        :type credentials: dict of string
        :return: response of the request
        :return type: requests.Response
        """
        if self.is_authenticated:
            return
        self.is_authenticated = True
        if register:
            return self.authenticate(credentials=credentials)
        else:
            return self.register(credentials=credentials)
    
    def drop(self, graph_name):
        """
        Removes (or deletes) a graph from Semanticforms. First build the sparql request, call auth() method then update() primitive
        :param graph_name: name of the graph to be dropped
        :type graph_name: string
        """
        if not graph_name:
            raise Exception('graph_name argument cannot be None')
        query = "DROP GRAPH <{0}/{1}>".format(self.domaine, graph_name)
        r = self.update(query)
        return r

    def clean_subject(self, subject_name):
        """
        First execute a delete request to remove all triplet where subject parameter is subject or object
        Then if graph naming after subject is empty after delete, drops it
        :param subject_name: name of the subject to be removed from the database
        :type subject_name: string
        """
        # vérifie que l'utilisateur est correctment authentifié sur le endpoint
        self.auth()
        # delete query
        subj_uri = '{}/ldp/{}'.format(self.domaine, subject_name)
        delete_query = """DELETE WHERE {{
            GRAPH ?G1 {{ ?s1 ?p1 <{0}> . }}
            GRAPH ?G2 {{ <{0}> ?p2 ?o2 . }}
        }}""".format(subj_uri)
        self.update(delete_query)
        # check if graph contains data
        graph_name = 'ldp/{}'.format(subject_name)
        graph_uri = '{}/{}'.format(self.domaine, graph_name)
        query2 = "SELECT * WHERE {{ GRAPH <{}> {{ ?s ?p ?o . }} }} LIMIT 5".format(graph_uri)
        r = self.sparql(query2)
        d = json.loads(r.text)
        nb_result = len(d['results']['bindings'])
        if nb_result == 0:
            # graph containes no data then drop it
            self.drop(graph_name)
        return

    def get(self, id):
        """
        Access an URI an retrieve the json content
        :param url: the url (http://...) where the content is stored
        :param type: string
        :return: json content
        :return type: string
        """
        if not id:
            raise Exception('uri argument cannot be None')
        url = '{}/{}'.format(self.domaine, id)
        try:
            r = self.s.get(url, headers=self.default_headers)
            return r.text
        except:
            raise

    def import_csv(self, mapping_file_path, data_file_path):
        pass


