
from row_sparql_util import *

def create_triple(subject, predicate, object):
    if not Node.isinstance(subject):
        subject
    return update('INSERT DATA {' + f'{subject} {predicate} {object}' + '}')

m  = Node('http://www.w3.org/2023/03/31-my#maks')
n  = Node('http://www.w3.org/2023/03/31-my#name')
ml = Literal('Maksim')

print(create_triple(m, n, ml))