from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Alumno
from .forms import RegistroForm, AlumnoForm
import io
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth import logout

@login_required
def generar_pdf_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id, usuario=request.user)
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "SISTEMA DE GESTIÓN ACADÉMICA")
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
        p.drawString(100, 670, f"Carrera/Curso: {alumno.carrera}")
    
    if alumno.fecha_nacimiento:
        p.drawString(100, 650, f"Fecha Nacimiento: {alumno.fecha_nacimiento}")
    
    p.drawString(100, 630, f"Fecha Inscripción: {alumno.fecha_inscripcion}")
    
    p.drawString(100, 600, "Documento generado automáticamente")
    p.drawString(100, 580, f"Usuario: {request.user.username}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    
    send_mail(
        f'Ficha Académica - {alumno.nombre} {alumno.apellido}',
        f'Estimado/a {request.user.username},\n\nAdjuntamos la ficha académica del alumno {alumno.nombre} {alumno.apellido}.\n\nSaludos cordiales,\nSistema de Gestión Académica',
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
        attachments=[(f'ficha_{alumno.nombre}_{alumno.apellido}.pdf', buffer.getvalue(), 'application/pdf')]
    )
    
    messages.success(request, f'PDF enviado por correo a {request.user.email}')
    return redirect('dashboard')