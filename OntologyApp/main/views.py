from django.shortcuts import render

from .forms import SPARQLRequestForm
from .owl_sparql_util import *


# Create your views here.

def ontology(request):
    if request.method == 'POST':

        if 'addClass' in request.POST:
            name = request.POST.get('classInputName')

            classNode = Node(":" + name)
            newClass(classNode)

        if 'addInstance' in request.POST:
            name = request.POST.get('individualInputName')
            cls = request.POST.get('individualInput')

            instNode = Node(":" + name)
            classNode = Node(":" + cls)

            addClass(instNode, classNode)

        if 'addObjectProperty' in request.POST:
            name = request.POST.get('objectPropertyInputName')
            subject = request.POST.get('objectPropertyInputOne')
            object = request.POST.get('objectPropertyInputTwo')

            nameNode = Node(":" + name)
            subjectNode = Node(":" + subject)
            objectNode = Node(":" + object)
            newObjectProperty(nameNode)
            create_triple(subjectNode, nameNode, objectNode)

        if 'Edit' in request.POST:
            editedClass = request.POST.get('Edit')
            classEditOne = request.POST.get('classEditOne')

        if 'addSuperClass' in request.POST:
            editedClass = request.POST.get('addSuperClass')
            classInputOne = request.POST.get('classInputOne')

            editedClassNode = Node(editedClass)
            classInputNode = Node(":" + classInputOne)

            addSuperClass(editedClassNode, classInputNode)

        if 'addSubClass' in request.POST:
            editedClass = request.POST.get('addSubClass')
            classInput = request.POST.get('classInputTwo')

            editedClassNode = Node(editedClass)
            classInputNode = Node(":" + classInput)

            addSuperClass(classInputNode, editedClassNode)

        if 'Delete' in request.POST:
            className = request.POST.get('Delete')

            classNode = Node(className)

            delete(classNode)

    classes = getAllClasses()

    subClasses = []
    for i in classes:
        subClasses.append(getSubClasses(i))

    superClasses = []
    for i in classes:
        superClasses.append(getSuperClasses(i))

    instances = []
    for i in classes:
        instances.append(getInstancesOfClass(i))

    classes = list(zip(classes, superClasses, subClasses, instances))

    context = {
        'classes': classes,
    }
    return render(request, 'main/ontology.html', {'context': context})


def instances(request):
    instances = getAllInstances()

    if request.method == 'POST':

        if 'Edit' in request.POST:
            editedInstance = request.POST.get('Edit')
            newName = request.POST.get('individualEditNewName')
            superClass = request.POST.get('individualEditInput')

        if 'Delete' in request.POST:
            delInstance = request.POST.get('Delete')

    context = {
        'instances': instances,
    }
    return render(request, 'main/instances.html', {'context': context})


def objectProperties(request):
    objectProperties = getAllObjectProperty()

    if request.method == 'POST':

        if 'Edit' in request.POST:
            editedObjectProperty = request.POST.get('Edit')
            newName = request.POST.get('objectPropertyEditNewName')
            subject = request.POST.get('objectPropertyEditOne')
            object = request.POST.get('objectPropertyEditTwo')

        if 'Delete' in request.POST:
            delObjectProperty = request.POST.get('Delete')

    context = {
        'objectProperties': objectProperties,
    }
    return render(request, 'main/objectProperties.html', {'context': context})


def triplesRDF(request):
    if request.method == 'POST':

        if 'Delete' in request.POST:
            delTriples: str = request.POST.get('Delete')

            index1 = delTriples.find(' ')
            index2 = delTriples.find(' ', index1 + 1)

            subjectNode = Node(delTriples[:index1])
            predicateNode = Node(delTriples[index1 + 1:index2])
            objectNode = Node(delTriples[index2 + 1:])

            delete_triple(subjectNode, predicateNode, objectNode)

    triplesRaw = get_all_triple()
    triples = get_dict_triple(triplesRaw)
    context = {
        'triples': triples,
    }
    return render(request, 'main/triplesRDF.html', {'context': context})


def sparqlRequests(request):
    result = ResultSet()
    error = ''

    if request.method == 'POST':
        form = SPARQLRequestForm(request.POST)

        if form.is_valid():
            sparqlRequest = form.data['body']

            if 'SELECT' in sparqlRequest:
                result = query(sparqlRequest)
            elif 'INSERT' in sparqlRequest or 'DELETE' in sparqlRequest:
                update(sparqlRequest)
            else:
                error = 'Incorrect query!'
        else:
            error = 'Incorrect form!'

    form = SPARQLRequestForm()
    context = {
        'form': form,
        'result': result,
        'error': error
    }
    return render(request, 'main/sparqlRequests.html', context)
