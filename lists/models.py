from django.db import models

# Create your models here. 
#ORM converts Object Data into a Relational Data
class Item(models.Model):
    text = models.TextField(default='')
