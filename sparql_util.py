
from raw_sparql_util import *

def create_triple(subject, predicate, object):
    return update('INSERT DATA {' + f'{subject.__str__()} {predicate.__str__()} {object.__str__()}' + '}')

def get_all_triple(subject, predicate, object):
    return query('SELECT * WHERE { ?subject ?predicate ?object }')

m  = Node('http://www.w3.org/2023/03/31-my#maks')
n  = Node('http://www.w3.org/2023/03/31-my#name')
ml = Literal('Maksim')

print(create_triple(m, n, ml))

# update("""

# DELETE  {
#   ?subject ?predicate ?object
# } WHERE {
#   ?subject ?predicate ?object
# }

# """)

result = get_all_triple()

print(result.names())
for row in result.rows():
    print(row)