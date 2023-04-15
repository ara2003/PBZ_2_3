
from sparql_util import *

from functools import *

rdfType = Node("rdf:type")
owlClass = Node("owl:Class")
rdfsSubClassOf = Node("rdfs:subClassOf")
owlObjectProperty = Node("owl:ObjectProperty")

def getAllClasses():
    return list(map(lambda x: x["subject"], get_triple(None, rdfType, owlClass).rows()))

def newClass(cls):
    return create_triple(cls, rdfType, owlClass)

def getClasses(object):
    return list(map(lambda x: x["object"], get_triple(object, rdfType, None).rows()))

def getSubClasses(cls):
    return list(map(lambda x: x["object"], get_triple(cls, rdfsSubClassOf, None).rows()))

def getSuperClasses(cls):
    return list(map(lambda x: x["subject"], get_triple(None, rdfsSubClassOf, cls).rows()))

def addClass(object, cls):
    newClass(cls)
    return create_triple(object, rdfType, cls)

def addSuperClass(cls, superClass):
    newClass(cls)
    newClass(superClass)
    return create_triple(cls, rdfsSubClassOf, superClass)


def getAllObjectProperty():
    return list(map(lambda x: x["subject"], get_triple(None, rdfType, owlObjectProperty).rows()))

def newObjectProperty(cls):
    return create_triple(cls, rdfType, owlObjectProperty)

def createObjectProperty(subject, property, object):
    newObjectProperty(property)
    return create_triple(subject, property, object)

def getObjectOfProperty(subject, property):
    newObjectProperty(property)
    return list(map(lambda x: x["object"], get_triple(subject, property, None).rows()))

def getSubjectOfProperty(object, property):
    newObjectProperty(property)
    return list(map(lambda x: x["subject"], get_triple(None, property, object).rows()))

classA = Node(":classA")
classB = Node(":classB")

obj = Node(":obj")

delete_all_triple()

addSuperClass(classA, classB)

print(getSubClasses(classB))
print(getSubClasses(classA))
print(getSuperClasses(classB))
print(getSuperClasses(classA))

res = get_all_triple()
print(res.names())
for row in res.rows():
    print(row)
