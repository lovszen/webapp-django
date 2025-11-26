from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Alumno

@login_required
def buscar_alumnos(request):
    query = request.GET.get('q', '')
    resultados = []
    
    if query:
        alumnos = Alumno.objects.filter(
            usuario=request.user
        ).filter(
            nombre__icontains=query
        ) | Alumno.objects.filter(
            usuario=request.user
        ).filter(
            apellido__icontains=query
        ) | Alumno.objects.filter(
            usuario=request.user
        ).filter(
            carrera__icontains=query
        )
        
        for alumno in alumnos:
            resultados.append({
                'alumno': alumno,
                'titulo': f'{alumno.nombre} {alumno.apellido}',
                'contenido': f'Carrera: {alumno.carrera} | Email: {alumno.email}',
                'fuente': 'Base de datos local'
            })
    
    return render(request, 'scraper/buscar.html', {
        'resultados': resultados,
        'query': query
    })