# Sistema Academico Backend

API REST para gestion de sistema academico universitario construida con FastAPI y SQLModel.

## Caracteristicas

- **FastAPI**: Framework web moderno y rapido
- **SQLModel**: ORM basado en Pydantic para validacion de datos y modelos de base de datos
- **PostgreSQL**: Base de datos relacional
- **Arquitectura MVC**: Separacion clara de modelos, controladores (rutas) y configuracion
- **CRUD Completo**: Operaciones Create, Read, Update, Delete para todas las entidades

## Entidades del Sistema

- **Estudiante**: Gestion de estudiantes
- **Profesor**: Gestion de profesores
- **Facultad**: Gestion de facultades
- **Carrera**: Gestion de carreras academicas
- **Curso**: Gestion de cursos/materias
- **Seccion**: Gestion de secciones de cursos
- **Matricula**: Gestion de matriculas de estudiantes
- **Pago**: Gestion de pagos de matriculas
- **Calificacion**: Gestion de calificaciones

## Estructura del Proyecto

```
sistema-academico-backend/
├── app/
│   ├── models/          # Modelos SQLModel (tablas de base de datos)
│   │   ├── estudiante.py
│   │   ├── profesor.py
│   │   ├── facultad.py
│   │   ├── carrera.py
│   │   ├── curso.py
│   │   ├── seccion.py
│   │   ├── matricula.py
│   │   ├── pago.py
│   │   └── calificacion.py
│   ├── routes/          # Controladores/Rutas FastAPI
│   │   ├── estudiante.py
│   │   ├── profesor.py
│   │   ├── facultad.py
│   │   ├── carrera.py
│   │   ├── curso.py
│   │   ├── seccion.py
│   │   ├── matricula.py
│   │   ├── pago.py
│   │   └── calificacion.py
│   ├── config.py        # Configuracion de la aplicacion
│   └── database.py      # Configuracion de base de datos
├── main.py              # Punto de entrada de la aplicacion
├── pyproject.toml       # Configuracion del proyecto y dependencias (uv)
├── .env.example         # Ejemplo de variables de entorno
└── README.md
```

## Instalacion

### Prerequisitos

- Python 3.11 o superior
- PostgreSQL
- [uv](https://docs.astral.sh/uv/) - Gestor de paquetes Python ultra-rapido

Para instalar uv:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Pasos de instalacion

1. **Clonar el repositorio**

2. **Sincronizar dependencias con uv**
```bash
uv sync
```

Este comando automaticamente:
- Crea un entorno virtual (.venv)
- Instala todas las dependencias del proyecto
- Genera el archivo uv.lock para versiones reproducibles

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. **Configurar la base de datos**

Crear la base de datos PostgreSQL:
```bash
createdb sistema_academico
```

Ejecutar el script SQL para crear las tablas:
```bash
psql -d sistema_academico -f tablas.sql
```

O dejar que SQLModel cree las tablas automaticamente al iniciar la aplicacion.

## Uso

### Iniciar el servidor de desarrollo

```bash
uv run python main.py
```

O usar uvicorn directamente:
```bash
uv run uvicorn main:app --reload
```

El servidor estara disponible en `http://localhost:8000`

### Agregar nuevas dependencias

```bash
uv add nombre-del-paquete
```

### Actualizar dependencias

```bash
uv sync --upgrade
```

### Documentacion API

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/api/v1/openapi.json`

## Endpoints API

Todos los endpoints estan bajo el prefijo `/api/v1`

### Estudiantes
- `POST /api/v1/estudiantes` - Crear estudiante
- `GET /api/v1/estudiantes` - Listar estudiantes
- `GET /api/v1/estudiantes/{id}` - Obtener estudiante
- `PATCH /api/v1/estudiantes/{id}` - Actualizar estudiante
- `DELETE /api/v1/estudiantes/{id}` - Eliminar estudiante

### Profesores
- `POST /api/v1/profesores` - Crear profesor
- `GET /api/v1/profesores` - Listar profesores
- `GET /api/v1/profesores/{id}` - Obtener profesor
- `PATCH /api/v1/profesores/{id}` - Actualizar profesor
- `DELETE /api/v1/profesores/{id}` - Eliminar profesor

### Facultades
- `POST /api/v1/facultades` - Crear facultad
- `GET /api/v1/facultades` - Listar facultades
- `GET /api/v1/facultades/{id}` - Obtener facultad
- `PATCH /api/v1/facultades/{id}` - Actualizar facultad
- `DELETE /api/v1/facultades/{id}` - Eliminar facultad

### Carreras
- `POST /api/v1/carreras` - Crear carrera
- `GET /api/v1/carreras` - Listar carreras
- `GET /api/v1/carreras/{id}` - Obtener carrera
- `PATCH /api/v1/carreras/{id}` - Actualizar carrera
- `DELETE /api/v1/carreras/{id}` - Eliminar carrera

### Cursos
- `POST /api/v1/cursos` - Crear curso
- `GET /api/v1/cursos` - Listar cursos
- `GET /api/v1/cursos/{id}` - Obtener curso
- `PATCH /api/v1/cursos/{id}` - Actualizar curso
- `DELETE /api/v1/cursos/{id}` - Eliminar curso

### Secciones
- `POST /api/v1/secciones` - Crear seccion
- `GET /api/v1/secciones` - Listar secciones
- `GET /api/v1/secciones/{id}` - Obtener seccion
- `PATCH /api/v1/secciones/{id}` - Actualizar seccion
- `DELETE /api/v1/secciones/{id}` - Eliminar seccion

### Matriculas
- `POST /api/v1/matriculas` - Crear matricula
- `GET /api/v1/matriculas` - Listar matriculas
- `GET /api/v1/matriculas/{id}` - Obtener matricula
- `PATCH /api/v1/matriculas/{id}` - Actualizar matricula
- `DELETE /api/v1/matriculas/{id}` - Eliminar matricula

### Pagos
- `POST /api/v1/pagos` - Crear pago
- `GET /api/v1/pagos` - Listar pagos
- `GET /api/v1/pagos/{id}` - Obtener pago
- `PATCH /api/v1/pagos/{id}` - Actualizar pago
- `DELETE /api/v1/pagos/{id}` - Eliminar pago

### Calificaciones
- `POST /api/v1/calificaciones` - Crear calificacion
- `GET /api/v1/calificaciones` - Listar calificaciones
- `GET /api/v1/calificaciones/{id}` - Obtener calificacion
- `PATCH /api/v1/calificaciones/{id}` - Actualizar calificacion
- `DELETE /api/v1/calificaciones/{id}` - Eliminar calificacion

## Ejemplo de Uso

### Crear un estudiante

```bash
curl -X POST "http://localhost:8000/api/v1/estudiantes" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "Perez",
    "dni": "12345678",
    "email": "juan.perez@example.com",
    "fecha_nacimiento": "2000-01-15",
    "telefono": "987654321",
    "direccion": "Av. Principal 123"
  }'
```

### Listar estudiantes

```bash
curl "http://localhost:8000/api/v1/estudiantes"
```

## Configuracion de Base de Datos

Actualizar la variable `DATABASE_URL` en el archivo `.env`:

```
DATABASE_URL=postgresql://usuario:password@localhost:5432/sistema_academico
```

## Tecnologias

- **uv**: Gestor de paquetes y entornos virtuales Python ultra-rapido
- **FastAPI**: Framework web asincrono
- **SQLModel**: ORM y validacion de datos
- **Pydantic**: Validacion de datos
- **PostgreSQL**: Base de datos
- **Uvicorn**: Servidor ASGI
- **psycopg2**: Driver PostgreSQL

## Licencia

Este proyecto es de codigo abierto y esta disponible bajo la licencia MIT.
