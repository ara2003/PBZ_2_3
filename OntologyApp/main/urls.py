from django.urls import path
from . import views

urlpatterns = [
    path('', views.ontology, name = 'ontology'),
    path('instances', views.instances, name = 'instances'),
    path('objectProperties', views.objectProperties, name = 'objectProperties'),
    path('triplesRDF', views.triplesRDF, name = 'triplesRDF'),
    path('sparqlRequests', views.sparqlRequests, name = 'sparqlRequests'),

]