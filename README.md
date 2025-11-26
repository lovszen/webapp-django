# Sistema de Gestión Académica - Django

## Descripción del Proyecto
Sistema web desarrollado en Django para la gestión de alumnos, generación de reportes en PDF y búsqueda de alumnos.

## Funcionalidades Implementadas

### Sistema de Autenticación
- Registro de usuarios (username + email + password)
- Login/Logout con sistema de Django  
- Templates con Bootstrap 5

### Dashboard de Alumnos
- Acceso restringido a usuarios autenticados
- Modelo Alumno: nombre, apellido, email, carrera, DNI, teléfono, fecha de nacimiento
- Cada usuario gestiona sus propios alumnos
- Interfaz administrativa personalizada

### Generación de PDF
- Generación de PDF con ReportLab
- Botón \"Generar PDF\" por cada alumno
- Diseño profesional con todos los datos del alumno

### Búsqueda de Alumnos
- Búsqueda por nombre o apellido de alumnos
- Resultados en tabla con información completa
- Interfaz intuitiva para buscar en la base de datos
