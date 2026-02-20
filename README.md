<div align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/DRF-REST_Framework-ff1709?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
<img src="https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>

<br/><br/>

# ✈️ Travel Agency — Backend API

**API RESTful construida con Django REST Framework para la gestión completa de una agencia de viajes.**  
Administra paquetes, destinos, reservas, clientes y autenticación basada en roles — lista para producción.

[📖 API Docs](#-api-endpoints) · [🚀 Quick Start](#-getting-started) · [🐳 Docker](#-running-with-docker) · [🤝 Contributing](#-contributing)

</div>

---

## 📌 Overview

Este servicio backend impulsa una plataforma completa de **gestión de agencia de viajes**, exponiendo APIs REST seguras y escalables para:

- 🗺️ Catálogo de paquetes turísticos y destinos
- 👤 Registro y gestión de perfiles de clientes
- 📅 Ciclo de vida de reservas y disponibilidad
- 🔐 Autenticación JWT con control de roles (Admin / Customer)
- 📊 Seguimiento de disponibilidad y reportes

---

## 🛠️ Tech Stack

| Layer            | Technology                          |
|------------------|-------------------------------------|
| **Language**     | Python 3.11+                        |
| **Framework**    | Django 4.x                          |
| **REST Layer**   | Django REST Framework (DRF)         |
| **Auth**         | SimpleJWT                           |
| **Database**     | PostgreSQL 16 / MySQL 8             |
| **ORM**          | Django ORM                          |
| **API Docs**     | drf-spectacular (OpenAPI 3)         |
| **Container**    | Docker + Docker Compose             |
| **Environment**  | python-decouple / django-environ    |

---

## 🏗️ Architecture

Arquitectura en capas siguiendo las convenciones de Django con separación de responsabilidades por apps:

```
travel_agency/
├── 📁 apps/
│   ├── 🔐 authentication/     → Login, register, JWT
│   ├── 🗺️  packages/           → Paquetes turísticos y destinos
│   ├── 📅  bookings/           → Reservas y disponibilidad
│   ├── 👤  customers/          → Clientes y perfiles
│   └── 🌍  destinations/       → Destinos y categorías
├── 📁 core/
│   ├── settings/
│   │   ├── base.py             → Configuración base
│   │   ├── development.py      → Config local
│   │   └── production.py       → Config producción
│   ├── urls.py                 → URL root
│   └── wsgi.py / asgi.py
├── 📁 utils/
│   ├── permissions.py          → Permisos personalizados
│   ├── pagination.py           → Paginación global
│   └── exceptions.py           → Manejo de errores global
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── manage.py
```

Cada **app** sigue la estructura interna:

```
packages/
├── models.py          → Modelos Django
├── serializers.py     → DRF Serializers
├── views.py           → ViewSets / APIViews
├── urls.py            → URL patterns
├── permissions.py     → Permisos específicos
└── tests.py           → Unit tests
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- 🐍 Python 3.11+
- 📦 pip / virtualenv
- 🐘 PostgreSQL 16
- 🐳 Docker *(opcional)*

### 📥 Installation

```bash
# 1. Clonar el repositorio
git clone https://github.com/Rodrigo-Salva/travel_agency_BackEnd.git
cd travel_agency_BackEnd

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver
```

> 🟢 Servidor en: `http://localhost:8000`  
> 📄 Swagger UI en: `http://localhost:8000/api/schema/swagger-ui/`  
> 📘 ReDoc en: `http://localhost:8000/api/schema/redoc/`

---

## 🔑 Environment Variables

Crea tu archivo `.env` en la raíz del proyecto:

```env
# ─── Django ───────────────────────────────────────
SECRET_KEY=your-super-secret-django-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ─── Database ─────────────────────────────────────
DB_ENGINE=django.db.backends.postgresql
DB_NAME=travel_agency_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# ─── JWT ──────────────────────────────────────────
JWT_ACCESS_TOKEN_LIFETIME=1        # days
JWT_REFRESH_TOKEN_LIFETIME=7       # days

# ─── CORS ─────────────────────────────────────────
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

> ⚠️ **Nunca subas tu `.env` al repositorio.** Asegúrate de tenerlo en `.gitignore`.

---

## 📡 API Endpoints

**Base URL:** `http://localhost:8000/api/v1`

<details>
<summary>🔐 <strong>Authentication</strong></summary>

| Method | Endpoint                  | Description                  | Access |
|--------|---------------------------|------------------------------|--------|
| `POST` | `/auth/register/`         | Registrar nuevo usuario      | Public |
| `POST` | `/auth/login/`            | Login y obtener tokens JWT   | Public |
| `POST` | `/auth/token/refresh/`    | Refrescar access token       | Public |
| `POST` | `/auth/logout/`           | Cerrar sesión (blacklist)    | Auth   |

</details>

<details>
<summary>🗺️ <strong>Packages</strong></summary>

| Method   | Endpoint                  | Description                  | Access |
|----------|---------------------------|------------------------------|--------|
| `GET`    | `/packages/`              | Listar todos los paquetes    | Public |
| `GET`    | `/packages/{id}/`         | Detalle de un paquete        | Public |
| `POST`   | `/packages/`              | Crear paquete                | Admin  |
| `PUT`    | `/packages/{id}/`         | Actualizar paquete completo  | Admin  |
| `PATCH`  | `/packages/{id}/`         | Actualizar campos parciales  | Admin  |
| `DELETE` | `/packages/{id}/`         | Eliminar paquete             | Admin  |

</details>

<details>
<summary>📅 <strong>Bookings</strong></summary>

| Method   | Endpoint                  | Description                  | Access |
|----------|---------------------------|------------------------------|--------|
| `GET`    | `/bookings/`              | Listar reservas              | Admin  |
| `GET`    | `/bookings/{id}/`         | Detalle de reserva           | Auth   |
| `POST`   | `/bookings/`              | Crear reserva                | Auth   |
| `PATCH`  | `/bookings/{id}/`         | Actualizar estado            | Admin  |
| `DELETE` | `/bookings/{id}/`         | Cancelar reserva             | Auth   |

</details>

<details>
<summary>👤 <strong>Customers</strong></summary>

| Method  | Endpoint                   | Description                  | Access |
|---------|----------------------------|------------------------------|--------|
| `GET`   | `/customers/`              | Listar clientes              | Admin  |
| `GET`   | `/customers/{id}/`         | Detalle de cliente           | Admin  |
| `PUT`   | `/customers/{id}/`         | Actualizar perfil            | Auth   |
| `PATCH` | `/customers/{id}/`         | Actualizar campos parciales  | Auth   |

</details>

<details>
<summary>🌍 <strong>Destinations</strong></summary>

| Method   | Endpoint                   | Description                  | Access |
|----------|----------------------------|------------------------------|--------|
| `GET`    | `/destinations/`           | Listar destinos              | Public |
| `GET`    | `/destinations/{id}/`      | Detalle de destino           | Public |
| `POST`   | `/destinations/`           | Crear destino                | Admin  |
| `DELETE` | `/destinations/{id}/`      | Eliminar destino             | Admin  |

</details>

---

## 🗃️ Database Schema

```
┌──────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│    customers     │     │    packages      │     │     bookings       │
├──────────────────┤     ├──────────────────┤     ├────────────────────┤
│ id          (PK) │     │ id          (PK) │     │ id            (PK) │
│ user_id     (FK) │     │ title            │     │ customer_id   (FK) │──▶ customers
│ phone            │     │ description      │     │ package_id    (FK) │──▶ packages
│ address          │     │ price            │     │ booking_date       │
│ birth_date       │     │ duration_days    │     │ travel_date        │
│ created_at       │     │ destination (FK) │──▶  │ status             │
└──────────────────┘     │ available_slots  │     │ total_price        │
                         │ image_url        │     │ passengers         │
┌──────────────────┐     │ created_at       │     │ created_at         │
│  destinations    │     └──────────────────┘     └────────────────────┘
├──────────────────┤
│ id          (PK) │
│ name             │
│ country          │
│ description      │
│ image_url        │
└──────────────────┘
```

---

## 🐳 Running with Docker

```bash
# Construir y levantar todos los servicios
docker-compose up --build

# Modo background
docker-compose up -d

# Aplicar migraciones en contenedor
docker-compose exec web python manage.py migrate

# Crear superusuario en contenedor
docker-compose exec web python manage.py createsuperuser

# Detener servicios
docker-compose down
```

Servicios levantados por `docker-compose.yml`:

| Service  | Description                | Port   |
|----------|----------------------------|--------|
| `web`    | Django application         | `8000` |
| `db`     | PostgreSQL instance        | `5432` |

---

## 🧪 Running Tests

```bash
# Ejecutar todos los tests
python manage.py test

# Test de una app específica
python manage.py test apps.bookings

# Con cobertura
pip install coverage
coverage run manage.py test
coverage report
```

---

## 🤝 Contributing

1. 🍴 Haz fork del repositorio
2. 🌿 Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. ✅ Commitea tus cambios: `git commit -m "feat: descripción del cambio"`
4. 📤 Push a tu rama: `git push origin feature/nueva-funcionalidad`
5. 🔁 Abre un Pull Request

> Sigue el estándar de [Conventional Commits](https://www.conventionalcommits.org/) para los mensajes.

---

## 📄 License

Este proyecto está bajo la licencia **MIT** — consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

Made with ❤️ by <a href="https://github.com/Rodrigo-Salva">Rodrigo Salva</a>

</div>
