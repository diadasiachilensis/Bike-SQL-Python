# 🚲 Bike SQL Python - MVP (CustomBikes Data Ops)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-13-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=for-the-badge&logo=docker&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.8.1-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?style=for-the-badge&logo=terraform&logoColor=white)

> **Estado:** 🟢 Operativo (MVP) | **Rama:** `main`

Proyecto **End-to-End** que integra **Infraestructura como Código (Terraform)** + **Base de Datos PostgreSQL** + **Orquestación con Apache Airflow** para generar reportes automatizados desde una base de datos de negocio (*CustomBikes*).

Este repositorio levanta:
- una **DB de negocio** (Postgres) provisionada vía **Terraform (Docker provider)** con scripts SQL de inicialización,
- un stack de **Airflow (webserver/scheduler/triggerer)** en Docker Compose,
- un **DAG** que verifica conectividad y genera un reporte en `./reports/`.

---

## 🏗️ Arquitectura del Sistema

El flujo se divide en dos capas:

### 1) Infra (Terraform)
- Provisiona **PostgreSQL de negocio** como contenedor Docker.
- Monta scripts SQL (`./sql`) para crear tablas y poblar datos.
- Expone el puerto **5432**.

### 2) Orquestación (Airflow + Docker Compose)
- Levanta **Postgres de metadatos de Airflow** (interno, separado de la DB de negocio).
- Levanta Airflow y ejecuta un DAG que:
  1) valida conectividad a la DB de negocio,
  2) ejecuta lógica Python y exporta un CSV a `./reports`.

---

## 🛠️ Stack Tecnológico

- **Infraestructura:** Terraform + Docker Provider (IaC)
- **Orquestación:** Apache Airflow 2.8.1 (LocalExecutor)
- **Base de datos:** PostgreSQL 13
- **Data/ETL:** Python (`pandas`, `sqlalchemy`, `psycopg2-binary`)
- **Contenerización:** Docker Engine + Docker Compose v2

---

## ✅ Pre-requisitos

- Docker Engine + Docker Compose (v2)
- Terraform (v1.x)
- Git
- (Opcional) Python 3.8+ si ejecutas utilidades localmente

---

## 🚀 Instalación y Ejecución

### 1) Clonar el repositorio
```bash
git clone https://github.com/diadasiachilensis/Bike-SQL-Python.git
cd Bike-SQL-Python
````

---

## 🧱 Paso A — Levantar DB de negocio con Terraform

> Esto crea el contenedor `custombikes_db_container` y la red `custombikes_data_network`.

```bash
cd infra
terraform init
terraform apply -auto-approve
```

### Verificación rápida

```bash
docker ps | grep custombikes_db_container
docker network ls | grep custombikes_data_network
```

### Ver tablas creadas (opcional)

```bash
docker exec -it custombikes_db_container psql -U custom_user -d custombike -c "\dt"
```

---

## 🌬️ Paso B — Levantar Airflow con Docker Compose

Vuelve a la raíz del repo:

```bash
cd ..
```

Crea el `.env` para permisos consistentes (recomendado):

```bash
echo "AIRFLOW_UID=50000" > .env
mkdir -p logs reports plugins
```

Inicializa Airflow (DB metadatos + usuario admin):

```bash
docker compose up airflow-init
```

Levanta todos los servicios:

```bash
docker compose up -d
docker compose ps
```

---

## 🖥️ Acceso a los Servicios

| Servicio              | URL Local               | Credenciales    | Descripción                                |
| --------------------- | ----------------------- | --------------- | ------------------------------------------ |
| **Airflow Webserver** | `http://localhost:8080` | `admin / admin` | UI para DAGs, logs, ejecuciones y métricas |

---

## 🧪 Ejecutar el Pipeline (DAG)

1. Entra a Airflow: `http://localhost:8080`
2. Busca el DAG: **`custombikes_reporte_automatizado`**
3. Actívalo (**Unpause**)
4. Ejecuta (**Trigger DAG**)

### Salida esperada

* Un archivo CSV generado en `./reports/` (host)
* Logs disponibles en la UI de Airflow por task

Verifica en tu máquina:

```bash
ls -l reports
```

---

## 📂 Estructura del Proyecto

```text
Bike-SQL-Python/
├── infra/
│   ├── main.tf                 # Terraform: red, imagen y contenedor Postgres (negocio)
│   └── variables.tf            # Variables Terraform
├── sql/
│   ├── 00_init_db.sql
│   ├── 01_personas.sql
│   └── ...                     # Scripts SQL (DDL/DML)
├── dags/
│   └── reportes_bike_dag.py    # DAG Airflow (verificación + reporte)
├── scripts/
│   └── etl_utils.py            # Utilidades Python (query + export)
├── docker-compose.yml          # Stack Airflow + Postgres metadatos
├── requirements.txt            # Dependencias Python (útil para ejecución local)
├── logs/                       # Logs (se ignoran, se conserva .gitkeep)
├── reports/                    # Outputs (se ignoran, se conserva .gitkeep)
└── README.md
```

---

## 🧹 Operación y Mantenimiento

**Ver logs:**

```bash
docker compose logs -f airflow-scheduler
docker compose logs -f airflow-webserver
```

**Detener stack Airflow:**

```bash
docker compose down
```

**Reset total Airflow (incluye volumen metadatos):**

```bash
docker compose down -v
```

**Destruir DB de negocio (Terraform):**

```bash
cd infra
terraform destroy -auto-approve
```

---

## 🔮 Roadmap

* [x] DB de negocio provisionada con Terraform (Docker provider)
* [x] Airflow contenerizado con Postgres de metadatos separado
* [x] DAG funcional que genera reportes a `./reports`
* [ ] Parametrización por `.env.example` (credenciales/hosts)
* [ ] Reportes versionados por fecha y partición
* [ ] Calidad de datos: validaciones y alertas
* [ ] Exportación a almacenamiento (S3/GCS) + notificación

---

Hecho con 💻 y ☕ en Chile.

