
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

    def __repr__(self):
        return f"Node({self.uri})"

class Literal(Resource):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"Literal({self.value})"

class Triple:
    def __init__(self, subject, predicate, object):
        self.subject = subject
        self.predicate = predicate
        self.object = object

    def __repr__(self):
        return f"Triple({self.subject}, {self.predicate}, {self.object})"

def parse_resource(resource):
    type = resource["type"]
    if type == "uri":
        return Node(resource["value"])
    if type == "literal":
        return Literal(resource["value"])
    raise Exception("type: {type}")
        

def query(query: str) -> list[Triple]:
    query = database_prefix + query
    sparql = SPARQLWrapper(database_url)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    result = []
    ret = sparql.query().convert()
    for r in ret["results"]["bindings"]:
        subject = parse_resource(r["subject"])
        predicate = parse_resource(r["predicate"])
        object = parse_resource(r["object"])
        t = Triple(subject, predicate, object)
        result.append(t)
    return result

def update(query: str) -> dict[str, str]:
    query = database_prefix + query
    sparql = SPARQLWrapper(database_url)
    sparql.setReturnFormat(JSON)
    sparql.setMethod(POST)
    sparql.setHTTPAuth(DIGEST)
    sparql.setQuery(query)
    result = sparql.query().convert()
    if result["statusCode"] != 200:
        raise Exception(result["message"])
    return result

tripletes = update("""

INSERT DATA {
    :maks :name "Maksim"
}
""")

print(tripletes)