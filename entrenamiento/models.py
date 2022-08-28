import os
from django.db import models

from entrenamiento.encoder import model

# Create your models here.
class Media(models.Model):
    nombre = models.TextField()
    ruta = models.FileField(upload_to="sounds/")
    fecha = models.DateTimeField(auto_now=True)
    ruta_audio_clonado = models.TextField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.ruta.storage, self.ruta.path
        # Delete the model before the file
        super(Media, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
        try:
            os.remove("./" + self.ruta_audio_clonado)
        except:
            pass
