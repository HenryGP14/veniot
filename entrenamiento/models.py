from django.db import models

from entrenamiento.encoder import model

# Create your models here.
class Media(models.Model):
    nombre = models.TextField()
    ruta = models.FileField(upload_to="sounds/")
    fecha = models.DateTimeField(auto_now=True)
