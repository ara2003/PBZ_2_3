
from raw_sparql_util import *

def create_triple(subject, predicate, object):
    return 'INSERT DATA {' + f'{subject.__str__()} {predicate.__str__()} {object.__str__()}' + '}'

m  = Node('http://www.w3.org/2023/03/31-my#maks')
n  = Node('http://www.w3.org/2023/03/31-my#name')
ml = Literal('Maksim')

print(create_triple(m, n, ml))