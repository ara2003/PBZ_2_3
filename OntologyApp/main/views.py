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
    
    if request.method == 'POST':

        if 'addClass' in request.POST:
            name = request.POST.get('classInputName')
            superClass = request.POST.get('classInputOne')
            subClass = request.POST.get('classInputTwo')
        
        if 'addInstance' in request.POST:
            name = request.POST.get('individualInputName')
            superClass = request.POST.get('individualInput')

        if 'addObjectProperty' in request.POST:
            name = request.POST.get('objectPropertyInputName')
            subject = request.POST.get('objectPropertyInputOne')
            object = request.POST.get('objectPropertyInputTwo')

        if 'Edit' in request.POST:
            editedClass = request.POST.get('Edit')
            newName = request.POST.get('classEditOne')
            subClass = request.POST.get('classEditTwo')
        
        if 'Delete' in request.POST:
            delClass = request.POST.get('Delete')


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
    triplesRaw = get_all_triple()
    triples = get_dict_triple(triplesRaw)

    if request.method == 'POST':
        
        if 'Delete' in request.POST:
            delTriples = request.POST.get('Delete')

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

    form = SPARQLRequestForm()
    context = {
        'form': form,
        'result': result,
        'error': error
    }
    return render(request, 'main/sparqlRequests.html', context)