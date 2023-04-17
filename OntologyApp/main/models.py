from django.db import models

# Create your models here.


class SPARQLRequest(models.Model):
    body = models.TextField('SPARQL Request', blank=True, null=True)

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'SPARQLRequest'
        verbose_name_plural = 'SPARQLRequests'