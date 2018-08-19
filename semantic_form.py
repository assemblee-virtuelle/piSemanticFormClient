"""
    Creative Commons: CC-BY
    Author : swann Bouvier-Muller (swann.bouviermuller[a]gmail.com)
    Publication : 2018-08-16

    This is a library to ease communication with semanticforms access when using python scripts
    The first use is to simplify data loading into the db when deploying SemApps stack
"""
import requests

# TODO add no CredentialException
# TODO use wrong argument exception
# TODO check docstrings compliance

class Client:

    def __init__(self, domaine=None, headers=None, credentials=None, sparql_endpoint='sparql2'):
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

    def update(self, item_id, insert_query):
        """
        Used to mimic a classical SQL UPDATE by deleting the item then inserting new data
        :param insert_query: the sparql INSERT query
        :type insert_query: string
        :param item_id: the item_id to drop (usually the same as the one you will insert)
        :type item_id: string
        :return: last http response
        :return type: requests.Response
        """
        if not insert_query or not item_id:
            raise Exception('Item_id and insert_query arguments canot be None')
        self.drop(item_id)
        r = self.insert(insert_query)
        return r
    
    def insert(self, query):
        """
        Used to send a sparql INSERT query to the LDP
        Make an HTTP post to /update endpoint with payload = { 'query' : 'INSERT DATA ...' }
        :param query: the sparql INSERT query.
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


    def authenticate(self, credentials):
        """
        retrive connection cookie for an existing account, enabling insert / delete manipulationsself.
        No return value
        :param credentials: specific credential with userid / password, if None are passed, use default credentials
        :type credentials: dict of string
        """
        if not credentials:
            credentials = self.default_credentials
        url = '{}/authenticate'.format(self.domaine)
        r = self.s.post(url, headers=self.default_headers, data=credentials)
        return r

    def register(self, credentials=None):
        """
        This function is used, first, to create new online account into semantic form, second, to retrieve the cookie that
        authorise insert/update/delete manipulation (like authenticate)
        It uses the default credentials initialise in the constructor if none are passed
        There is no information returned

        :param credentials: a dictionnary of three information : userid, password and confirmPassword. Can be None.
        :type credentials: dictionnary
        """
        if not credentials:
            credentials = self.default_credentials
        url = '{}/register'.format(self.domaine)
        r = self.s.post(url, headers=self.default_headers, data=credentials)
        return r

    def drop(self, id):
        """
        Removes (or deletes) a graph from Semanticforms
        :param id: id of the graph to be removed
        :type id: string
        """
        if not id:
            raise Exception('id argument cannot be None')
        url = '{}/update'.format(self.domaine)
        query = "DROP GRAPH <{0}/ldp/{1}>".format(self.domaine, id)
        payload = {'query' : query }
        r = self.s.post(url, headers=self.default_headers, data=payload)
        return r

    def sparql(self, query, mime=None):
        """
        Executes a SPARQL query and return result. Result is returned in json-ld unless indicate otherwise in mime parametersself.
        Accepted mime parameter values : 'text/turtle', 'application/json'
        """
        headers = self.default_headers
        if mime:
            headers['accept']=mime
        payload = {'query' : query }
        url = '{}/{}'.format(self.domaine, self.sparql_endpoint)
        r = self.s.post(url, headers=headers, data=payload)
        return r

    def import_csv(self, mapping_file_path, data_file_path):
        pass


