from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Produto(models.Model):

    codigo = models.IntegerField(validators=[MaxValueValidator(10000000000), MinValueValidator(0)])
    nome = models.CharField(max_length=15)
    descricao = models.CharField(max_length=30, blank=True, default='', null=True)
    preco = models.FloatField(validators=[MinValueValidator(0.0)])
    tipo = models.CharField(max_length=1)



