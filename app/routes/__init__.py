from .estudiante import router as estudiante_router
from .profesor import router as profesor_router
from .facultad import router as facultad_router
from .carrera import router as carrera_router
from .curso import router as curso_router
from .seccion import router as seccion_router
from .matricula import router as matricula_router
from .pago import router as pago_router
from .calificacion import router as calificacion_router

__all__ = [
    "estudiante_router",
    "profesor_router",
    "facultad_router",
    "carrera_router",
    "curso_router",
    "seccion_router",
    "matricula_router",
    "pago_router",
    "calificacion_router",
]
