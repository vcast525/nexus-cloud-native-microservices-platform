# NEXUS Docker Infrastructure

## Overview

This directory contains the local Docker infrastructure configuration for the NEXUS Cloud-Native Microservices Platform.

The Docker environment will be expanded incrementally as NEXUS development progresses.

The current infrastructure implementation provides:

* PostgreSQL database container
* Environment-variable-based configuration
* Persistent PostgreSQL storage
* Automatic database schema initialization
* PostgreSQL health monitoring
* Dedicated Docker networking

Future development phases will add:

* Redis
* API Gateway
* Backend microservices
* Celery workers
* React frontend
* Prometheus
* Grafana
* Jaeger

---

## Current Docker Architecture

```text
LOCAL DEVELOPMENT MACHINE
        │
        │ localhost:5433
        ▼
DOCKER ENVIRONMENT
        │
        ▼
NEXUS NETWORK
        │
        ▼
POSTGRESQL CONTAINER
        │
        │ postgres:5432
        ▼
NEXUS DATABASE
        │
        ├── identity
        ├── registry
        ├── incidents
        ├── notifications
        ├── audit
        └── public
        │
        ▼
PERSISTENT DOCKER VOLUME
```

---

## Directory Structure

```text
infrastructure/
└── docker/
    ├── docker-compose.yml
    ├── README.md
    │
    └── postgres/
        └── init/
            └── 01-create-schemas.sql
```

---

## Infrastructure Components

### Docker Compose

The `docker-compose.yml` file defines the local NEXUS infrastructure.

The current configuration includes:

* PostgreSQL 16 Alpine
* Environment-variable configuration
* Port mapping
* Persistent storage
* Initialization scripts
* Health checks
* Docker networking

---

### PostgreSQL

PostgreSQL serves as the primary relational system of record for NEXUS.

The PostgreSQL container uses:

```text
Image: postgres:16-alpine

Container Name: nexus-postgres

Database Name: nexus

Internal Port: 5432

Local Development Port: 5433
```

The local host port uses `5433` because port `5432` was already in use on the development machine.

Application containers will communicate with PostgreSQL internally through:

```text
postgres:5432
```

Local development tools may communicate with PostgreSQL through:

```text
localhost:5433
```

---

## PostgreSQL Logical Schemas

NEXUS uses one PostgreSQL database containing multiple logical schemas.

```text
nexus
│
├── identity
├── registry
├── incidents
├── notifications
├── audit
└── public
```

### Identity Schema

```text
identity
```

Stores:

* Users
* Roles
* Authentication events
* Identity-related records

---

### Registry Schema

```text
registry
```

Stores:

* Registered services
* Support teams
* Environments
* Service-health records

---

### Incidents Schema

```text
incidents
```

Stores:

* Operational incidents
* Incident assignments
* Status history
* Resolution records

---

### Notifications Schema

```text
notifications
```

Stores:

* Notifications
* Processing status
* Retry attempts
* Delivery history

---

### Audit Schema

```text
audit
```

Stores:

* Application audit events
* Security-relevant activity
* Business-operation history

---

## Environment Configuration

The Docker Compose configuration uses environment variables.

The repository contains:

```text
.env.example
```

Developers create a local environment file:

```text
.env
```

The `.env` file must never be committed to GitHub.

The project `.gitignore` excludes local environment files.

---

## Create the Local Environment File

From the project root:

```text
cp .env.example .env
```

Review the local `.env` configuration before starting Docker infrastructure.

---

## PostgreSQL Port Configuration

The local environment currently uses:

```text
POSTGRES_HOST_PORT=5433
```

This maps:

```text
LOCAL MACHINE
localhost:5433
        │
        ▼
POSTGRESQL CONTAINER
postgres:5432
```

The PostgreSQL container continues using the standard internal port `5432`.

---

## Validate Docker Compose Configuration

Before starting the infrastructure, validate the Docker Compose configuration.

From the project root:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml config
```

A successful validation prints the resolved Docker Compose configuration.

Configuration errors must be corrected before starting the environment.

---

## Start PostgreSQL

From the project root:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml up -d postgres
```

The command:

* Creates the NEXUS Docker network
* Creates the PostgreSQL persistent volume when required
* Creates the PostgreSQL container
* Starts PostgreSQL
* Executes initialization scripts for a new database volume
* Begins PostgreSQL health monitoring

---

## Check Container Status

Run:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml ps
```

Expected PostgreSQL status:

```text
running (healthy)
```

The port mapping should show:

```text
0.0.0.0:5433->5432/tcp
```

---

## PostgreSQL Initialization

The PostgreSQL container automatically executes initialization scripts located in:

```text
infrastructure/docker/postgres/init/
```

The initial script is:

```text
01-create-schemas.sql
```

This script creates:

```text
identity
registry
incidents
notifications
audit
```

Initialization scripts execute only when PostgreSQL starts with an empty data directory.

If the persistent PostgreSQL volume already contains database data, the initialization scripts will not automatically execute again.

---

## Verify PostgreSQL Schemas

Run:

```text
docker exec -it nexus-postgres psql -U nexus_user -d nexus -c "\dn"
```

Expected schemas:

```text
audit
identity
incidents
notifications
public
registry
```

---

## PostgreSQL Health Check

The Docker Compose configuration uses:

```text
pg_isready
```

The health check verifies that PostgreSQL is ready to accept database connections.

The configured health-check behavior includes:

```text
Interval: 5 seconds

Timeout: 5 seconds

Retries: 10

Start Period: 10 seconds
```

A healthy container should display:

```text
running (healthy)
```

---

## Persistent Storage

PostgreSQL data is stored in the Docker volume:

```text
nexus-postgres-data
```

The volume is mounted inside the PostgreSQL container at:

```text
/var/lib/postgresql/data
```

This allows PostgreSQL data to survive normal container restarts and container replacement.

---

## Verify Database Persistence

Restart PostgreSQL:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml restart postgres
```

Check the container status:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml ps
```

Verify the schemas again:

```text
docker exec -it nexus-postgres psql -U nexus_user -d nexus -c "\dn"
```

The schemas should remain available after the restart.

---

## Stop PostgreSQL

Run:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml stop postgres
```

This stops the PostgreSQL container without removing the container or persistent volume.

---

## Start an Existing PostgreSQL Container

Run:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml start postgres
```

---

## Stop the Docker Compose Environment

Run:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml down
```

This removes Docker Compose containers and networks.

The named PostgreSQL volume remains available unless volume removal is explicitly requested.

---

## View PostgreSQL Logs

Run:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml logs postgres
```

Follow logs continuously:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml logs -f postgres
```

---

## Connect to PostgreSQL

Open an interactive PostgreSQL session:

```text
docker exec -it nexus-postgres psql -U nexus_user -d nexus
```

Exit the PostgreSQL session with:

```text
\q
```

---

## List Databases

From inside the PostgreSQL session:

```text
\l
```

---

## List Schemas

From inside the PostgreSQL session:

```text
\dn
```

---

## List Tables

From inside the PostgreSQL session:

```text
\dt
```

At the current development phase, application tables have not yet been created.

Tables will be added through service-specific ORM models and database migrations.

---

## Inspect Docker Volumes

List Docker volumes:

```text
docker volume ls
```

Inspect the NEXUS PostgreSQL volume:

```text
docker volume inspect nexus-postgres-data
```

---

## Inspect the Docker Network

Run:

```text
docker network inspect nexus-network
```

The NEXUS network will eventually support communication between:

* PostgreSQL
* Redis
* API Gateway
* Backend microservices
* Celery workers
* Monitoring services

---

## Troubleshooting

### Docker Daemon Is Not Running

Error:

```text
Cannot connect to the Docker daemon
```

Resolution:

Start Docker Desktop and wait for the Docker engine to become available.

Then rerun the Docker command.

---

### PostgreSQL Port Is Already in Use

Error:

```text
bind: address already in use
```

Cause:

Another process or container is already using local port `5432`.

NEXUS resolves this locally by using:

```text
POSTGRES_HOST_PORT=5433
```

The PostgreSQL container continues using internal port `5432`.

---

### PostgreSQL Container Name Conflict

Error:

```text
The container name "/nexus-postgres" is already in use
```

Inspect the existing container:

```text
docker ps -a --filter name=nexus-postgres
```

If the existing container is a failed or obsolete NEXUS container, remove it:

```text
docker rm -f nexus-postgres
```

Then start the environment again.

---

### PostgreSQL Container Is Unhealthy

Check status:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml ps
```

Read logs:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml logs postgres
```

Potential causes include:

* Incorrect database credentials
* Invalid environment variables
* Persistent volume problems
* PostgreSQL initialization errors

---

### Schemas Were Not Created

Verify schemas:

```text
docker exec -it nexus-postgres psql -U nexus_user -d nexus -c "\dn"
```

If the schemas are missing, inspect PostgreSQL logs.

Remember:

> PostgreSQL initialization scripts run only when the database data directory is empty.

An existing volume may prevent a newly added initialization script from executing automatically.

---

## Complete Environment Reset

A complete reset deletes the PostgreSQL container and persistent database data.

This action is destructive.

Stop the environment and remove volumes:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml down -v
```

The next startup will create a new database volume and rerun PostgreSQL initialization scripts.

Start PostgreSQL again:

```text
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml up -d postgres
```

Use complete resets only when intentionally recreating the local database.

---

## Security Considerations

The local PostgreSQL infrastructure follows these practices:

* Database configuration uses environment variables
* Local `.env` files are excluded from Git
* Example configuration contains development placeholders
* PostgreSQL uses a dedicated application user
* Persistent data remains outside the container filesystem
* PostgreSQL will remain internally accessible in future container environments
* Production secrets are not stored in the repository

The current fallback values in Docker Compose are intended only for local development.

Future Kubernetes deployments will use Kubernetes Secrets.

---

## Current Infrastructure Status

The PostgreSQL infrastructure has been validated successfully.

Completed validation includes:

```text
✓ Docker Compose configuration validated

✓ PostgreSQL image downloaded

✓ NEXUS Docker network created

✓ PostgreSQL persistent volume created

✓ PostgreSQL container started

✓ PostgreSQL health check passed

✓ NEXUS database created

✓ Identity schema created

✓ Registry schema created

✓ Incidents schema created

✓ Notifications schema created

✓ Audit schema created

✓ Database schema validation completed

✓ Container restart completed

✓ Database persistence validated
```

---

## Next Development Stage

The PostgreSQL infrastructure provides the database foundation required for future NEXUS development.

Subsequent development work will introduce:

```text
POSTGRESQL INFRASTRUCTURE
        │
        ▼
DATABASE CONNECTION UTILITIES
        │
        ▼
SQLALCHEMY CONFIGURATION
        │
        ▼
ALEMBIC MIGRATIONS
        │
        ▼
SERVICE-SPECIFIC MODELS
        │
        ▼
SYNTHETIC SEED DATA
        │
        ▼
DATABASE TESTING
```

The PostgreSQL database infrastructure is now ready to support the NEXUS microservices platform.