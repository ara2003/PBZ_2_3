
from SPARQLWrapper import *

sparql = SPARQLWrapper("http://localhost:3030/test")
sparql.setMethod(POST)
sparql.setHTTPAuth(DIGEST)

sparql.setReturnFormat(JSON)


sparql.setQuery(""" 
SELECT * WHERE {
  ?subject ?predicate ?object
}
""")

try:
    ret = sparql.query().convert()

    for r in ret["results"]["bindings"]:
        print(r)
except Exception as e:
    print(e)