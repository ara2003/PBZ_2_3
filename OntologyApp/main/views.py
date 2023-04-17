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
    variables = ['','','']
    query = []
    error = ''

    if request.method == 'POST':
        form = SPARQLRequestForm(request.POST)

        if form.is_valid():

            sparqlRequest = form.data['body']

            if '*' in sparqlRequest:
                strVariables = sparqlRequest[sparqlRequest.find('{'):].replace('{', '').replace('}', '')
                if ' ' in strVariables:
                    variables = strVariables.replace('?', '').split(' ')
                else:
                    variables = strVariables.split('?')
                    variables.remove('')
            else:
                variablesRaw = sparqlRequest.replace('{', '').replace('}', '').split(' ')
                variablesRaw = list(filter(lambda x: x.startswith('?'), variablesRaw))
                variablesRaw = list(map(lambda x: x.replace('?', ''), variablesRaw))

                variablesRaw = [i for i in variablesRaw if variablesRaw.count(i) != 1]
                
                variables = []
                for i in variablesRaw:
                    if i not in variables:
                        variables.append(i)

            if 'SELECT' in sparqlRequest:
                queryRaw = get_tripleRequest(sparqlRequest)
                query = get_dict_triple(queryRaw)
            elif 'INSERT' in sparqlRequest or 'DELETE' in sparqlRequest:
                update(sparqlRequest)

        else:
            error = 'Incorrect form!'

    form = SPARQLRequestForm()
    context = {
        'form': form,
        'variables': variables,
        'query': query,
        'error': error
    }
    return render(request, 'main/sparqlRequests.html', {'context': context, 'variables': variables, 'query': query})