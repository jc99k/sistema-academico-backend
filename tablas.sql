-- Creación de tablas para el sistema de matrícula universitaria

-- Tabla ESTUDIANTE
CREATE TABLE estudiante (
    estudiante_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento DATE NOT NULL,
    direccion VARCHAR(200),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla PROFESOR
CREATE TABLE profesor (
    profesor_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    especialidad VARCHAR(100),
    titulo_academico VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla FACULTAD
CREATE TABLE facultad (
    facultad_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    ubicacion VARCHAR(100),
    decano VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla CARRERA
CREATE TABLE carrera (
    carrera_id SERIAL PRIMARY KEY,
    facultad_id INTEGER NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    duracion_semestres INTEGER NOT NULL,
    titulo_otorgado VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_facultad FOREIGN KEY (facultad_id) REFERENCES facultad(facultad_id) ON DELETE RESTRICT,
    CONSTRAINT uk_carrera_nombre UNIQUE (nombre)
);

-- Tabla CURSO
CREATE TABLE curso (
    curso_id SERIAL PRIMARY KEY,
    carrera_id INTEGER NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    creditos INTEGER NOT NULL,
    nivel_semestre INTEGER NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_carrera FOREIGN KEY (carrera_id) REFERENCES carrera(carrera_id) ON DELETE RESTRICT,
    CONSTRAINT ck_creditos CHECK (creditos > 0),
    CONSTRAINT ck_nivel_semestre CHECK (nivel_semestre > 0)
);

-- Tabla PRERREQUISITO
CREATE TABLE prerrequisito (
    prerrequisito_id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    curso_req_id INTEGER NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_curso FOREIGN KEY (curso_id) REFERENCES curso(curso_id) ON DELETE CASCADE,
    CONSTRAINT fk_curso_req FOREIGN KEY (curso_req_id) REFERENCES curso(curso_id) ON DELETE CASCADE,
    CONSTRAINT uk_prerrequisito UNIQUE (curso_id, curso_req_id),
    CONSTRAINT ck_curso_diferente CHECK (curso_id != curso_req_id)
);

-- Tabla SECCION
CREATE TABLE seccion (
    seccion_id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    profesor_id INTEGER NOT NULL,
    codigo VARCHAR(20) NOT NULL,
    capacidad_maxima INTEGER NOT NULL,
    aula VARCHAR(50),
    horario VARCHAR(50),
    dias VARCHAR(50),
    periodo_academico VARCHAR(20) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_curso FOREIGN KEY (curso_id) REFERENCES curso(curso_id) ON DELETE RESTRICT,
    CONSTRAINT fk_profesor FOREIGN KEY (profesor_id) REFERENCES profesor(profesor_id) ON DELETE RESTRICT,
    CONSTRAINT uk_seccion_periodo UNIQUE (curso_id, codigo, periodo_academico),
    CONSTRAINT ck_capacidad_maxima CHECK (capacidad_maxima > 0)
);

-- Tabla MATRICULA
CREATE TABLE matricula (
    matricula_id SERIAL PRIMARY KEY,
    estudiante_id INTEGER NOT NULL,
    seccion_id INTEGER NOT NULL,
    fecha_matricula DATE NOT NULL DEFAULT CURRENT_DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
    costo NUMERIC(10, 2) NOT NULL,
    metodo_pago VARCHAR(50),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiante(estudiante_id) ON DELETE RESTRICT,
    CONSTRAINT fk_seccion FOREIGN KEY (seccion_id) REFERENCES seccion(seccion_id) ON DELETE RESTRICT,
    CONSTRAINT uk_matricula_seccion UNIQUE (estudiante_id, seccion_id),
    CONSTRAINT ck_estado CHECK (estado IN ('PENDIENTE', 'PAGADO', 'ANULADO', 'COMPLETADO')),
    CONSTRAINT ck_costo CHECK (costo >= 0)
);

-- Tabla PAGO
CREATE TABLE pago (
    pago_id SERIAL PRIMARY KEY,
    matricula_id INTEGER NOT NULL,
    fecha_pago DATE NOT NULL DEFAULT CURRENT_DATE,
    monto NUMERIC(10, 2) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    referencia VARCHAR(100),
    estado VARCHAR(20) NOT NULL DEFAULT 'PROCESADO',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_matricula FOREIGN KEY (matricula_id) REFERENCES matricula(matricula_id) ON DELETE RESTRICT,
    CONSTRAINT ck_monto CHECK (monto > 0),
    CONSTRAINT ck_estado_pago CHECK (estado IN ('PENDIENTE', 'PROCESADO', 'RECHAZADO'))
);

-- Tabla CALIFICACION
CREATE TABLE calificacion (
    calificacion_id SERIAL PRIMARY KEY,
    matricula_id INTEGER NOT NULL,
    nota NUMERIC(5, 2),
    observacion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_matricula FOREIGN KEY (matricula_id) REFERENCES matricula(matricula_id) ON DELETE RESTRICT,
    CONSTRAINT uk_calificacion_matricula UNIQUE (matricula_id),
    CONSTRAINT ck_nota CHECK (nota >= 0 AND nota <= 20)
);

-- Indices para mejorar el rendimiento
CREATE INDEX idx_estudiante_apellido ON estudiante(apellido);
CREATE INDEX idx_profesor_apellido ON profesor(apellido);
CREATE INDEX idx_curso_nombre ON curso(nombre);
CREATE INDEX idx_curso_codigo ON curso(codigo);
CREATE INDEX idx_matricula_estudiante ON matricula(estudiante_id);
CREATE INDEX idx_matricula_seccion ON matricula(seccion_id);
CREATE INDEX idx_seccion_curso ON seccion(curso_id);
CREATE INDEX idx_seccion_profesor ON seccion(profesor_id);
CREATE INDEX idx_seccion_periodo ON seccion(periodo_academico);
CREATE INDEX idx_carrera_facultad ON carrera(facultad_id);

-- Vistas útiles para el sistema

-- Vista para obtener la lista de matrículas con información completa
CREATE VIEW v_matriculas AS
SELECT 
    m.matricula_id,
    e.estudiante_id,
    e.nombre || ' ' || e.apellido AS estudiante,
    e.dni AS estudiante_dni,
    c.codigo AS codigo_curso,
    c.nombre AS nombre_curso,
    s.codigo AS codigo_seccion,
    p.nombre || ' ' || p.apellido AS profesor,
    s.periodo_academico,
    m.fecha_matricula,
    m.estado,
    m.costo,
    COALESCE(cal.nota, 0) AS nota
FROM 
    matricula m
    JOIN estudiante e ON m.estudiante_id = e.estudiante_id
    JOIN seccion s ON m.seccion_id = s.seccion_id
    JOIN curso c ON s.curso_id = c.curso_id
    JOIN profesor p ON s.profesor_id = p.profesor_id
    LEFT JOIN calificacion cal ON m.matricula_id = cal.matricula_id;

-- Vista para obtener el historial académico de un estudiante
CREATE VIEW v_historial_academico AS
SELECT 
    e.estudiante_id,
    e.nombre || ' ' || e.apellido AS estudiante,
    e.dni,
    c.codigo AS codigo_curso,
    c.nombre AS nombre_curso,
    c.creditos,
    c.nivel_semestre,
    ca.nombre AS carrera,
    s.periodo_academico,
    COALESCE(cal.nota, 0) AS nota,
    CASE 
        WHEN cal.nota >= 11 THEN 'APROBADO'
        WHEN cal.nota < 11 AND cal.nota > 0 THEN 'DESAPROBADO'
        ELSE 'PENDIENTE'
    END AS estado
FROM 
    estudiante e
    JOIN matricula m ON e.estudiante_id = m.estudiante_id
    JOIN seccion s ON m.seccion_id = s.seccion_id
    JOIN curso c ON s.curso_id = c.curso_id
    JOIN carrera ca ON c.carrera_id = ca.carrera_id
    LEFT JOIN calificacion cal ON m.matricula_id = cal.matricula_id;

-- Vista para obtener la carga académica de un profesor
CREATE VIEW v_carga_academica_profesor AS
SELECT 
    p.profesor_id,
    p.nombre || ' ' || p.apellido AS profesor,
    c.codigo AS codigo_curso,
    c.nombre AS nombre_curso,
    s.codigo AS codigo_seccion,
    s.periodo_academico,
    s.horario,
    s.dias,
    s.aula,
    COUNT(m.matricula_id) AS num_estudiantes
FROM 
    profesor p
    JOIN seccion s ON p.profesor_id = s.profesor_id
    JOIN curso c ON s.curso_id = c.curso_id
    LEFT JOIN matricula m ON s.seccion_id = m.seccion_id
GROUP BY 
    p.profesor_id, p.nombre, p.apellido, c.codigo, c.nombre, s.codigo, 
    s.periodo_academico, s.horario, s.dias, s.aula;

-- Vista para obtener estadísticas de matrícula por periodo académico
CREATE VIEW v_estadisticas_matricula AS
SELECT 
    s.periodo_academico,
    c.carrera_id,
    ca.nombre AS carrera,
    f.nombre AS facultad,
    COUNT(DISTINCT m.estudiante_id) AS total_estudiantes,
    COUNT(m.matricula_id) AS total_matriculas,
    SUM(m.costo) AS ingresos_totales
FROM 
    matricula m
    JOIN seccion s ON m.seccion_id = s.seccion_id
    JOIN curso c ON s.curso_id = c.curso_id
    JOIN carrera ca ON c.carrera_id = ca.carrera_id
    JOIN facultad f ON ca.facultad_id = f.facultad_id
GROUP BY 
    s.periodo_academico, c.carrera_id, ca.nombre, f.nombre;