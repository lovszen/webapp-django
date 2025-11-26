from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .models import Alumno
from .forms import RegistroForm, AlumnoForm
import io
from reportlab.pdfgen import canvas

def home(request):
    return render(request, 'main/home.html')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                '¡Bienvenido/a al Sistema Académico!',
                f'Hola {user.username},\n\nTe has registrado exitosamente.\n\nSaludos,\nEquipo del Sistema',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            login(request, user)
            messages.success(request, '¡Registro exitoso! Email enviado.')
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'main/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido/a {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada')
    return redirect('home')

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'main/dashboard.html', {'alumnos': alumnos})

@login_required
def agregar_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, 'Alumno agregado')
            return redirect('dashboard')
    else:
        form = AlumnoForm()
    return render(request, 'main/form_alumno.html', {'form': form, 'titulo': 'Agregar Alumno'})

@login_required
def editar_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id, usuario=request.user)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno actualizado')
            return redirect('dashboard')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'main/form_alumno.html', {'form': form, 'titulo': 'Editar Alumno'})

@login_required
def eliminar_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id, usuario=request.user)
    if request.method == 'POST':
        alumno.delete()
        messages.success(request, 'Alumno eliminado')
        return redirect('dashboard')
    return render(request, 'main/eliminar_alumno.html', {'alumno': alumno})

@login_required
def generar_pdf_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id, usuario=request.user)
    
    try:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "SISTEMA ACADÉMICO")
        p.drawString(100, 780, "FICHA DEL ALUMNO")
        p.line(100, 775, 500, 775)
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 750, f"Nombre: {alumno.nombre} {alumno.apellido}")
        p.drawString(100, 730, f"Email: {alumno.email}")
        
        if alumno.dni:
            p.drawString(100, 710, f"DNI: {alumno.dni}")
        if alumno.telefono:
            p.drawString(100, 690, f"Teléfono: {alumno.telefono}")
        if alumno.carrera:
            p.drawString(100, 670, f"Carrera: {alumno.carrera}")
        if alumno.fecha_nacimiento:
            p.drawString(100, 650, f"Nacimiento: {alumno.fecha_nacimiento}")
        
        p.drawString(100, 630, f"Inscripción: {alumno.fecha_inscripcion}")
        p.drawString(100, 600, "Documento generado automáticamente")
        p.drawString(100, 580, f"Usuario: {request.user.username}")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        
        email = EmailMessage(
            f'Ficha Académica - {alumno.nombre} {alumno.apellido}',
            f'Ficha del alumno {alumno.nombre} {alumno.apellido} adjunta.',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
        )
        
        email.attach(f'ficha_{alumno.nombre}_{alumno.apellido}.pdf', buffer.getvalue(), 'application/pdf')
        email.send()
        
        messages.success(request, f'✅ PDF enviado REALMENTE a {request.user.email}')
        return redirect('dashboard')
    
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('dashboard')