from django.db import models
from django.contrib.auth.models import User 

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    carrera = models.CharField(max_length=100, blank=True, verbose_name="Carrera o Curso")
    dni = models.CharField(max_length=15, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"