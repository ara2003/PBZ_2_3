from .raw_sparql_util import *


def create_triple(subject, predicate, object):
    return update('INSERT DATA {' + f'{subject.__str__()} {predicate.__str__()} {object.__str__()}' + '}')


def delete_all_triple():
    return update(' DELETE  { ?subject ?predicate ?object } WHERE { ?subject ?predicate ?object}')


def delete_triple(subject, predicate, object):
    return update(' DELETE  {' + f'{subject.__str__()} {predicate.__str__()} {object.__str__()}' + '} WHERE { }')


def get_all_triple():
    return query('SELECT * WHERE { ?subject ?predicate ?object }')


def get_triple(subject, predicate, object) -> ResultSet:
    if subject is None:
        subject = "?subject"
    if predicate is None:
        predicate = "?predicate"
    if object is None:
        object = "?object"
    return query('SELECT * WHERE {' + f'{subject.__str__()} {predicate.__str__()} {object.__str__()}' + '}')


def get_tripleRequest(sparqlRequest):
    return query(sparqlRequest)


def get_dict_triple(triplesRaw):
    triples = []
    for row in triplesRaw.rows():
        triples.append(row)
    return triples