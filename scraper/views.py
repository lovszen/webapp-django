from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def buscar_educativo(request):
    query = request.GET.get('q', '')
    resultados = []
    
    if query:
        resultados = [{
            'titulo': f'Resultado para "{query}"',
            'contenido': f'Información educativa sobre {query}',
            'fuente': 'Sistema Educativo'
        }]
    
    return render(request, 'scraper/buscar.html', {
        'resultados': resultados,
        'query': query
    })