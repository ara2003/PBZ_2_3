from django.shortcuts import render
from .forms import SPARQLRequestForm
from .owl_sparql_util import *

# Create your views here.

def ontology(request):
    classes = getAllClasses()

    subClasses = []
    for i in classes:
        subClasses.append(getSubClasses(i))
    
    superClasses = []
    for i in classes:
        superClasses.append(getSuperClasses(i))

    classes = list(zip(classes, superClasses, subClasses))

    context = {
        'classes': classes,
    }
    return render(request, 'main/ontology.html', {'context': context})


def instances(request):
    instances = getAllInstances()

    context = {
        'instances': instances,
    }
    return render(request, 'main/instances.html', {'context': context})


def objectProperties(request):
    objectProperties = getAllObjectProperty()

    context = {
        'objectProperties': objectProperties,
    }
    return render(request, 'main/objectProperties.html', {'context': context})


def triplesRDF(request):
    triplesRaw = get_all_triple()
    triples = get_dict_triple(triplesRaw)

    context = {
        'triples' : triples,
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

    context = {
        'form': form,
        'result': result,
        'error': error
    }
    return render(request, 'main/sparqlRequests.html', context)