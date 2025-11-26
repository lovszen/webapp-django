from django.contrib import admin
from .models import Alumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'email', 'carrera', 'usuario', 'fecha_inscripcion']
    list_filter = ['carrera', 'fecha_inscripcion', 'usuario']
    search_fields = ['nombre', 'apellido', 'email', 'dni']
    readonly_fields = ['fecha_inscripcion']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'dni', 'fecha_nacimiento')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono')
        }),
        ('Información Académica', {
            'fields': ('carrera',)
        }),
        ('Metadata', {
            'fields': ('usuario', 'fecha_inscripcion')
        }),
    )