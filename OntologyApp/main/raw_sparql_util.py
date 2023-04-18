from SPARQLWrapper import *


database_url="http://localhost:3030/test"
database_prefix ="""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.w3.org/2023/03/31-my#>
"""

class Resource:
    pass

class Node(Resource):
    def __init__(self, uri: str):
        self.uri = uri

    def __str__(self):
        return f"{self.uri}"

    def __repr__(self):
        return f"Node({self.uri})"

class Literal(Resource):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f'"{self.value}"'
    
    def __repr__(self):
        return f"Literal({self.value})"

class Triple:
    def __init__(self, subject, predicate, object):
        self.subject = subject
        self.predicate = predicate
        self.object = object

    def __repr__(self):
        return f"Triple({self.subject}, {self.predicate}, {self.object})"

class ResultSet:
    def __init__(self, json_result) -> None:
        self.json_result = json_result
    
    def names(self):
        return self.json_result['head']['vars']

    def rows(self):
        return list(map(parse_result_row, self.json_result['results']['bindings']))

def parse_resource(resource):
    type = resource["type"]
    if type == "uri":
        return Node('<'+resource["value"]+'>')
    if type == "literal":
        return Literal(resource["value"])
    if type == "bnode":
        return Node(resource["value"])
    raise Exception(f"type: {resource}")
        
def parse_result_row(row: dict):
    result = {}
    for n in row.keys():
        result[n] = parse_resource(row[n])
    return result

def query(query: str) -> ResultSet:
    query = database_prefix + query
    sparql = SPARQLWrapper(database_url)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    ret = sparql.query().convert()
    result = ResultSet(ret)
    return result

def update(query: str) -> dict[str, str]:
    query = database_prefix + query
    sparql = SPARQLWrapper(database_url)
    sparql.setReturnFormat(JSON)
    sparql.setMethod(POST)
    sparql.setHTTPAuth(DIGEST)
    sparql.setQuery(query)
    query = sparql.query()
    result = query.convert()
    if result["statusCode"] != 200:
        raise Exception(result["message"])
    return result