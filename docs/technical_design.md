Monday, July 13, 2026 — 11:26 AM ET

# Technical Design Document

## Technical Design Overview

This document defines the concrete engineering design for the NEXUS Cloud-Native Microservices Platform.

The requirements document explains what the platform must accomplish.

The architecture document explains how the major system components work together.

This technical design document defines:

* The selected technologies
* The final service boundaries
* The responsibility of each service
* The application directory structure
* The API conventions
* The initial endpoint design
* The relational data model
* The Redis messaging design
* The authentication and authorization approach
* The frontend application structure
* The health-monitoring process
* The notification-processing workflow
* The observability implementation
* The Docker configuration
* The Kubernetes resource design
* The testing tools
* The CI/CD workflow
* The dependency strategy
* The development sequence

NEXUS will be built as a visible full-stack application supported by a cloud-native microservices architecture.

The project will use a controlled number of services so that the architecture remains realistic, understandable, and achievable within a portfolio-development timeline.

---

## Product Definition

NEXUS is an internal service operations platform that allows authorized technology teams to:

* Authenticate securely
* View platform health
* Register internal software services
* Assign service owners and support teams
* Review service environments and versions
* Monitor service-health status
* Run manual health checks
* Review service-health history
* Create operational incidents
* Assign incidents
* Change incident priority and status
* Resolve incidents
* Review notification-processing history
* Manage users and roles
* Review operational metrics
* Observe microservice health
* Demonstrate Kubernetes scaling and recovery

The visible application will be implemented with React.

The backend will be separated into independently deployable services.

---

## Final Technology Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Frontend | React | User-facing application |
| Frontend Build Tool | Vite | Fast React development and production builds |
| Frontend Language | JavaScript | React component and application logic |
| Frontend Routing | React Router | Page navigation and protected routes |
| Frontend HTTP Client | Axios | API communication |
| Frontend Charts | Recharts | Health and operational charts |
| API Gateway | Node.js and Express | Centralized request routing |
| Identity Service | Python and FastAPI | Authentication, users, roles, and tokens |
| Service Registry | Node.js and Express | Service inventory and service metadata |
| Incident Service | Python and FastAPI | Incident lifecycle management |
| Notification Service | Python | Asynchronous notification processing |
| Health Worker | Python | Scheduled and manual health checks |
| Relational Database | PostgreSQL | Persistent application data |
| Python ORM | SQLAlchemy | Database interaction for Python services |
| Python Migrations | Alembic | Database schema migration management |
| Node ORM | Prisma | Database interaction for Node.js services |
| Cache and Queue | Redis | Task coordination, caching, and retry state |
| Python Task Queue | Celery | Notification and health background jobs |
| Authentication | JWT | Stateless authentication tokens |
| Password Hashing | bcrypt through Passlib | Secure password storage |
| Metrics | Prometheus | Application and infrastructure metrics |
| Monitoring Dashboard | Grafana | Metrics visualization |
| Distributed Tracing | OpenTelemetry and Jaeger | Cross-service request tracing |
| Local Containers | Docker | Component containerization |
| Local Orchestration | Docker Compose | Multi-container local environment |
| Cloud-Native Orchestration | Kubernetes | Deployments, Services, probes, and scaling |
| Local Kubernetes | Docker Desktop Kubernetes | Free local Kubernetes cluster |
| Backend Testing | Pytest | Python unit and integration testing |
| Node Testing | Vitest or Jest | Node.js unit testing |
| Frontend Testing | Vitest and React Testing Library | React component testing |
| End-to-End Testing | Playwright | User workflow automation |
| API Contract Testing | Schemathesis or custom contract tests | OpenAPI contract validation |
| Python Formatting | Black | Consistent Python formatting |
| Python Linting | Ruff | Fast Python linting |
| Node Formatting | Prettier | JavaScript formatting |
| Node Linting | ESLint | JavaScript linting |
| CI/CD | GitHub Actions | Automated testing, builds, and validation |
| Dependency Scanning | Dependabot and package audit tools | Dependency risk detection |
| Secret Scanning | Gitleaks | Accidental secret detection |
| Container Scanning | Trivy | Docker image security scanning |

---

## Technology Selection Rationale

### React

React is selected because NEXUS requires a polished, interactive, and component-driven user interface.

React supports:

* Reusable dashboard components
* Role-aware navigation
* Dynamic service-health updates
* Incident forms
* Notification cards
* Search and filtering
* Data visualization
* Protected routes
* Future application expansion

---

### Vite

Vite provides:

* Fast frontend startup
* Simple React configuration
* Fast development refresh
* Production build support
* Straightforward environment-variable configuration

---

### Node.js and Express

Node.js and Express will be used for:

* The API Gateway
* The Service Registry Service

This decision demonstrates a polyglot backend architecture.

Node.js is appropriate for:

* Lightweight request routing
* JSON-heavy API communication
* Gateway middleware
* Service inventory APIs
* Asynchronous network operations
* JavaScript-based backend development

---

### Python and FastAPI

FastAPI will be used for:

* The Identity Service
* The Incident Service

Python will also be used for:

* The Notification Worker
* The Health Monitoring Worker

FastAPI provides:

* Pydantic validation
* Automatic OpenAPI documentation
* Asynchronous endpoint support
* Dependency injection
* Clear authentication patterns
* Strong typing
* Fast development

---

### PostgreSQL

PostgreSQL is selected because the platform contains highly structured relational data.

Examples include:

* Users and roles
* Services and owners
* Incidents and assignments
* Notifications and attempts
* Health-check history
* Audit records

PostgreSQL supports:

* Foreign keys
* Unique constraints
* Transactions
* Indexes
* Relational queries
* Reliable persistence

---

### Redis

Redis is selected for:

* Celery task queueing
* Notification processing
* Health-check jobs
* Controlled retry tracking
* Short-lived caching
* Rate-limiting state
* Temporary coordination

Redis will not store the primary system of record.

---

### Docker and Kubernetes

Docker provides consistent local packaging.

Docker Compose allows the entire platform to run locally before Kubernetes is introduced.

Kubernetes provides visible demonstrations of:

* Container orchestration
* Service discovery
* Desired state
* Self-healing
* Replicas
* Liveness probes
* Readiness probes
* ConfigMaps
* Secrets
* Ingress
* Horizontal scaling

---

## Final Microservice Design

NEXUS will contain six application components.

| Component | Technology | Primary Responsibility |
| --- | --- | --- |
| Frontend | React | User-facing application |
| API Gateway | Node.js and Express | Centralized routing and request middleware |
| Identity Service | FastAPI | Authentication, users, roles, and JWTs |
| Service Registry | Node.js and Express | Registered services, owners, environments, and health data |
| Incident Service | FastAPI | Incident lifecycle and incident history |
| Notification Worker | Python and Celery | Asynchronous notification processing |
| Health Worker | Python and Celery | Manual and scheduled service-health checks |

PostgreSQL, Redis, Prometheus, Grafana, and Jaeger are infrastructure components rather than business microservices.

---

## Service Boundary Principles

Each microservice will have:

* One primary business responsibility
* Its own source directory
* Its own dependency file
* Its own Dockerfile
* Its own health endpoint
* Its own tests
* Its own configuration module
* Its own logs
* Its own metrics
* A defined database schema or table ownership
* Documented request and response contracts

Services will not directly modify tables owned by another service.

Services will communicate through:

* REST APIs
* Redis-backed asynchronous tasks
* Shared identifiers
* Documented contracts

---

## Repository Structure

The repository will evolve into the following structure:

```text
nexus-cloud-native-microservices-platform/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── security-scan.yml
│       └── container-build.yml
│
├── docs/
│   ├── images/
│   ├── architecture.md
│   ├── deployment_strategy.md
│   ├── requirements.md
│   ├── roadmap.md
│   ├── security_design.md
│   ├── technical_design.md
│   ├── testing_strategy.md
│   └── user_experience_flow.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
│
├── infrastructure/
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   └── docker-compose.observability.yml
│   │
│   ├── kubernetes/
│   │   ├── base/
│   │   ├── config/
│   │   ├── deployments/
│   │   ├── services/
│   │   ├── ingress/
│   │   ├── storage/
│   │   └── observability/
│   │
│   └── monitoring/
│       ├── prometheus/
│       ├── grafana/
│       └── jaeger/
│
├── scripts/
│   ├── seed_demo_data.py
│   ├── wait_for_services.py
│   ├── run_health_demo.py
│   └── kubernetes_recovery_demo.md
│
├── services/
│   ├── api_gateway/
│   ├── identity_service/
│   ├── service_registry/
│   ├── incident_service/
│   ├── notification_worker/
│   └── health_worker/
│
├── tests/
│   ├── contract/
│   ├── end_to_end/
│   ├── integration/
│   └── fixtures/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## API Gateway Technical Design

### Technology

* Node.js
* Express
* Axios
* Helmet
* CORS
* Morgan or Pino
* Express Rate Limit
* OpenTelemetry instrumentation

### Responsibilities

The API Gateway will:

* Receive all frontend API requests
* Route requests to the correct service
* Apply request correlation identifiers
* Forward JWT authentication headers
* Apply rate limiting
* Apply secure HTTP headers
* Record structured request logs
* Normalize gateway-level errors
* Aggregate dashboard information
* Expose gateway health information
* Provide a stable frontend API base URL

### Gateway Directory Structure

```text
services/api_gateway/
│
├── src/
│   ├── config/
│   │   └── environment.js
│   ├── middleware/
│   │   ├── correlationId.js
│   │   ├── errorHandler.js
│   │   ├── logger.js
│   │   ├── rateLimiter.js
│   │   └── security.js
│   ├── routes/
│   │   ├── authRoutes.js
│   │   ├── dashboardRoutes.js
│   │   ├── incidentRoutes.js
│   │   ├── notificationRoutes.js
│   │   ├── serviceRoutes.js
│   │   └── userRoutes.js
│   ├── services/
│   │   ├── identityClient.js
│   │   ├── incidentClient.js
│   │   ├── notificationClient.js
│   │   └── registryClient.js
│   ├── telemetry/
│   │   ├── metrics.js
│   │   └── tracing.js
│   ├── app.js
│   └── server.js
│
├── tests/
├── Dockerfile
├── package.json
└── package-lock.json
```

### Gateway Ports

| Environment | Port |
| --- | --- |
| Local host | 8080 |
| Container | 8080 |
| Kubernetes Service | 8080 |

### Gateway Health Endpoints

* `GET /health`
* `GET /ready`
* `GET /metrics`

### Gateway Routing Table

| Frontend Route | Downstream Service |
| --- | --- |
| `/api/v1/auth/*` | Identity Service |
| `/api/v1/users/*` | Identity Service |
| `/api/v1/services/*` | Service Registry |
| `/api/v1/health-checks/*` | Service Registry or Health Worker |
| `/api/v1/incidents/*` | Incident Service |
| `/api/v1/notifications/*` | Notification Service API or records endpoint |
| `/api/v1/dashboard/*` | Gateway aggregation |

---

## Identity Service Technical Design

### Technology

* Python
* FastAPI
* SQLAlchemy
* Alembic
* Pydantic
* PostgreSQL
* Passlib
* bcrypt
* python-jose
* Pytest
* Prometheus client
* OpenTelemetry

### Responsibilities

The Identity Service will manage:

* User accounts
* User roles
* Login
* Password hashing
* JWT generation
* JWT verification support
* Current-user profile
* User activation
* User deactivation
* Role assignment
* Authentication audit events

### Directory Structure

```text
services/identity_service/
│
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── health.py
│   │       └── users.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   └── telemetry.py
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   ├── models/
│   │   ├── audit_event.py
│   │   ├── role.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── role_repository.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── role.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── user_service.py
│   └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
├── alembic.ini
├── Dockerfile
└── requirements.txt
```

### Identity Service Port

| Environment | Port |
| --- | --- |
| Local host | 8001 |
| Container | 8001 |
| Kubernetes Service | 8001 |

---

## Identity API Endpoints

### Authentication Endpoints

| Method | Endpoint | Purpose | Authentication |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/login` | Authenticate user | Public |
| POST | `/api/v1/auth/refresh` | Refresh approved token | Authenticated |
| GET | `/api/v1/auth/me` | Retrieve current user | Authenticated |
| POST | `/api/v1/auth/logout` | Record logout event | Authenticated |

### User Endpoints

| Method | Endpoint | Purpose | Required Role |
| --- | --- | --- | --- |
| GET | `/api/v1/users` | Retrieve users | Administrator |
| POST | `/api/v1/users` | Create user | Administrator |
| GET | `/api/v1/users/{user_id}` | Retrieve user | Administrator |
| PATCH | `/api/v1/users/{user_id}` | Update user | Administrator |
| PATCH | `/api/v1/users/{user_id}/role` | Assign role | Administrator |
| PATCH | `/api/v1/users/{user_id}/status` | Activate or deactivate | Administrator |

---

## JWT Technical Design

### Token Claims

JWT payloads may contain:

```text
sub
username
role
iat
exp
jti
```

### Token Lifetime

The initial access-token lifetime will be:

* 30 minutes for the primary access token

A future refresh-token implementation may be added if required.

### JWT Secret Handling

The signing secret will be supplied through:

* `.env` during local development
* Docker Compose environment configuration
* Kubernetes Secret during Kubernetes deployment

The secret will not be stored in GitHub.

### Authorization Header

Protected requests will use:

```text
Authorization: Bearer <token>
```

---

## Password Security Design

Passwords will:

* Never be stored as plain text
* Be hashed with bcrypt
* Be validated against minimum complexity rules
* Never be written to logs
* Never be returned through API responses
* Never be included in audit-change details

The platform will store:

* Password hash
* Password update timestamp
* User activation status

---

## Service Registry Technical Design

### Technology

* Node.js
* Express
* Prisma
* PostgreSQL
* Axios
* Zod
* Pino
* Prometheus client
* OpenTelemetry
* Vitest or Jest

### Responsibilities

The Service Registry will manage:

* Service records
* Service ownership
* Support teams
* Deployment environments
* Service versions
* Health endpoints
* Current health status
* Health history
* Service search
* Service filters
* Service deactivation
* Service-related audit events

### Directory Structure

```text
services/service_registry/
│
├── prisma/
│   ├── migrations/
│   └── schema.prisma
│
├── src/
│   ├── config/
│   │   └── environment.js
│   ├── controllers/
│   │   ├── healthCheckController.js
│   │   └── serviceController.js
│   ├── middleware/
│   │   ├── auth.js
│   │   ├── errorHandler.js
│   │   └── validation.js
│   ├── repositories/
│   │   ├── healthRepository.js
│   │   └── serviceRepository.js
│   ├── routes/
│   │   ├── healthCheckRoutes.js
│   │   ├── healthRoutes.js
│   │   └── serviceRoutes.js
│   ├── schemas/
│   │   └── serviceSchemas.js
│   ├── services/
│   │   ├── healthService.js
│   │   └── registryService.js
│   ├── telemetry/
│   │   ├── metrics.js
│   │   └── tracing.js
│   ├── app.js
│   └── server.js
│
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
├── package.json
└── package-lock.json
```

### Service Registry Port

| Environment | Port |
| --- | --- |
| Local host | 8002 |
| Container | 8002 |
| Kubernetes Service | 8002 |

---

## Service Registry API Endpoints

| Method | Endpoint | Purpose | Minimum Role |
| --- | --- | --- | --- |
| GET | `/api/v1/services` | Retrieve services | Viewer |
| POST | `/api/v1/services` | Register service | Service Owner |
| GET | `/api/v1/services/{service_id}` | Retrieve service details | Viewer |
| PATCH | `/api/v1/services/{service_id}` | Update service | Service Owner |
| PATCH | `/api/v1/services/{service_id}/status` | Update operational status | Operations Analyst |
| DELETE | `/api/v1/services/{service_id}` | Deactivate service | Administrator |
| GET | `/api/v1/services/{service_id}/health` | Retrieve latest health | Viewer |
| GET | `/api/v1/services/{service_id}/health/history` | Retrieve health history | Viewer |
| POST | `/api/v1/services/{service_id}/health-check` | Run manual health check | Operations Analyst |
| GET | `/health` | Service health | Public internal |
| GET | `/ready` | Service readiness | Public internal |
| GET | `/metrics` | Prometheus metrics | Internal |

---

## Service Search and Filtering Design

The service inventory will support query parameters.

Example:

```text
GET /api/v1/services?search=risk&environment=production&status=degraded&page=1&page_size=20
```

Supported filters may include:

* Search text
* Environment
* Operational status
* Owner
* Support team
* Business capability
* Active status

The response will include:

* Service records
* Current page
* Page size
* Total records
* Total pages
* Applied filters

---

## Incident Service Technical Design

### Technology

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Pydantic
* Redis client
* Celery client
* Pytest
* Prometheus client
* OpenTelemetry

### Responsibilities

The Incident Service will manage:

* Incident creation
* Incident priority
* Incident assignment
* Incident status
* Incident updates
* Resolution
* Closure
* Incident history
* Incident search
* Incident filtering
* Incident audit events
* Notification-event submission

### Directory Structure

```text
services/incident_service/
│
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── health.py
│   │       └── incidents.py
│   ├── clients/
│   │   └── registry_client.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── telemetry.py
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   ├── models/
│   │   ├── incident.py
│   │   └── incident_history.py
│   ├── repositories/
│   │   └── incident_repository.py
│   ├── schemas/
│   │   └── incident.py
│   ├── services/
│   │   ├── incident_service.py
│   │   └── notification_publisher.py
│   └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
├── alembic.ini
├── Dockerfile
└── requirements.txt
```

### Incident Service Port

| Environment | Port |
| --- | --- |
| Local host | 8003 |
| Container | 8003 |
| Kubernetes Service | 8003 |

---

## Incident API Endpoints

| Method | Endpoint | Purpose | Minimum Role |
| --- | --- | --- | --- |
| GET | `/api/v1/incidents` | Retrieve incidents | Viewer |
| POST | `/api/v1/incidents` | Create incident | Operations Analyst |
| GET | `/api/v1/incidents/{incident_id}` | Retrieve incident | Viewer |
| PATCH | `/api/v1/incidents/{incident_id}` | Update incident | Operations Analyst |
| PATCH | `/api/v1/incidents/{incident_id}/assign` | Assign incident | Operations Analyst |
| PATCH | `/api/v1/incidents/{incident_id}/status` | Change status | Operations Analyst |
| POST | `/api/v1/incidents/{incident_id}/resolve` | Resolve incident | Operations Analyst |
| POST | `/api/v1/incidents/{incident_id}/close` | Close incident | Service Owner |
| GET | `/api/v1/incidents/{incident_id}/history` | Retrieve timeline | Viewer |
| GET | `/health` | Service health | Public internal |
| GET | `/ready` | Service readiness | Public internal |
| GET | `/metrics` | Prometheus metrics | Internal |

---

## Incident State Transition Design

Allowed status transitions will be controlled.

```text
OPEN
  │
  ▼
INVESTIGATING
  │
  ├──────────────► MITIGATED
  │                   │
  │                   ▼
  └──────────────► RESOLVED
                      │
                      ▼
                    CLOSED
```

The system will reject invalid transitions.

Examples of invalid transitions:

* Closed directly from Open
* Investigating after Closed
* Resolved without a resolution summary
* Closed without a resolved timestamp

---

## Incident Priority Design

Supported priorities:

| Priority | Meaning |
| --- | --- |
| Critical | Major outage or severe business impact |
| High | Significant degradation or urgent operational risk |
| Medium | Limited impact requiring planned response |
| Low | Minor issue or informational follow-up |

Priority changes will generate:

* Incident-history records
* Audit events
* Notifications where configured

---

## Notification Worker Technical Design

### Technology

* Python
* Celery
* Redis
* SQLAlchemy
* PostgreSQL
* Pydantic
* Pytest
* Prometheus client
* OpenTelemetry

### Responsibilities

The Notification Worker will:

* Receive queued notification tasks
* Validate notification payloads
* Create pending notification records
* Simulate notification delivery
* Record processing results
* Retry temporary failures
* Record final failure state
* Expose metrics
* Generate structured logs

### Directory Structure

```text
services/notification_worker/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── telemetry.py
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── notification.py
│   │   └── notification_attempt.py
│   ├── schemas/
│   │   └── notification.py
│   ├── services/
│   │   └── notification_service.py
│   ├── tasks/
│   │   └── notification_tasks.py
│   └── worker.py
│
├── tests/
├── Dockerfile
└── requirements.txt
```

---

## Notification Event Schema

A notification task may contain:

```text
event_id
event_type
source_service
resource_type
resource_id
severity
title
message
recipient_role
recipient_team
correlation_id
created_at
```

Supported event types may include:

* `incident.created`
* `incident.assigned`
* `incident.priority_changed`
* `incident.resolved`
* `service.degraded`
* `service.unavailable`
* `service.recovered`

---

## Notification Retry Strategy

Celery retry configuration will include:

* Maximum retry count
* Retry delay
* Exponential backoff where practical
* Final failed state
* Attempt history
* Structured error logging

Example behavior:

```text
Attempt 1
   │
   ├── Success → SENT
   │
   └── Failure
          │
          ▼
       Retry delay
          │
          ▼
Attempt 2
   │
   ├── Success → SENT
   │
   └── Failure
          │
          ▼
Attempt 3
   │
   ├── Success → SENT
   │
   └── Failure → FAILED
```

---

## Notification API Design

The initial notification retrieval endpoints may be exposed through the Incident Service, Service Registry, or a lightweight notification API.

The preferred design is to include a small FastAPI retrieval application within the notification component.

| Method | Endpoint | Purpose | Minimum Role |
| --- | --- | --- | --- |
| GET | `/api/v1/notifications` | Retrieve notifications | Viewer |
| GET | `/api/v1/notifications/{notification_id}` | Retrieve notification | Viewer |
| POST | `/api/v1/notifications/{notification_id}/retry` | Retry failure | Operations Analyst |
| PATCH | `/api/v1/notifications/{notification_id}/read` | Mark as read | Viewer |
| GET | `/health` | Service health | Public internal |
| GET | `/ready` | Service readiness | Public internal |
| GET | `/metrics` | Prometheus metrics | Internal |

The notification component may therefore contain:

* A Celery worker
* A lightweight FastAPI API
* Shared models and repositories

---

## Health Worker Technical Design

### Technology

* Python
* Celery
* Redis
* HTTPX
* SQLAlchemy
* PostgreSQL
* Pytest
* Prometheus client
* OpenTelemetry

### Responsibilities

The Health Worker will:

* Execute manual health-check tasks
* Execute scheduled health-check tasks
* Request registered service endpoints
* Measure response duration
* Record HTTP status
* Detect timeouts
* Determine platform health classification
* Store health history
* Update current service status
* Generate Redis notification events
* Record metrics
* Produce structured logs

### Directory Structure

```text
services/health_worker/
│
├── app/
│   ├── clients/
│   │   └── registry_client.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── telemetry.py
│   ├── schemas/
│   │   └── health_check.py
│   ├── services/
│   │   └── health_check_service.py
│   ├── tasks/
│   │   └── health_tasks.py
│   └── worker.py
│
├── tests/
├── Dockerfile
└── requirements.txt
```

---

## Health Classification Logic

Initial health classification:

| Result | Platform Status |
| --- | --- |
| HTTP 200 and response within threshold | Healthy |
| HTTP 200 and response above threshold | Degraded |
| HTTP 500-series response | Unavailable |
| Connection refused | Unavailable |
| Timeout | Unavailable |
| Invalid endpoint configuration | Unknown |
| Health check disabled | Maintenance or Unknown |

Initial response-time thresholds may be:

| Response Time | Classification |
| --- | --- |
| Less than 500 milliseconds | Healthy |
| 500 to 1,500 milliseconds | Degraded |
| Greater than 1,500 milliseconds | Degraded |
| Timeout | Unavailable |

Thresholds should be configurable.

---

## Health-Check Data Flow

```text
MANUAL OR SCHEDULED REQUEST
             │
             ▼
         REDIS QUEUE
             │
             ▼
        HEALTH WORKER
             │
             ├── Retrieve service configuration
             ├── Request health endpoint
             ├── Measure response time
             ├── Determine status
             └── Store result
             │
             ▼
        POSTGRESQL
             │
             ├───────────────┐
             │               │
             ▼               ▼
   DASHBOARD DISPLAY   STATUS-CHANGE EVENT
                             │
                             ▼
                    NOTIFICATION WORKER
```

---

## PostgreSQL Technical Design

### Database Strategy

NEXUS will use one PostgreSQL instance during local development.

Services will maintain logical ownership through separate schemas.

Proposed schemas:

```text
identity
registry
incidents
notifications
audit
```

This design reduces local resource usage while preserving service ownership.

---

## Identity Data Model

### Roles Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| name | VARCHAR | Unique and required |
| description | TEXT | Optional |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

### Users Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| username | VARCHAR | Unique and required |
| email | VARCHAR | Unique and required |
| password_hash | VARCHAR | Required |
| first_name | VARCHAR | Required |
| last_name | VARCHAR | Required |
| role_id | UUID | Foreign key to role |
| is_active | BOOLEAN | Required |
| last_login_at | TIMESTAMP | Optional |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

### Authentication Events Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| user_id | UUID | Optional foreign key |
| event_type | VARCHAR | Required |
| result | VARCHAR | Required |
| ip_address | VARCHAR | Optional |
| correlation_id | VARCHAR | Optional |
| created_at | TIMESTAMP | Required |

---

## Service Registry Data Model

### Teams Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| name | VARCHAR | Unique and required |
| description | TEXT | Optional |
| contact_email | VARCHAR | Optional |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

### Registered Services Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| service_code | VARCHAR | Unique and required |
| name | VARCHAR | Unique and required |
| description | TEXT | Required |
| service_type | VARCHAR | Required |
| business_capability | VARCHAR | Optional |
| owner_user_id | UUID | Optional shared identifier |
| support_team_id | UUID | Foreign key |
| environment | VARCHAR | Required |
| version | VARCHAR | Required |
| repository_url | VARCHAR | Optional |
| documentation_url | VARCHAR | Optional |
| health_endpoint | VARCHAR | Optional |
| operational_status | VARCHAR | Required |
| is_active | BOOLEAN | Required |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

### Service Health History Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| service_id | UUID | Foreign key |
| health_status | VARCHAR | Required |
| http_status | INTEGER | Optional |
| response_time_ms | INTEGER | Optional |
| error_message | TEXT | Optional |
| checked_at | TIMESTAMP | Required |
| correlation_id | VARCHAR | Optional |

---

## Incident Data Model

### Incidents Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| incident_code | VARCHAR | Unique and required |
| title | VARCHAR | Required |
| description | TEXT | Required |
| service_id | UUID | Required shared identifier |
| environment | VARCHAR | Required |
| priority | VARCHAR | Required |
| status | VARCHAR | Required |
| assigned_user_id | UUID | Optional |
| assigned_team_id | UUID | Optional |
| reported_by_user_id | UUID | Required |
| resolution_summary | TEXT | Optional |
| resolved_at | TIMESTAMP | Optional |
| closed_at | TIMESTAMP | Optional |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

### Incident History Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| incident_id | UUID | Foreign key |
| action | VARCHAR | Required |
| previous_value | JSONB | Optional |
| new_value | JSONB | Optional |
| changed_by_user_id | UUID | Required |
| correlation_id | VARCHAR | Optional |
| created_at | TIMESTAMP | Required |

---

## Notification Data Model

### Notifications Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| event_id | UUID | Unique and required |
| event_type | VARCHAR | Required |
| source_service | VARCHAR | Required |
| resource_type | VARCHAR | Required |
| resource_id | UUID | Required |
| severity | VARCHAR | Required |
| title | VARCHAR | Required |
| message | TEXT | Required |
| recipient_role | VARCHAR | Optional |
| recipient_team_id | UUID | Optional |
| status | VARCHAR | Required |
| is_read | BOOLEAN | Required |
| correlation_id | VARCHAR | Optional |
| created_at | TIMESTAMP | Required |
| processed_at | TIMESTAMP | Optional |

### Notification Attempts Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| notification_id | UUID | Foreign key |
| attempt_number | INTEGER | Required |
| result | VARCHAR | Required |
| error_message | TEXT | Optional |
| attempted_at | TIMESTAMP | Required |

---

## Audit Data Model

### Audit Events Table

| Column | Type | Constraints |
| --- | --- | --- |
| id | UUID | Primary key |
| event_type | VARCHAR | Required |
| source_service | VARCHAR | Required |
| user_id | UUID | Optional |
| resource_type | VARCHAR | Required |
| resource_id | UUID | Optional |
| action | VARCHAR | Required |
| result | VARCHAR | Required |
| change_summary | JSONB | Optional |
| correlation_id | VARCHAR | Optional |
| created_at | TIMESTAMP | Required |

---

## Database Indexing Strategy

Indexes will be created for frequently queried fields.

Examples include:

* User username
* User email
* User role
* Service name
* Service code
* Service environment
* Service status
* Service support team
* Health service identifier
* Health checked timestamp
* Incident code
* Incident status
* Incident priority
* Incident service identifier
* Incident assigned user
* Incident created timestamp
* Notification status
* Notification event type
* Notification created timestamp
* Audit correlation identifier
* Audit created timestamp

---

## Database Migration Strategy

Python services will use Alembic.

Node.js services will use Prisma migrations.

Migration files will:

* Be committed to GitHub
* Be reviewed with application changes
* Run before dependent services start
* Avoid destructive changes without documentation
* Support reproducible local setup

A root migration script may coordinate service migrations.

---

## Redis Technical Design

### Redis Responsibilities

Redis will provide:

* Celery broker
* Celery result backend where required
* Health-check task queue
* Notification task queue
* Retry coordination
* Gateway rate-limit storage
* Optional short-lived dashboard caching

### Proposed Queue Names

```text
notifications
health_checks
default
```

### Redis Key Examples

```text
rate_limit:{client_id}
dashboard_cache:overview
health_check_lock:{service_id}
notification_retry:{notification_id}
```

### Cache Expiration

Dashboard cache values may expire after:

* 15 to 30 seconds

Health-check locks may expire after:

* 30 to 60 seconds

Rate-limit keys will expire according to the configured request window.

---

## API Design Standards

### Base Route

```text
/api/v1
```

### Resource Naming

Routes will use:

* Lowercase names
* Plural resource nouns
* Hyphen-separated words only where required
* Stable identifiers
* Query parameters for filtering

Examples:

```text
/api/v1/services
/api/v1/incidents
/api/v1/notifications
/api/v1/users
```

---

## Standard Success Response

Logical response structure:

```json
{
  "success": true,
  "message": "Service retrieved successfully.",
  "data": {},
  "meta": {},
  "correlation_id": "example-correlation-id",
  "timestamp": "2026-07-13T15:26:00Z"
}
```

---

## Standard Error Response

```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested service was not found.",
    "details": []
  },
  "correlation_id": "example-correlation-id",
  "timestamp": "2026-07-13T15:26:00Z"
}
```

---

## HTTP Status Standards

| Status | Use |
| --- | --- |
| 200 | Successful retrieval or update |
| 201 | Successful resource creation |
| 202 | Asynchronous task accepted |
| 204 | Successful operation with no response body |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Insufficient permission |
| 404 | Resource not found |
| 409 | Duplicate or conflicting state |
| 422 | Validation failure |
| 429 | Rate limit exceeded |
| 500 | Unexpected internal error |
| 502 | Downstream service failure |
| 503 | Service unavailable |
| 504 | Downstream timeout |

---

## Pagination Standard

Collection endpoints will support:

```text
page
page_size
sort_by
sort_order
```

Default values:

```text
page=1
page_size=20
sort_order=desc
```

Maximum page size:

```text
100
```

---

## Correlation Identifier Design

The API Gateway will:

1. Read `X-Correlation-ID` if provided
2. Generate a UUID if missing
3. Add the identifier to downstream requests
4. Return the identifier in the response
5. Include the identifier in structured logs
6. Include the identifier in audit records
7. Include the identifier in notification events

Header:

```text
X-Correlation-ID
```

---

## Frontend Technical Design

### Technology

* React
* Vite
* React Router
* Axios
* Recharts
* React Context
* Vitest
* React Testing Library
* Playwright

### Frontend Pages

| Page | Purpose |
| --- | --- |
| Login | Authenticate user |
| Dashboard | Display platform overview |
| Services | Display service inventory |
| Service Detail | Display one service and health history |
| Register Service | Create service |
| Incidents | Display incident inventory |
| Incident Detail | Review and update incident |
| Create Incident | Create operational incident |
| Notifications | Review notification history |
| Monitoring | Display platform metrics |
| Users | Administrative user management |
| Profile | Display authenticated-user information |
| Unauthorized | Explain restricted access |
| Not Found | Handle invalid routes |

---

## Frontend Directory Structure

```text
frontend/src/
│
├── api/
│   ├── apiClient.js
│   ├── authApi.js
│   ├── dashboardApi.js
│   ├── incidentApi.js
│   ├── notificationApi.js
│   ├── serviceApi.js
│   └── userApi.js
│
├── assets/
│
├── components/
│   ├── common/
│   ├── dashboard/
│   ├── incidents/
│   ├── monitoring/
│   ├── notifications/
│   ├── services/
│   └── users/
│
├── context/
│   ├── AuthContext.jsx
│   └── NotificationContext.jsx
│
├── hooks/
│   ├── useAuth.js
│   ├── useIncidents.js
│   ├── useNotifications.js
│   └── useServices.js
│
├── layouts/
│   ├── AppLayout.jsx
│   └── AuthLayout.jsx
│
├── pages/
│   ├── DashboardPage.jsx
│   ├── IncidentDetailPage.jsx
│   ├── IncidentsPage.jsx
│   ├── LoginPage.jsx
│   ├── MonitoringPage.jsx
│   ├── NotificationsPage.jsx
│   ├── RegisterServicePage.jsx
│   ├── ServiceDetailPage.jsx
│   ├── ServicesPage.jsx
│   ├── UnauthorizedPage.jsx
│   ├── UserAdministrationPage.jsx
│   └── UserProfilePage.jsx
│
├── routes/
│   ├── AppRoutes.jsx
│   └── ProtectedRoute.jsx
│
├── services/
│   ├── authStorage.js
│   └── permissions.js
│
├── styles/
│   ├── components.css
│   ├── global.css
│   ├── layout.css
│   └── variables.css
│
├── utils/
│   ├── dateFormat.js
│   ├── errorMessages.js
│   └── statusLabels.js
│
├── App.jsx
└── main.jsx
```

---

## Frontend State Design

Global state will remain limited.

React Context will manage:

* Authenticated user
* JWT session state
* Assigned role
* Logout
* Global notification count

Page-level state will manage:

* Loading state
* Form state
* Search text
* Filters
* Selected records
* API errors
* Success messages
* Pagination

A larger state-management library will not be introduced unless the application becomes difficult to maintain.

---

## Protected Route Design

Protected routes will verify:

* User authentication
* Required role
* Active account status

Example route rules:

| Route | Allowed Roles |
| --- | --- |
| Dashboard | All authenticated roles |
| Services | All authenticated roles |
| Register Service | Administrator and Service Owner |
| Incidents | All authenticated roles |
| Create Incident | Administrator, Service Owner, Operations Analyst |
| Notifications | All authenticated roles |
| Monitoring | Administrator, Service Owner, Operations Analyst |
| Users | Administrator only |

Frontend route protection improves usability.

Backend authorization remains the security authority.

---

## Frontend Visual Components

Reusable components will include:

* Application sidebar
* Top navigation
* Metric card
* Service-status badge
* Incident-priority badge
* Incident-status badge
* Notification card
* Search input
* Filter control
* Data table
* Empty-state panel
* Error alert
* Success alert
* Loading spinner
* Confirmation dialog
* Health chart
* Incident timeline
* Role badge
* Pagination controls

---

## Dashboard Data Contract

The dashboard endpoint may return:

```json
{
  "services": {
    "total": 24,
    "healthy": 19,
    "degraded": 3,
    "unavailable": 2
  },
  "incidents": {
    "open": 4,
    "critical": 1
  },
  "recent_notifications": [],
  "recent_incidents": [],
  "service_health": []
}
```

The API Gateway may aggregate this response from multiple services.

---

## Frontend Error Handling

The frontend will distinguish:

* Validation errors
* Authentication errors
* Authorization errors
* Resource-not-found errors
* Downstream-service errors
* Network errors
* Unexpected errors

User messages will be understandable.

Technical details will remain in logs.

---

## Structured Logging Design

### Log Format

Services will produce JSON-formatted logs.

Recommended fields:

```text
timestamp
service
environment
level
event
correlation_id
method
path
status_code
duration_ms
user_id
resource_type
resource_id
error_type
error_message
```

### Sensitive Data Exclusions

Logs will never intentionally contain:

* Passwords
* Password hashes
* JWT values
* Signing secrets
* Database passwords
* Private keys
* Full authorization headers

---

## Metrics Design

Each application service will expose:

```text
GET /metrics
```

Metrics may include:

```text
http_requests_total
http_request_duration_seconds
http_errors_total
service_health_checks_total
service_health_check_failures_total
incidents_created_total
open_incidents_total
notifications_processed_total
notification_failures_total
celery_tasks_total
celery_task_failures_total
```

Metric labels may include:

* Service
* Route
* Method
* Status code
* Environment
* Incident priority
* Notification result

Labels must avoid user identifiers or high-cardinality values.

---

## Distributed Tracing Design

OpenTelemetry instrumentation will be added to:

* API Gateway
* Identity Service
* Service Registry
* Incident Service
* Notification Service
* Health Worker

Trace context will flow through:

```text
React Request
    │
    ▼
API Gateway
    │
    ▼
Backend Service
    │
    ├── PostgreSQL
    ├── Redis
    └── Downstream Service
```

Jaeger will display:

* Trace duration
* Service spans
* Downstream calls
* Error spans
* Request relationships

---

## Health Endpoint Design

Each HTTP service will expose:

### Liveness

```text
GET /health
```

Returns whether the process is alive.

### Readiness

```text
GET /ready
```

Checks required dependencies such as:

* PostgreSQL
* Redis where applicable
* Required configuration
* Service initialization

### Metrics

```text
GET /metrics
```

Exposes Prometheus metrics.

---

## Docker Technical Design

Each service will have its own Dockerfile.

Docker images will:

* Use small official base images
* Install only required dependencies
* Use non-root users where practical
* Avoid copying `.env`
* Expose only the application port
* Include health-check support
* Use deterministic dependency files
* Avoid development tools in production images where practical

---

## Docker Compose Services

The local environment will include:

```text
frontend
api-gateway
identity-service
service-registry
incident-service
notification-api
notification-worker
health-worker
postgres
redis
prometheus
grafana
jaeger
```

### Planned Local Ports

| Component | Host Port |
| --- | --- |
| React Frontend | 3000 |
| API Gateway | 8080 |
| Identity Service | 8001 |
| Service Registry | 8002 |
| Incident Service | 8003 |
| Notification API | 8004 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Prometheus | 9090 |
| Grafana | 3001 |
| Jaeger UI | 16686 |

Internal container communication will use service names rather than localhost.

Example:

```text
http://identity-service:8001
http://service-registry:8002
http://incident-service:8003
```

---

## Environment Variable Design

The root `.env.example` will document variables such as:

```text
APP_ENV=
LOG_LEVEL=

POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

REDIS_HOST=
REDIS_PORT=

JWT_SECRET=
JWT_ALGORITHM=
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=

IDENTITY_SERVICE_URL=
SERVICE_REGISTRY_URL=
INCIDENT_SERVICE_URL=
NOTIFICATION_SERVICE_URL=

VITE_API_BASE_URL=

PROMETHEUS_PORT=
OTEL_EXPORTER_OTLP_ENDPOINT=
```

Live values will exist only in local `.env` files or Kubernetes Secrets.

---

## Kubernetes Technical Design

### Namespace

NEXUS resources will use a dedicated namespace:

```text
nexus
```

### Resource Types

The Kubernetes deployment will include:

* Namespace
* ConfigMaps
* Secrets
* Deployments
* Services
* PersistentVolumeClaims
* Ingress
* Service Accounts where practical
* HorizontalPodAutoscaler where practical
* Prometheus configuration
* Grafana configuration
* Jaeger configuration

---

## Kubernetes Deployment Design

Stateless components will use Deployments.

Initial replica counts:

| Component | Initial Replicas |
| --- | --- |
| Frontend | 1 |
| API Gateway | 2 |
| Identity Service | 2 |
| Service Registry | 2 |
| Incident Service | 2 |
| Notification API | 1 |
| Notification Worker | 2 |
| Health Worker | 1 |

PostgreSQL and Redis will initially use one local instance each.

---

## Kubernetes Service Types

| Component | Service Type |
| --- | --- |
| Frontend | ClusterIP |
| API Gateway | ClusterIP |
| Identity Service | ClusterIP |
| Service Registry | ClusterIP |
| Incident Service | ClusterIP |
| Notification API | ClusterIP |
| PostgreSQL | ClusterIP |
| Redis | ClusterIP |
| Prometheus | ClusterIP |
| Grafana | ClusterIP |

Ingress will provide external access to the frontend and API Gateway.

---

## Kubernetes Ingress Routes

Proposed routes:

```text
/               → frontend-service
/api            → api-gateway-service
/grafana        → grafana-service
```

Prometheus and Jaeger may use port forwarding rather than public ingress exposure.

---

## Kubernetes Probe Design

### Liveness Probe

Example behavior:

```text
Path: /health
Initial delay: 20 seconds
Period: 10 seconds
Timeout: 3 seconds
Failure threshold: 3
```

### Readiness Probe

Example behavior:

```text
Path: /ready
Initial delay: 10 seconds
Period: 5 seconds
Timeout: 3 seconds
Failure threshold: 3
```

Exact values will be adjusted during implementation.

---

## Kubernetes Resource Requests and Limits

Initial example values:

```text
requests:
  cpu: 100m
  memory: 128Mi

limits:
  cpu: 500m
  memory: 512Mi
```

Observability components may require larger memory allocations.

Values will be adjusted to fit the local development machine.

---

## Horizontal Scaling Demonstration

The project will demonstrate manual scaling.

Example:

```text
kubectl scale deployment incident-service --replicas=3 -n nexus
```

The platform will then show:

* Three incident-service pods
* One stable Kubernetes Service
* Continued frontend functionality
* Metrics reflecting multiple instances

A HorizontalPodAutoscaler may be added if local metrics support is practical.

---

## Self-Healing Demonstration

The project will intentionally delete a pod.

Example:

```text
kubectl delete pod <incident-pod-name> -n nexus
```

Kubernetes will:

1. Detect the missing replica
2. Create a replacement pod
3. Run readiness checks
4. Add the new pod to the Service
5. Restore the desired replica count

This demonstration will be documented with screenshots.

---

## Testing Tool Design

### Python Services

Tools:

* Pytest
* pytest-asyncio
* HTTPX test client
* pytest-cov
* Testcontainers where practical

### Node.js Services

Tools:

* Vitest or Jest
* Supertest
* Prisma test database
* Mock Service Worker or Axios mocks where needed

### React Frontend

Tools:

* Vitest
* React Testing Library
* User Event
* Mock Service Worker

### End-to-End

Tool:

* Playwright

### Contract Testing

Tools may include:

* Schemathesis for FastAPI OpenAPI contracts
* Supertest contract assertions
* Shared JSON fixtures
* Gateway-to-service compatibility tests

---

## Unit Testing Targets

Unit tests will cover:

* Password verification
* JWT generation
* Authorization rules
* User activation rules
* Service validation
* Health classification
* Incident transition rules
* Incident resolution rules
* Notification retry logic
* API Gateway routing helpers
* Frontend permissions
* Data-formatting utilities

---

## Integration Testing Targets

Integration tests will cover:

* Identity Service and PostgreSQL
* Service Registry and PostgreSQL
* Incident Service and PostgreSQL
* Notification Worker and Redis
* Health Worker and Redis
* Gateway and downstream services
* Incident Service and Registry validation
* Incident event and Notification Worker
* Prometheus metric exposure

---

## End-to-End Testing Scenarios

Playwright will validate:

1. User login
2. Protected dashboard access
3. Service inventory display
4. Service registration
5. Service search
6. Manual health check
7. Incident creation
8. Incident assignment
9. Incident resolution
10. Notification display
11. Administrator user-management access
12. Viewer authorization restrictions
13. Logout

---

## CI Workflow Design

The main GitHub Actions workflow will include jobs for:

### Python Validation

* Set up Python
* Install dependencies
* Run Ruff
* Run Black validation
* Run Pytest
* Generate coverage result

### Node Validation

* Set up Node.js
* Install dependencies
* Run ESLint
* Run Prettier validation
* Run unit tests
* Build Node services

### Frontend Validation

* Install frontend dependencies
* Run frontend tests
* Build React application

### Contract Validation

* Validate selected API schemas
* Run gateway compatibility tests

### Docker Validation

* Build service images
* Validate Dockerfiles

### Security Validation

* Scan dependencies
* Scan repository for secrets
* Scan Docker images where practical

---

## GitHub Actions Trigger Design

The CI workflow will run on:

```text
pull_request
push to main
manual workflow dispatch
```

Container-build workflows may run on:

```text
push to main
version tags
manual workflow dispatch
```

---

## Security Tooling Design

### Gitleaks

Will scan for:

* Secrets
* Tokens
* Passwords
* Private keys
* Credentials

### Trivy

Will scan:

* Docker images
* Dependency vulnerabilities
* Misconfigurations where supported

### Dependabot

Will monitor:

* Python dependencies
* Node.js dependencies
* GitHub Actions versions

---

## Dependency Management

Each service will maintain its own dependencies.

Python services:

```text
requirements.txt
```

Node.js services:

```text
package.json
package-lock.json
```

The root `requirements.txt` will be used only for shared developer tooling or will remain minimal.

Dependencies will be pinned or bounded to improve reproducibility.

---

## Seed Data Design

A seed script will create synthetic demonstration data.

Seed data may include:

* Four user roles
* Several demonstration users
* Twenty-four registered services
* Multiple support teams
* Healthy services
* Degraded services
* Unavailable services
* Open incidents
* Resolved incidents
* Notification history
* Health-check history
* Audit events

No real employee or customer data will be used.

---

## Demonstration Services

The visible service inventory may include synthetic systems such as:

* Payment API
* Customer Identity Service
* Risk Analytics Engine
* Notification Service
* Transaction Monitoring Service
* Reporting Automation Service
* Document Processing Service
* Data Quality API
* Authentication Gateway
* Market Data Service
* Compliance Rules Engine
* Case Management API

These records represent systems monitored by NEXUS.

They do not need to be fully built as separate applications.

Selected demonstration endpoints may be simulated to produce:

* Healthy responses
* Slow responses
* Failed responses
* Recovery behavior

---

## Demonstration Health Endpoints

Small simulated health services may expose:

```text
/demo/healthy
/demo/degraded
/demo/unavailable
/demo/recovering
```

These endpoints will allow the Health Worker to demonstrate status changes without relying on external websites or paid services.

---

## Development Strategy

NEXUS will be developed in vertical slices.

A vertical slice connects:

```text
VISIBLE FRONTEND
      │
      ▼
API GATEWAY
      │
      ▼
BACKEND SERVICE
      │
      ▼
DATABASE OR REDIS
      │
      ▼
VISIBLE USER RESULT
```

This approach avoids building every backend component before anything is visible.

---

## Recommended Development Order

### Phase 1: Visible Frontend Foundation

Build:

* Application layout
* Sidebar
* Top navigation
* Dashboard mockup
* Service cards
* Incident cards
* Notification cards
* Monitoring mockup

Use static demonstration data first.

This gives an immediate visual product.

---

### Phase 2: API Gateway and Health Foundation

Build:

* API Gateway
* Gateway health endpoint
* Correlation identifier
* Structured gateway logs
* Frontend-to-gateway connectivity

---

### Phase 3: Identity Vertical Slice

Build:

* Identity database models
* User seed data
* Login endpoint
* JWT generation
* Protected routes
* Role-aware frontend navigation
* User profile

Visible result:

* Real login
* Role-specific interface

---

### Phase 4: Service Registry Vertical Slice

Build:

* Service data model
* Service API
* Service inventory page
* Service detail page
* Search and filters
* Register service form

Visible result:

* Real service records displayed from PostgreSQL

---

### Phase 5: Incident Vertical Slice

Build:

* Incident data model
* Incident API
* Incident list
* Incident detail
* Incident creation
* Incident assignment
* Incident resolution
* Incident timeline

Visible result:

* Full incident workflow

---

### Phase 6: Redis and Notifications

Build:

* Redis
* Celery
* Notification event publishing
* Notification processing
* Retry behavior
* Notification Center

Visible result:

* Incident actions create visible notifications

---

### Phase 7: Health Monitoring

Build:

* Health Worker
* Manual health check
* Scheduled checks
* Health history
* Health chart
* Health-change notifications

Visible result:

* Services visibly change between Healthy, Degraded, and Unavailable

---

### Phase 8: Observability

Build:

* Metrics endpoints
* Prometheus
* Grafana
* OpenTelemetry
* Jaeger
* Monitoring dashboards

Visible result:

* Request activity and service behavior appear in dashboards

---

### Phase 9: Automated Testing and CI

Build:

* Unit tests
* Integration tests
* Contract tests
* Playwright tests
* GitHub Actions
* Security scans

Visible result:

* GitHub workflow validates changes

---

### Phase 10: Kubernetes

Build:

* Namespace
* ConfigMaps
* Secrets
* Deployments
* Services
* Ingress
* Probes
* Replicas
* Recovery demonstration
* Scaling demonstration

Visible result:

* NEXUS runs in Kubernetes and recovers from pod deletion

---

## Technical Risks

### Risk: Excessive Local Resource Usage

Mitigation:

* Develop with only required services running
* Add observability later
* Use one PostgreSQL instance
* Use controlled replica counts
* Document minimum system requirements

### Risk: Too Many Services at Once

Mitigation:

* Build one vertical slice at a time
* Keep service responsibilities narrow
* Avoid adding optional services early

### Risk: Authentication Complexity

Mitigation:

* Start with access tokens only
* Use local users
* Use clear role rules
* Add refresh tokens only if needed

### Risk: Database Migration Conflicts

Mitigation:

* Use schema ownership
* Keep migration folders separate
* Run migrations through documented scripts
* Avoid cross-service table modification

### Risk: Frontend Waiting Too Long for Backend Completion

Mitigation:

* Build static frontend views first
* Replace mock data one page at a time
* Maintain visible progress throughout development

### Risk: Kubernetes Introduced Too Early

Mitigation:

* Complete Docker Compose implementation first
* Verify each service independently
* Add Kubernetes only after the application works locally

---

## Technical Decision Summary

NEXUS will use:

* React and Vite for the visible application
* Node.js and Express for the API Gateway
* FastAPI for identity and incident management
* Node.js and Express for the Service Registry
* Python and Celery for notifications and health checks
* PostgreSQL for persistent relational data
* Redis for asynchronous processing and caching
* JWT for authentication
* Role-based access control for authorization
* SQLAlchemy and Alembic for Python data access
* Prisma for Node.js data access
* Axios for HTTP communication
* Prometheus for metrics
* Grafana for monitoring
* OpenTelemetry and Jaeger for tracing
* Docker for service packaging
* Docker Compose for local orchestration
* Kubernetes for cloud-native deployment
* Pytest, Vitest, React Testing Library, and Playwright for testing
* GitHub Actions for CI/CD
* Gitleaks, Trivy, and Dependabot for security validation

---

## Final Technical Outcome

The completed NEXUS platform will be a professional, visible, full-stack cloud-native application.

The user will interact with:

* A secure login page
* A platform dashboard
* A service inventory
* Service-detail pages
* Health charts
* Incident-management pages
* Incident timelines
* A Notification Center
* A user-administration interface
* A monitoring dashboard

Those visible capabilities will be powered by:

* Multiple independently deployable services
* A Node.js API Gateway
* FastAPI services
* A Node.js service registry
* PostgreSQL
* Redis
* Celery workers
* JWT authentication
* Role-based authorization
* Structured logs
* Metrics
* Distributed traces
* Docker containers
* Kubernetes workloads
* Automated tests
* GitHub Actions
* Security scans

The project will demonstrate the complete engineering path:

```text
BUSINESS REQUIREMENT
        │
        ▼
VISIBLE USER EXPERIENCE
        │
        ▼
FRONTEND COMPONENT
        │
        ▼
API GATEWAY ROUTE
        │
        ▼
MICROSERVICE ENDPOINT
        │
        ▼
BUSINESS LOGIC
        │
        ▼
POSTGRESQL OR REDIS
        │
        ▼
LOGS, METRICS, AND TRACES
        │
        ▼
DOCKER CONTAINER
        │
        ▼
KUBERNETES WORKLOAD
        │
        ▼
AUTOMATED TESTING AND CI/CD
        │
        ▼
VISIBLE, WORKING CLOUD-NATIVE PLATFORM
```

This technical design provides the implementation blueprint for building NEXUS from the first visible React screen through the final Kubernetes deployment and operational demonstration.