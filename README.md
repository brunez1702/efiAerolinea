# efiAerolinea
✈️ Sistema de Gestión de Aerolínea — API REST

Proyecto desarrollado en Django Rest Framework (DRF) como extensión del sistema de gestión de aerolínea.
Permite administrar vuelos, pasajeros, reservas y boletos a través de una API REST segura, documentada y modular, siguiendo el patrón Service–Repository.

🚀 Instalación y Uso Rápido

A continuación tenés los comandos listos para clonar, configurar y ejecutar el proyecto:

# 1️⃣ Clonar el repositorio
git clone https://github.com/brunez1702/efiAerolinea.git
cd efiAerolinea/aerolinea

# 2️⃣ Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows

# 3️⃣ Instalar dependencias
pip install -r requirements.txt

# 4️⃣ Aplicar migraciones
python manage.py migrate

# 5️⃣ Crear un superusuario
python manage.py createsuperuser

# 6️⃣ (Opcional) Cargar datos iniciales
python manage.py loaddata airline/fixtures/initial_data.json

# 7️⃣ Levantar el servidor
python manage.py runserver

🌐 Accesos Principales

| Seccion | URL | 

| **API Root**    | [http://localhost:8000/api/]     

| **Swagger UI**  | [http://localhost:8000/swagger/]

| **ReDoc**       | [http://localhost:8000/redoc/]   

| **Panel Admin** | [http://localhost:8000/admin/]

🧩 Autenticación (JWT)

La API utiliza autenticación con tokens JWT para gestionar sesiones seguras y control de acceso por roles (administrador / usuario).

| Metodo | Endpoints | Descripcion  |

| `POST` | `/api/auth/register/`      | Registro de nuevo usuario |

| `POST` | `/api/auth/login/`         | Inicio de sesión          |

| `POST` | `/api/auth/logout/`        | Cierre de sesión          |

| `POST` | `/api/auth/token/refresh/` | Renovar token JWT         |

🛫 Endpoints Principales
| Recurso | Endpoints |

| **Vuelos** | `/api/vuelos/`, `/api/vuelos/{id}/`, `/api/vuelos/buscar/` |

| **Pasajeros** | `/api/pasajeros/`, `/api/pasajeros/{id}/` |

| **Reservas** | `/api/reservas/`, `/api/reservas/{id}/`, `/api/reservas/mis_reservas/` |

| **Aviones** | `/api/aviones/`, `/api/aviones/{id}/` |

| **Asientos** | `/api/asientos/por_vuelo/?vuelo_id={id}` |

| **Boletos** | `/api/boletos/`, `/api/boletos/{id}/` |

| **Reportes** | `/api/reportes/vuelos_mas_reservados/`, `/api/reportes/pasajeros_frecuentes/` |

⚙️ Arquitectura del Backend

El backend está construido siguiendo una arquitectura modular con separación de responsabilidades clara:

Models: Estructura de datos y relaciones entre entidades.

Repositories: Acceso y manipulación de datos.

Services: Lógica de negocio y validaciones.

Views / ViewSets: Gestión de las peticiones HTTP.

URLs: Enrutamiento y conexión de vistas con endpoints.

Esto asegura un código limpio, escalable y fácil de mantener.

🗄️ Modelos de Datos Principales

User: Usuarios del sistema con roles definidos.

Pasajero: Datos personales vinculados a un usuario.

Avión: Modelo, capacidad y disposición de asientos.

Vuelo: Origen, destino, horarios, precio y avión asignado.

Reserva: Asociación entre pasajero, vuelo y asiento.

Boleto: Ticket emitido con código único.

Relaciones establecidas mediante ForeignKey y OneToOne para garantizar integridad referencial.

📚 Documentación

El proyecto cuenta con documentación automática generada con Swagger y ReDoc, accesible desde el navegador.
Incluye ejemplos, descripciones y parámetros de cada endpoint.

🧱 Tecnologías Utilizadas

Python 3.10+

Django 5.x

Django Rest Framework (DRF)

SimpleJWT (autenticación)

drf-yasg (Swagger/ReDoc)

SQLite / PostgreSQL

Bootstrap / HTML5 / CSS3

👩‍💻 Equipo de Desarrollo

Agostina Bringas

Micaela Cortez

Bruno Sanchez 