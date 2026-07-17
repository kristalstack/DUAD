-- Crear el schema si todavía no existe
CREATE SCHEMA IF NOT EXISTS lyfter_car_rental;

-- Eliminar la tabla si ya existe para poder ejecutar
-- nuevamente el script durante las pruebas
DROP TABLE IF EXISTS lyfter_car_rental.users CASCADE;

-- Crear la tabla de usuarios
CREATE TABLE lyfter_car_rental.users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    account_status VARCHAR(20) NOT NULL
        CHECK (account_status IN ('active', 'inactive', 'suspended')),
    is_delinquent BOOLEAN NOT NULL DEFAULT FALSE
);

-- Insertar 50 usuarios
INSERT INTO lyfter_car_rental.users (
    full_name,
    email,
    username,
    password,
    birth_date,
    account_status
)
VALUES
    ('Ana López', 'ana.lopez1@example.com', 'analopez1', 'password001', '1990-03-15', 'active'),
    ('Carlos Ramírez', 'carlos.ramirez2@example.com', 'carlosramirez2', 'password002', '1985-07-22', 'active'),
    ('María González', 'maria.gonzalez3@example.com', 'mariagonzalez3', 'password003', '1992-11-08', 'inactive'),
    ('José Hernández', 'jose.hernandez4@example.com', 'josehernandez4', 'password004', '1988-01-30', 'active'),
    ('Laura Martínez', 'laura.martinez5@example.com', 'lauramartinez5', 'password005', '1995-05-17', 'active'),
    ('Pedro Sánchez', 'pedro.sanchez6@example.com', 'pedrosanchez6', 'password006', '1982-09-12', 'suspended'),
    ('Sofía Torres', 'sofia.torres7@example.com', 'sofiatorres7', 'password007', '1998-02-25', 'active'),
    ('Diego Vargas', 'diego.vargas8@example.com', 'diegovargas8', 'password008', '1991-06-19', 'active'),
    ('Valentina Castro', 'valentina.castro9@example.com', 'valentinacastro9', 'password009', '1996-10-03', 'inactive'),
    ('Andrés Méndez', 'andres.mendez10@example.com', 'andresmendez10', 'password010', '1987-12-14', 'active'),
    ('Camila Rojas', 'camila.rojas11@example.com', 'camilarojas11', 'password011', '1993-04-21', 'active'),
    ('Fernando Morales', 'fernando.morales12@example.com', 'fernandomorales12', 'password012', '1980-08-09', 'suspended'),
    ('Daniela Navarro', 'daniela.navarro13@example.com', 'danielanavarro13', 'password013', '1999-01-11', 'active'),
    ('Ricardo Jiménez', 'ricardo.jimenez14@example.com', 'ricardojimenez14', 'password014', '1986-05-28', 'inactive'),
    ('Gabriela Ortiz', 'gabriela.ortiz15@example.com', 'gabrielaortiz15', 'password015', '1994-09-07', 'active'),
    ('Miguel Castillo', 'miguel.castillo16@example.com', 'miguelcastillo16', 'password016', '1989-03-18', 'active'),
    ('Natalia Vega', 'natalia.vega17@example.com', 'nataliavega17', 'password017', '1997-07-26', 'active'),
    ('Javier Guerrero', 'javier.guerrero18@example.com', 'javierguerrero18', 'password018', '1983-11-02', 'inactive'),
    ('Isabella Flores', 'isabella.flores19@example.com', 'isabellaflores19', 'password019', '2000-02-13', 'active'),
    ('Manuel Cabrera', 'manuel.cabrera20@example.com', 'manuelcabrera20', 'password020', '1984-06-24', 'suspended'),
    ('Lucía Silva', 'lucia.silva21@example.com', 'luciasilva21', 'password021', '1991-10-16', 'active'),
    ('Sebastián Reyes', 'sebastian.reyes22@example.com', 'sebastianreyes22', 'password022', '1995-12-05', 'active'),
    ('Paula Mendoza', 'paula.mendoza23@example.com', 'paulamendoza23', 'password023', '1988-04-27', 'inactive'),
    ('Alejandro Núñez', 'alejandro.nunez24@example.com', 'alejandronunez24', 'password024', '1992-08-20', 'active'),
    ('Mariana Herrera', 'mariana.herrera25@example.com', 'marianaherrera25', 'password025', '1996-01-09', 'active'),
    ('Esteban Paredes', 'esteban.paredes26@example.com', 'estebanparedes26', 'password026', '1981-05-31', 'suspended'),
    ('Renata Campos', 'renata.campos27@example.com', 'renatacampos27', 'password027', '1998-09-23', 'active'),
    ('Tomás Acosta', 'tomas.acosta28@example.com', 'tomasacosta28', 'password028', '1987-02-04', 'active'),
    ('Victoria Peña', 'victoria.pena29@example.com', 'victoriapena29', 'password029', '1993-06-15', 'inactive'),
    ('Martín Lozano', 'martin.lozano30@example.com', 'martinlozano30', 'password030', '1985-10-29', 'active'),
    ('Elena Fuentes', 'elena.fuentes31@example.com', 'elenafuentes31', 'password031', '1990-12-12', 'active'),
    ('Nicolás Salazar', 'nicolas.salazar32@example.com', 'nicolassalazar32', 'password032', '1994-03-06', 'active'),
    ('Adriana Miranda', 'adriana.miranda33@example.com', 'adrianamiranda33', 'password033', '1989-07-18', 'suspended'),
    ('Felipe Cordero', 'felipe.cordero34@example.com', 'felipecordero34', 'password034', '1982-11-25', 'active'),
    ('Andrea Espinoza', 'andrea.espinoza35@example.com', 'andreaespinoza35', 'password035', '1997-01-14', 'inactive'),
    ('Santiago Molina', 'santiago.molina36@example.com', 'santiagomolina36', 'password036', '1991-05-22', 'active'),
    ('Juliana Arias', 'juliana.arias37@example.com', 'julianaarias37', 'password037', '1999-08-30', 'active'),
    ('Cristian Valdez', 'cristian.valdez38@example.com', 'cristianvaldez38', 'password038', '1986-12-03', 'suspended'),
    ('Carolina Soto', 'carolina.soto39@example.com', 'carolinasoto39', 'password039', '1993-02-17', 'active'),
    ('Roberto Álvarez', 'roberto.alvarez40@example.com', 'robertoalvarez40', 'password040', '1980-06-08', 'active'),
    ('Mónica León', 'monica.leon41@example.com', 'monicaleon41', 'password041', '1995-10-21', 'inactive'),
    ('Hugo Benítez', 'hugo.benitez42@example.com', 'hugobenitez42', 'password042', '1988-01-26', 'active'),
    ('Patricia Zamora', 'patricia.zamora43@example.com', 'patriciazamora43', 'password043', '1992-04-10', 'active'),
    ('Óscar Villalobos', 'oscar.villalobos44@example.com', 'oscarvillalobos44', 'password044', '1984-09-19', 'suspended'),
    ('Alejandra Solís', 'alejandra.solis45@example.com', 'alejandrasolis45', 'password045', '1996-11-27', 'active'),
    ('Emilio Duarte', 'emilio.duarte46@example.com', 'emilioduarte46', 'password046', '1989-03-02', 'active'),
    ('Verónica Calderón', 'veronica.calderon47@example.com', 'veronicacalderon47', 'password047', '1994-07-13', 'inactive'),
    ('Raúl Palacios', 'raul.palacios48@example.com', 'raulpalacios48', 'password048', '1983-12-20', 'active'),
    ('Sara Montero', 'sara.montero49@example.com', 'saramontero49', 'password049', '1998-05-05', 'active'),
    ('Iván Quesada', 'ivan.quesada50@example.com', 'ivanquesada50', 'password050', '1987-08-16', 'active');