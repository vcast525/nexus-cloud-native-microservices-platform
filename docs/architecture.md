Monday, July 13, 2026 — 11:22 AM ET

# System Architecture

## Architecture Overview

NEXUS is a cloud-native service operations platform designed as a modular microservices ecosystem.

The platform provides a visible, interactive React application where technology teams can:

* Monitor registered software services
* Review current service health
* View service ownership and environment information
* Create and manage operational incidents
* Review system notifications
* Monitor application performance
* Administer users and access roles
* Observe how cloud-native services operate behind the interface

The frontend experience is powered by independently deployable backend services, PostgreSQL, Redis, Docker, Kubernetes, automated testing, CI/CD, and centralized observability.

The architecture is designed to demonstrate:

* Full-stack application development
* Microservices architecture
* Polyglot backend development
* API gateway routing
* 
* Secure authentication
* Role-based authorization
* Service-to-service communication
* Relational data persistence
* Redis-backed asynchronous processing
* Docker containerization
* Kubernetes orchestration
* Centralized logging
* Metrics collection
* Distributed tracing
* Automated testing
* CI/CD
* Horizontal scaling
* Fault isolation
* Automated service recovery

The platform will initially run locally through Docker Compose and will later be deployed to a local Kubernetes environment.

---

## User-Facing Concept

The end user interacts with a centralized React dashboard called the NEXUS Cloud Operations Platform.

The dashboard provides a visual command center for monitoring internal software services and responding to operational problems.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   NEXUS                                               🔔 3     👤 Vincent    │
│   CLOUD OPERATIONS PLATFORM                                                  │
│                                                                              │
├───────────────────┬──────────────────────────────────────────────────────────┤
│                   │                                                          │
│  🏠 Dashboard     │  PLATFORM OVERVIEW                                       │
│                   │                                                          │
│  ◈ Services       │  ┌────────────┐ ┌────────────┐ ┌────────────┐            │
│                   │  │    24      │ │    19      │ │     3      │            │
│  ⚠ Incidents      │  │  SERVICES  │ │  HEALTHY   │ │  DEGRADED  │            │
│                   │  └────────────┘ └────────────┘ └────────────┘            │
│  🔔 Notifications │                                                          │
│                   │  ┌────────────┐ ┌────────────┐                           │
│  📊 Monitoring    │  │     2      │ │     4      │                           │
│                   │  │    DOWN    │ │ OPEN       │                           │
│  👥 Users         │  │            │ │ INCIDENTS  │                           │
│                   │  └────────────┘ └────────────┘                           │
│  ⚙ Settings       │                                                          │
│                   │  SERVICE HEALTH                                          │
│                   │                                                          │
│                   │  Payment API              ● HEALTHY        99.98%        │
│                   │  Customer Identity         ● HEALTHY        99.95%        │
│                   │  Risk Analytics Engine     ● DEGRADED       94.21%        │
│                   │  Notification Service      ● UNAVAILABLE     0.00%        │
│                   │                                                          │
│                   │  ─────────────────────────────────────────────────────   │
│                   │                                                          │
│                   │  ACTIVE INCIDENTS                                        │
│                   │                                                          │
│                   │  INC-1042   Notification Service   CRITICAL      OPEN     │
│                   │  INC-1041   Risk Analytics Engine  HIGH   INVESTIGATING  │
│                   │  INC-1038   Payment API            MEDIUM        OPEN     │
│                   │                                                          │
└───────────────────┴──────────────────────────────────────────────────────────┘
```

The dashboard gives users immediate visibility into:

* Total registered services
* Healthy services
* Degraded services
* Unavailable services
* Open incidents
* Critical incidents
* Recent notifications
* Recent operational activity
* Current service availability
* Platform health trends

The frontend converts the backend microservices architecture into something visible, understandable, and useful.

---

## Service Inventory Concept

The Services area allows users to review every application registered within NEXUS.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   NEXUS                                                     SERVICE INVENTORY│
│                                                                              │
├───────────────────┬──────────────────────────────────────────────────────────┤
│                   │                                                          │
│  🏠 Dashboard     │  REGISTERED SERVICES                 [+ REGISTER SERVICE] │
│                   │                                                          │
│  ◈ Services       │  Search services...     Environment ▼     Status ▼       │
│                   │                                                          │
│  ⚠ Incidents      │  ┌────────────────────────────────────────────────────┐  │
│                   │  │ PAYMENT API                              ● HEALTHY  │  │
│  🔔 Notifications │  │ Production                                         │  │
│                   │  │ Owner: Payments Technology                          │  │
│  📊 Monitoring    │  │ Version: 4.8.1                                     │  │
│                   │  │ Uptime: 99.98%                                      │  │
│  👥 Users         │  └────────────────────────────────────────────────────┘  │
│                   │                                                          │
│  ⚙ Settings       │  ┌────────────────────────────────────────────────────┐  │
│                   │  │ RISK ANALYTICS ENGINE                   ● DEGRADED │  │
│                   │  │ Production                                         │  │
│                   │  │ Owner: Risk Technology                              │  │
│                   │  │ Version: 3.4.2                                     │  │
│                   │  │ Uptime: 94.21%                                      │  │
│                   │  └────────────────────────────────────────────────────┘  │
│                   │                                                          │
│                   │  ┌────────────────────────────────────────────────────┐  │
│                   │  │ NOTIFICATION SERVICE                ● UNAVAILABLE │  │
│                   │  │ Production                                         │  │
│                   │  │ Owner: Platform Engineering                         │  │
│                   │  │ Version: 2.1.0                                     │  │
│                   │  │ Uptime: 0.00%                                       │  │
│                   │  └────────────────────────────────────────────────────┘  │
│                   │                                                          │
└───────────────────┴──────────────────────────────────────────────────────────┘
```

The Service Inventory connects visible frontend elements to backend capabilities.

| User-Facing Element | Backend Capability | What It Demonstrates |
| --- | --- | --- |
| Registered Services | Service Registry Service | Centralized service management |
| Service Owner | PostgreSQL service records | Clear operational ownership |
| Environment | Service metadata | Development, testing, staging, and production classification |
| Health Status | Health Monitoring Worker | Automated service checks |
| Version | Service Registry data | Deployment and release visibility |
| Uptime | Health history and metrics | Operational reliability tracking |
| Register Service | Service Registry API | Secure service creation workflow |
| Search and Filters | Query parameters and database filtering | Efficient service discovery |

---

## Service Detail Concept

Users can select a service to review its metadata, health history, current incidents, and operational controls.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   NEXUS                                      SERVICES / RISK ANALYTICS ENGINE │
│                                                                              │
├───────────────────┬──────────────────────────────────────────────────────────┤
│                   │                                                          │
│  🏠 Dashboard     │  RISK ANALYTICS ENGINE                  ● DEGRADED        │
│                   │                                                          │
│  ◈ Services       │  Service ID        SVC-1007                               │
│                   │  Owner             Risk Technology                        │
│  ⚠ Incidents      │  Environment       Production                             │
│                   │  Version           3.4.2                                  │
│  🔔 Notifications │  Health Endpoint   /health                                │
│                   │  Support Contact    risk-platform@example.com              │
│  📊 Monitoring    │                                                          │
│                   │  ─────────────────────────────────────────────────────   │
│  👥 Users         │                                                          │
│                   │  SERVICE HEALTH                                          │
│  ⚙ Settings       │                                                          │
│                   │  Availability                                            │
│                   │                                                          │
│                   │       100% ┤     ╭──────╮                                 │
│                   │        95% ┤─────╯      ╰────────                         │
│                   │        90% ┤                                              │
│                   │            └──────────────────────────                    │
│                   │             8AM   10AM   12PM   2PM                       │
│                   │                                                          │
│                   │  RESPONSE TIME                  284 ms                    │
│                   │  UPTIME                         94.21%                    │
│                   │  OPEN INCIDENTS                 2                         │
│                   │  LAST CHECK                     11:17 AM                  │
│                   │                                                          │
│                   │  [ RUN HEALTH CHECK ]   [ CREATE INCIDENT ]              │
│                   │                                                          │
└───────────────────┴──────────────────────────────────────────────────────────┘
```

The Service Detail page allows users to understand a service without reviewing source code, container logs, or Kubernetes configuration.

The page visually connects:

* Service metadata
* Service ownership
* Deployment environment
* Health status
* Response time
* Uptime
* Open incidents
* Health-check history
* Manual health-check actions
* Incident creation

---

## Incident Management Concept

The Incident Management area provides a centralized interface for operational issue tracking.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   NEXUS                                                INCIDENT MANAGEMENT    │
│                                                                              │
├───────────────────┬──────────────────────────────────────────────────────────┤
│                   │                                                          │
│  🏠 Dashboard     │  ACTIVE INCIDENTS                    [+ CREATE INCIDENT]  │
│                   │                                                          │
│  ◈ Services       │  Search incidents...        Status ▼    Priority ▼       │
│                   │                                                          │
│  ⚠ Incidents      │  ┌────────────────────────────────────────────────────┐  │
│                   │  │ INC-1042                                           │  │
│  🔔 Notifications │  │ Notification Service Unavailable                   │  │
│                   │  │                                                    │  │
│  📊 Monitoring    │  │ CRITICAL    OPEN                                   │  │
│                   │  │                                                    │  │
│  👥 Users         │  │ Assigned: Platform Engineering                     │  │
│                   │  │ Created: July 13, 2026                             │  │
│  ⚙ Settings       │  └────────────────────────────────────────────────────┘  │
│                   │                                                          │
│                   │  ┌────────────────────────────────────────────────────┐  │
│                   │  │ INC-1041                                           │  │
│                   │  │ Elevated Risk Analytics Response Times             │  │
│                   │  │                                                    │  │
│                   │  │ HIGH        INVESTIGATING                          │  │
│                   │  │                                                    │  │
│                   │  │ Assigned: Risk Technology                          │  │
│                   │  └────────────────────────────────────────────────────┘  │
│                   │                                                          │
└───────────────────┴──────────────────────────────────────────────────────────┘
```

Users can:

* Create incidents
* Search incidents
* Filter by status
* Filter by priority
* Filter by affected service
* Assign incidents
* Change incident status
* Add resolution information
* Review incident history
* View associated notifications

---

## Incident Detail Concept

The Incident Detail page provides the complete lifecycle of an operational issue.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   INCIDENT INC-1042                                      CRITICAL • OPEN      │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Notification Service Unavailable                                            │
│                                                                              │
│  Affected Service     Notification Service                                   │
│  Environment          Production                                             │
│  Assigned Team        Platform Engineering                                   │
│  Reported By          Operations Analyst                                     │
│  Created              July 13, 2026 — 10:42 AM                              │
│                                                                              │
│  DESCRIPTION                                                                 │
│                                                                              │
│  Health checks are failing and notification requests are not being           │
│  processed. The service has returned repeated connection errors.             │
│                                                                              │
│  INCIDENT TIMELINE                                                           │
│                                                                              │
│  10:42 AM   Incident created                        ●                         │
│  10:44 AM   Assigned to Platform Engineering       ●                         │
│  10:48 AM   Status changed to Investigating        ●                         │
│  11:03 AM   Notification retry initiated           ●                         │
│                                                                              │
│  Priority       [ Critical ▼ ]                                                │
│  Status         [ Open ▼ ]                                                    │
│  Assigned Team  [ Platform Engineering ▼ ]                                   │
│                                                                              │
│  [ SAVE CHANGES ]      [ RESOLVE INCIDENT ]                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

This screen demonstrates how database records, role-based authorization, audit events, notification processing, and service relationships become visible to the user.

---

## Notification Center Concept

The Notification Center displays events generated by service-health changes and incident workflows.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   NEXUS                                                 NOTIFICATION CENTER   │
│                                                                              │
├───────────────────┬──────────────────────────────────────────────────────────┤
│                   │                                                          │
│  🏠 Dashboard     │  RECENT NOTIFICATIONS                  Status ▼          │
│                   │                                                          │
│  ◈ Services       │  🔴 Service Unavailable                                  │
│                   │     Notification Service                                 │
│  ⚠ Incidents      │     Critical incident INC-1042 created                   │
│                   │     Status: Sent                     2 minutes ago        │
│  🔔 Notifications │                                                          │
│                   │  🟠 Service Degraded                                     │
│  📊 Monitoring    │     Risk Analytics Engine                                │
│                   │     Response time exceeded threshold                     │
│  👥 Users         │     Status: Sent                     18 minutes ago       │
│                   │                                                          │
│  ⚙ Settings       │  🟢 Service Recovered                                    │
│                   │     Payment API                                           │
│                   │     Health status returned to normal                     │
│                   │     Status: Sent                     42 minutes ago       │
│                   │                                                          │
│                   │  ⚠ Notification Failed                                   │
│                   │     Incident assignment notification                     │
│                   │     Status: Failed                   [ RETRY ]            │
│                   │                                                          │
└───────────────────┴──────────────────────────────────────────────────────────┘
```

The Notification Center allows users to observe asynchronous backend processing through visible status updates.

| Notification Status | Meaning |
| --- | --- |
| Pending | Notification has been created but not processed |
| Processing | Notification worker is handling the event |
| Sent | Simulated or in-application delivery completed |
| Failed | Notification processing failed |
| Retrying | Controlled retry is in progress |

---

## User Administration Concept

Platform Administrators will manage users and assigned roles through the React application.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   NEXUS                                                   USER ADMINISTRATION│
│                                                                              │
├───────────────────┬──────────────────────────────────────────────────────────┤
│                   │                                                          │
│  🏠 Dashboard     │  USERS                                [+ CREATE USER]     │
│                   │                                                          │
│  ◈ Services       │  Search users...                      Role ▼              │
│                   │                                                          │
│  ⚠ Incidents      │  Vincent Castillo                                       │
│                   │  vincent@example.com                                     │
│  🔔 Notifications │  Platform Administrator        ACTIVE                   │
│                   │                                                          │
│  📊 Monitoring    │  Jordan Lee                                              │
│                   │  jordan.lee@example.com                                  │
│  👥 Users         │  Service Owner                  ACTIVE                   │
│                   │                                                          │
│  ⚙ Settings       │  Morgan Davis                                            │
│                   │  morgan.davis@example.com                                │
│                   │  Operations Analyst             ACTIVE                   │
│                   │                                                          │
│                   │  Taylor Smith                                            │
│                   │  taylor.smith@example.com                                │
│                   │  Viewer                         INACTIVE                 │
│                   │                                                          │
└───────────────────┴──────────────────────────────────────────────────────────┘
```

The User Administration interface demonstrates:

* Authentication
* Authorization
* Role assignment
* Account activation
* Account deactivation
* Protected administrative routes
* User audit events

---

## Monitoring Dashboard Concept

NEXUS will include a visible monitoring experience powered by Prometheus and Grafana.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   NEXUS PLATFORM MONITORING                                                  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  REQUEST RATE                     ERROR RATE                                 │
│                                                                              │
│  1,250 requests/min               1.8%                                       │
│                                                                              │
│       ╭───╮       ╭────╮                ╭╮                                   │
│  ─────╯   ╰───────╯    ╰────       ─────╯╰────────                          │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  AVERAGE RESPONSE TIME            ACTIVE SERVICE INSTANCES                   │
│                                                                              │
│  284 ms                           API Gateway             3 pods              │
│                                   Identity Service        2 pods              │
│                                   Service Registry        2 pods              │
│                                   Incident Service        3 pods              │
│                                   Notification Service    2 pods              │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SERVICE AVAILABILITY                                                        │
│                                                                              │
│  Payment API                 99.98%                                           │
│  Customer Identity          99.95%                                           │
│  Risk Analytics Engine      94.21%                                           │
│  Notification Service        0.00%                                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

This monitoring experience allows users and recruiters to see that observability is not merely configuration hidden in the repository.

The monitoring dashboard may display:

* Request counts
* Error rates
* Response times
* Service availability
* Active Kubernetes replicas
* Container restarts
* Incident activity
* Notification-processing results
* Health-check failures

---

## User-Facing Operational Flow

The user-facing operational flow connects visible actions to backend processing.

```text
USER OPENS NEXUS
        │
        ▼
LOGIN SCREEN
        │
        ▼
IDENTITY SERVICE VALIDATES USER
        │
        ▼
ROLE-AWARE DASHBOARD
        │
        ├───────────────┬────────────────┬────────────────┐
        │               │                │                │
        ▼               ▼                ▼                ▼
 VIEW SERVICES    VIEW INCIDENTS   VIEW NOTIFICATIONS  VIEW MONITORING
        │               │                │                │
        ▼               ▼                ▼                ▼
 SERVICE DETAIL   INCIDENT DETAIL  PROCESSING STATUS  METRICS & HEALTH
        │               │
        ├───────────────┘
        │
        ▼
 RUN HEALTH CHECK OR CREATE INCIDENT
        │
        ▼
 BACKEND SERVICES PROCESS REQUEST
        │
        ▼
 POSTGRESQL / REDIS UPDATED
        │
        ▼
 DASHBOARD REFRESHES
        │
        ▼
 USER SEES RESULT
```

The goal is not only to build backend services.

The goal is to make every important backend capability visible through the application.

---

## Architecture Goals

The NEXUS architecture is designed to achieve the following goals:

* Separate business capabilities into clear service boundaries
* Provide a polished and visible user experience
* Allow services to be developed and deployed independently
* Protect application functionality through authentication and authorization
* Maintain clear ownership of data and responsibilities
* Support reliable service-to-service communication
* Prevent failures in one component from unnecessarily affecting the entire platform
* Provide visibility into service health and platform behavior
* Support automated testing at multiple levels
* Support containerized local development
* Support Kubernetes orchestration
* Demonstrate horizontal scaling
* Demonstrate service recovery
* Remain understandable and manageable as a portfolio project
* Avoid unnecessary dependency on paid cloud services

---

## High-Level Architecture

The high-level architecture connects the user-facing React application to the backend microservices and data platforms.

```text
                              USER
                                │
                                ▼
                    ┌─────────────────────┐
                    │                     │
                    │   REACT FRONTEND    │
                    │                     │
                    │  Dashboard          │
                    │  Services           │
                    │  Incidents          │
                    │  Notifications      │
                    │  Monitoring         │
                    │  User Management    │
                    │                     │
                    └──────────┬──────────┘
                               │
                               │ REST API REQUESTS
                               ▼
                    ┌─────────────────────┐
                    │                     │
                    │    API GATEWAY      │
                    │      NODE.JS        │
                    │                     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┬────────────────┐
              │                │                │                │
              ▼                ▼                ▼                ▼
     ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
     │                │ │                │ │                │ │                │
     │    IDENTITY    │ │    SERVICE     │ │    INCIDENT    │ │  NOTIFICATION  │
     │    SERVICE     │ │    REGISTRY    │ │    SERVICE     │ │    SERVICE     │
     │                │ │                │ │                │ │                │
     │    FastAPI     │ │    Node.js     │ │    FastAPI     │ │ Python/Node.js │
     │                │ │                │ │                │ │                │
     └────────┬───────┘ └────────┬───────┘ └────────┬───────┘ └────────┬───────┘
              │                  │                  │                  │
              └──────────────────┴─────────┬────────┴──────────────────┘
                                           │
                              ┌────────────┴────────────┐
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐      ┌──────────────────┐
                    │                  │      │                  │
                    │    POSTGRESQL    │      │      REDIS       │
                    │                  │      │                  │
                    └──────────────────┘      └──────────────────┘
```

The user interacts with the React frontend.

The frontend communicates only with the API Gateway.

The API Gateway routes requests to the appropriate backend service.

The backend services own separate business capabilities.

PostgreSQL stores persistent business records.

Redis supports asynchronous notification and health-monitoring workflows.

---

## Complete System Architecture

```text
                            BUSINESS PROBLEM
                                   │
                                   ▼
                         BUSINESS REQUIREMENTS
                                   │
                                   ▼
                         USER-FACING CAPABILITIES
                                   │
                                   ▼
                         ┌───────────────────┐
                         │                   │
                         │  REACT FRONTEND   │
                         │                   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │                   │
                         │   API GATEWAY     │
                         │     NODE.JS       │
                         │                   │
                         └─────────┬─────────┘
                                   │
             ┌─────────────────────┼──────────────────────┐
             │                     │                      │
             ▼                     ▼                      ▼
     ┌───────────────┐    ┌─────────────────┐    ┌─────────────────┐
     │               │    │                 │    │                 │
     │   IDENTITY    │    │ SERVICE REGISTRY│    │ INCIDENT SERVICE│
     │   SERVICE     │    │                 │    │                 │
     │               │    │                 │    │                 │
     └───────┬───────┘    └────────┬────────┘    └────────┬────────┘
             │                     │                      │
             │                     ▼                      │
             │            ┌─────────────────┐             │
             │            │                 │             │
             │            │ HEALTH MONITOR  │             │
             │            │     WORKER      │             │
             │            │                 │             │
             │            └────────┬────────┘             │
             │                     │                      │
             └─────────────────────┼──────────────────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │                   │
                         │    POSTGRESQL     │
                         │                   │
                         └───────────────────┘

                      INCIDENT AND HEALTH EVENTS
                                   │
                                   ▼
                         ┌───────────────────┐
                         │                   │
                         │       REDIS       │
                         │                   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │                   │
                         │   NOTIFICATION    │
                         │     SERVICE       │
                         │                   │
                         └───────────────────┘

                       APPLICATION TELEMETRY
                                   │
                   ┌───────────────┼───────────────┐
                   │               │               │
                   ▼               ▼               ▼
              STRUCTURED        METRICS          TRACES
                LOGS               │               │
                                   ▼               ▼
                         ┌───────────────────┐
                         │                   │
                         │    PROMETHEUS     │
                         │     GRAFANA       │
                         │      JAEGER       │
                         │                   │
                         └───────────────────┘

                      COMPLETE PLATFORM RUNS IN
                                   │
                                   ▼
                         ┌───────────────────┐
                         │                   │
                         │    KUBERNETES     │
                         │                   │
                         │  Deployments      │
                         │  Pods             │
                         │  Services         │
                         │  ConfigMaps       │
                         │  Secrets          │
                         │  Ingress          │
                         │  Health Probes    │
                         │  Replicas         │
                         │                   │
                         └───────────────────┘
```

The architecture contains five primary workflows:

1. User authentication and authorization
2. Service registration and health monitoring
3. Incident creation and lifecycle management
4. Notification generation and background processing
5. Metrics, logging, tracing, and platform monitoring

---

## Core Platform Components

### React Frontend

The React frontend provides the primary user-facing interface for NEXUS.

Frontend responsibilities include:

* Display the login interface
* Provide role-aware navigation
* Display dashboard summary metrics
* Display the service inventory
* Display individual service details
* Support service registration
* Display service-health history
* Support manual health checks
* Display incidents
* Support incident creation
* Support incident assignment
* Support incident resolution
* Display notifications
* Display monitoring information
* Support user administration
* Provide search and filtering
* Display loading indicators
* Display success messages
* Display error messages
* Display empty-state messaging

The frontend will not directly access PostgreSQL, Redis, or internal microservice containers.

---

### API Gateway

The API Gateway provides a centralized entry point for frontend requests.

The gateway will be implemented using Node.js and Express.

The API Gateway will be responsible for:

* Receiving frontend API requests
* Routing requests to the correct backend service
* Applying consistent API versioning
* Propagating authentication tokens
* Assigning or forwarding correlation identifiers
* Recording structured request logs
* Returning standardized error responses
* Supporting cross-origin configuration
* Providing a stable frontend integration point

Example routing behavior:

* `/api/v1/auth/*` → Identity Service
* `/api/v1/users/*` → Identity Service
* `/api/v1/services/*` → Service Registry Service
* `/api/v1/incidents/*` → Incident Service
* `/api/v1/notifications/*` → Notification Service
* `/api/v1/dashboard/*` → Aggregated platform information

The API Gateway will not contain the primary business logic.

---

### Identity Service

The Identity Service will be implemented using FastAPI.

The Identity Service will be responsible for:

* User authentication
* Password verification
* Secure password hashing
* JSON Web Token generation
* Token validation
* User profile retrieval
* User administration
* Role assignment
* Account activation
* Account deactivation
* Authentication audit events

Primary identity entities may include:

* User
* Role
* UserRole
* AuthenticationEvent

---

### Service Registry Service

The Service Registry Service will manage the internal software-service inventory.

The service will be implemented using Node.js or FastAPI as confirmed during technical design.

Responsibilities include:

* Service registration
* Service metadata management
* Service ownership
* Support-team assignment
* Environment classification
* Service status
* Service search
* Service filtering
* Service deactivation
* Health-check configuration
* Service-detail retrieval
* Service audit events

Primary entities may include:

* RegisteredService
* ServiceOwner
* SupportTeam
* Environment
* ServiceStatus
* ServiceHealthCheck
* ServiceHealthHistory

---

### Incident Service

The Incident Service will be implemented using FastAPI.

Responsibilities include:

* Incident creation
* Incident prioritization
* Incident status management
* Incident assignment
* Incident updates
* Incident resolution
* Incident closure
* Incident search
* Incident filtering
* Incident history
* Incident audit events
* Notification-event generation

Primary entities may include:

* Incident
* IncidentStatus
* IncidentPriority
* IncidentAssignment
* IncidentHistory
* IncidentResolution

---

### Notification Service

The Notification Service will operate as an independent backend capability.

Responsibilities include:

* Receiving operational notification events
* Processing notification requests
* Maintaining notification history
* Recording processing status
* Handling controlled retries
* Recording failures
* Supporting in-application notifications
* Simulating external delivery channels

Notification events may be generated when:

* A critical incident is created
* An incident is assigned
* An incident priority changes
* An incident is resolved
* A service becomes degraded
* A service becomes unavailable
* A service recovers

---

### Health Monitoring Worker

The Health Monitoring Worker will evaluate configured service-health endpoints.

Responsibilities include:

* Reading registered health-check configurations
* Sending health-check requests
* Measuring response time
* Recording HTTP response information
* Determining service health
* Persisting health history
* Triggering degradation events
* Triggering recovery events
* Supporting manual health checks
* Supporting scheduled health checks

The worker may operate as:

* A background Python process
* A Redis-backed task worker
* A dedicated Docker container
* A Kubernetes Deployment
* A Kubernetes CronJob

---

## Data and Messaging Architecture

### PostgreSQL

PostgreSQL will provide persistent relational storage for core application data.

Possible database organization includes:

* Identity schema
* Service Registry schema
* Incident schema
* Notification schema
* Audit schema

PostgreSQL will store:

* Users
* Roles
* Registered services
* Owners
* Teams
* Environments
* Health results
* Incidents
* Incident history
* Notifications
* Audit events

Each microservice will own its assigned data.

A service should not directly modify another service’s tables.

---

### Redis

Redis will support fast, temporary, and asynchronous platform operations.

Redis may be used for:

* Notification queueing
* Background task queueing
* Short-lived caching
* Rate limiting
* Health-check scheduling
* Retry tracking
* Temporary coordination

Redis will not be the primary system of record.

---

## Authentication Flow

```text
USER
  │
  ▼
REACT LOGIN SCREEN
  │
  ▼
API GATEWAY
  │
  ▼
IDENTITY SERVICE
  │
  ├── Validate username
  ├── Verify password hash
  ├── Retrieve assigned role
  └── Generate JWT
  │
  ▼
API GATEWAY
  │
  ▼
REACT FRONTEND
  │
  ▼
ROLE-AWARE DASHBOARD
```

The authentication flow will be:

1. User enters credentials
2. Frontend sends credentials to the API Gateway
3. API Gateway routes the request to the Identity Service
4. Identity Service retrieves the user
5. Identity Service verifies the password hash
6. Identity Service retrieves the assigned role
7. Identity Service issues a JSON Web Token
8. Frontend stores approved session information
9. Frontend includes the token in protected requests
10. Backend services validate the token
11. Role permissions are applied

Frontend visibility alone will not be considered sufficient security.

Backend services will enforce authorization.

---

## Service Registration Flow

```text
AUTHORIZED USER
      │
      ▼
REGISTER SERVICE FORM
      │
      ▼
REACT FRONTEND
      │
      ▼
API GATEWAY
      │
      ▼
SERVICE REGISTRY SERVICE
      │
      ├── Validate request
      ├── Check authorization
      ├── Create service record
      ├── Assign owner and environment
      └── Record audit event
      │
      ▼
POSTGRESQL
      │
      ▼
UPDATED SERVICE INVENTORY
```

---

## Service Health Flow

```text
REGISTERED SERVICE
      │
      ▼
HEALTH MONITORING WORKER
      │
      ├── Request /health endpoint
      ├── Measure response time
      ├── Capture HTTP status
      └── Determine service status
      │
      ▼
POSTGRESQL HEALTH HISTORY
      │
      ├───────────────┐
      │               │
      ▼               ▼
DASHBOARD UPDATE   REDIS EVENT
                      │
                      ▼
              NOTIFICATION SERVICE
```

The health workflow will be:

1. A service contains a configured health endpoint
2. The worker sends a health-check request
3. Response status and response time are captured
4. A health result is created
5. Health history is stored
6. Current service status is updated
7. The dashboard displays the new status
8. Significant changes generate notification events
9. Metrics and logs record the operation

---

## Incident Creation Flow

```text
AUTHORIZED USER
      │
      ▼
CREATE INCIDENT FORM
      │
      ▼
API GATEWAY
      │
      ▼
INCIDENT SERVICE
      │
      ├── Validate request
      ├── Validate affected service
      ├── Create incident
      ├── Create history record
      ├── Record audit event
      └── Create notification event
      │
      ├─────────────────────┐
      ▼                     ▼
POSTGRESQL                REDIS
                              │
                              ▼
                    NOTIFICATION SERVICE
                              │
                              ▼
                  IN-APPLICATION NOTIFICATION
```

---

## Notification Processing Flow

```text
BUSINESS EVENT
      │
      ▼
REDIS QUEUE
      │
      ▼
NOTIFICATION SERVICE
      │
      ├── Create pending record
      ├── Process notification
      ├── Simulate delivery
      └── Record result
      │
      ├───────────────┐
      │               │
      ▼               ▼
    SENT            FAILED
                      │
                      ▼
               CONTROLLED RETRY
```

---

## Dashboard Aggregation Architecture

The dashboard displays information from several backend services.

Dashboard metrics may include:

* Total services
* Healthy services
* Degraded services
* Unavailable services
* Open incidents
* Critical incidents
* Recent notifications
* Recent activity

The initial implementation may use API Gateway aggregation.

```text
REACT DASHBOARD
      │
      ▼
API GATEWAY
      │
      ├──────────────► SERVICE REGISTRY
      │
      ├──────────────► INCIDENT SERVICE
      │
      └──────────────► NOTIFICATION SERVICE
      │
      ▼
AGGREGATED DASHBOARD RESPONSE
      │
      ▼
REACT DASHBOARD CARDS
```

A future version may introduce a dedicated Dashboard Service.

---

## Observability Architecture

NEXUS will include:

1. Structured logs
2. Metrics
3. Distributed traces

```text
APPLICATION SERVICES
        │
        ├───────────────┬────────────────┐
        │               │                │
        ▼               ▼                ▼
 STRUCTURED LOGS      METRICS          TRACES
        │               │                │
        │               ▼                ▼
        │          PROMETHEUS          JAEGER
        │               │                │
        │               └────────┬───────┘
        │                        ▼
        └───────────────────► GRAFANA
```

### Structured Logging

Recommended fields include:

* Timestamp
* Service name
* Environment
* Log level
* Event name
* Correlation identifier
* Request method
* Request path
* HTTP status
* Response time
* User identifier when appropriate
* Error type
* Error message

Logs will not expose:

* Passwords
* Authentication tokens
* Private keys
* Database credentials
* Sensitive personal information

---

### Metrics

Prometheus may collect:

* Request counts
* Request duration
* Error counts
* Health-check counts
* Health-check failures
* Incident creation counts
* Open incident counts
* Notification-processing counts
* Notification failures
* Container availability
* Restart counts
* Replica counts

---

### Distributed Tracing

Distributed tracing will allow one request to be followed through:

```text
REACT FRONTEND
      │
      ▼
API GATEWAY
      │
      ▼
BACKEND SERVICE
      │
      ▼
POSTGRESQL OR REDIS
      │
      ▼
DOWNSTREAM SERVICE
```

A correlation identifier will be generated or forwarded through each stage.

OpenTelemetry-compatible tooling may be used.

---

## Docker Architecture

Each major component will operate in its own Docker container.

Planned containers include:

* React frontend
* API Gateway
* Identity Service
* Service Registry Service
* Incident Service
* Notification Service
* Health Monitoring Worker
* PostgreSQL
* Redis
* Prometheus
* Grafana
* Tracing component

```text
DOCKER COMPOSE
      │
      ├── frontend
      ├── api-gateway
      ├── identity-service
      ├── service-registry
      ├── incident-service
      ├── notification-service
      ├── health-worker
      ├── postgres
      ├── redis
      ├── prometheus
      ├── grafana
      └── tracing
```

Docker Compose will manage:

* Container startup
* Networking
* Environment configuration
* Port mapping
* Volumes
* Health checks
* Service dependencies
* Local observability

---

## Kubernetes Architecture

The platform will later run inside a local Kubernetes cluster.

Possible local Kubernetes options include:

* Docker Desktop Kubernetes
* Kind
* Minikube

The selected option must be:

* Free
* Compatible with the development environment
* Reproducible
* Appropriate for portfolio demonstration

```text
                         KUBERNETES CLUSTER
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  INGRESS                                                                     │
│     │                                                                        │
│     ├──────────────► FRONTEND SERVICE                                        │
│     │                       │                                                │
│     │                       ▼                                                │
│     │                FRONTEND PODS                                           │
│     │                                                                        │
│     └──────────────► API GATEWAY SERVICE                                     │
│                             │                                                │
│                             ▼                                                │
│                     API GATEWAY PODS                                         │
│                             │                                                │
│             ┌───────────────┼─────────────────┐                              │
│             │               │                 │                              │
│             ▼               ▼                 ▼                              │
│       IDENTITY SERVICE  REGISTRY SERVICE  INCIDENT SERVICE                   │
│             │               │                 │                              │
│             ▼               ▼                 ▼                              │
│       IDENTITY PODS    REGISTRY PODS    INCIDENT PODS                        │
│                                                                              │
│                     NOTIFICATION SERVICE                                     │
│                             │                                                │
│                             ▼                                                │
│                     NOTIFICATION PODS                                        │
│                                                                              │
│         POSTGRESQL       REDIS       PROMETHEUS       GRAFANA                 │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Kubernetes Components

### Deployments

Stateless services will run through Kubernetes Deployments.

Planned Deployments may include:

* Frontend Deployment
* API Gateway Deployment
* Identity Service Deployment
* Service Registry Deployment
* Incident Service Deployment
* Notification Service Deployment
* Health Worker Deployment
* Prometheus Deployment
* Grafana Deployment

---

### Kubernetes Services

Kubernetes Services will provide stable internal networking.

Examples include:

* `frontend-service`
* `api-gateway-service`
* `identity-service`
* `service-registry-service`
* `incident-service`
* `notification-service`
* `postgres-service`
* `redis-service`
* `prometheus-service`
* `grafana-service`

---

### ConfigMaps

ConfigMaps will store non-sensitive configuration such as:

* Service URLs
* Environment names
* Log levels
* Feature flags
* API prefixes
* Port values
* Monitoring configuration

---

### Secrets

Kubernetes Secrets will store sensitive configuration such as:

* Database passwords
* JWT signing secrets
* Redis credentials
* Administrative seed credentials

Only synthetic demonstration credentials will be used.

---

### Ingress

Ingress may route:

* `/` → React Frontend
* `/api` → API Gateway
* `/grafana` → Grafana where appropriate

---

### Liveness Probes

Liveness probes will determine when a failed service instance must be restarted.

```text
SERVICE INSTANCE
      │
      ▼
LIVENESS PROBE
      │
      ├── Success → Continue running
      │
      └── Repeated failure → Restart container
```

---

### Readiness Probes

Readiness probes will determine when an instance can receive traffic.

```text
NEW POD STARTS
      │
      ▼
READINESS PROBE
      │
      ├── Database unavailable → Not Ready
      ├── Startup incomplete → Not Ready
      └── Dependencies available → Ready
                                   │
                                   ▼
                          RECEIVE USER TRAFFIC
```

---

## Kubernetes Recovery Demonstration

One important visual demonstration will be intentionally stopping a service pod and watching Kubernetes replace it.

```text
3 INCIDENT SERVICE PODS
      │
      ├── incident-pod-1
      ├── incident-pod-2
      └── incident-pod-3
              │
              ▼
     incident-pod-2 deleted
              │
              ▼
     Kubernetes detects missing replica
              │
              ▼
     New incident pod automatically created
              │
              ▼
     Desired replica count restored to 3
```

This demonstrates:

* Desired state
* Replica management
* Self-healing
* Fault recovery
* Service continuity

---

## Horizontal Scaling Architecture

Selected stateless services will support multiple replicas.

```text
                     API GATEWAY SERVICE
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Gateway Pod 1    Gateway Pod 2    Gateway Pod 3
```

Potential scaling demonstrations include:

* Multiple API Gateway replicas
* Multiple Incident Service replicas
* Multiple Notification Service workers
* Multiple Health Monitoring workers

The user-facing application will continue using one stable service address.

---

## CI/CD Architecture

GitHub Actions will automate validation.

```text
DEVELOPER PUSHES CODE
        │
        ▼
GITHUB REPOSITORY
        │
        ▼
GITHUB ACTIONS
        │
        ├── Install dependencies
        ├── Validate formatting
        ├── Run linting
        ├── Run backend tests
        ├── Run frontend tests
        ├── Build React application
        ├── Validate Docker images
        ├── Scan dependencies
        ├── Scan for secrets
        └── Report result
        │
        ▼
PASS OR FAIL
```

A controlled delivery workflow may:

* Build Docker images
* Tag images
* Validate Kubernetes manifests
* Prepare deployment artifacts
* Support future deployment

---

## Failure Handling Architecture

NEXUS will handle failures such as:

* Invalid credentials
* Expired authentication tokens
* Unauthorized requests
* PostgreSQL unavailability
* Redis unavailability
* Downstream service failure
* Health-check timeout
* Notification failure
* Invalid request data
* Container failure
* Kubernetes pod restart

Services should:

* Return clear errors
* Log failures
* Preserve correlation identifiers
* Avoid exposing sensitive details
* Use explicit network timeouts
* Use controlled retries
* Avoid infinite retry loops
* Record failed processing status
* Continue operating when unrelated components fail

---

## Testing Architecture

### Unit Tests

Unit tests will validate:

* Authentication logic
* Authorization rules
* Input validation
* Service business rules
* Incident state transitions
* Notification processing
* Health-status evaluation

### Integration Tests

Integration tests will validate:

* API and PostgreSQL communication
* API and Redis communication
* API Gateway routing
* Service-to-service communication
* Notification processing
* Health-check storage

### Contract Tests

Contract tests will validate:

* Request models
* Response models
* Required fields
* HTTP status codes
* Gateway-to-service compatibility

### End-to-End Tests

End-to-end tests will validate:

* Login
* Service registration
* Service search
* Manual health checks
* Incident creation
* Incident assignment
* Incident resolution
* Notification visibility
* Role-based restrictions

---

## Repository Architecture

The planned repository structure is:

```text
nexus-cloud-native-microservices-platform/
│
├── .github/
│   └── workflows/
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
│
├── infrastructure/
│   ├── docker/
│   ├── kubernetes/
│   └── monitoring/
│
├── scripts/
│
├── services/
│
├── tests/
│   ├── contract/
│   ├── end_to_end/
│   └── integration/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Proposed Service Directory Structure

```text
services/
│
├── api_gateway/
├── identity_service/
├── service_registry/
├── incident_service/
├── notification_service/
└── health_worker/
```

Each service may contain:

* Application source code
* API routes
* Data models
* Business services
* Configuration
* Tests
* Dockerfile
* Dependency file
* Health endpoint
* Service documentation

---

## Architecture Tradeoffs

### Microservices Versus Monolith

Microservices provide:

* Independent deployment
* Clear service ownership
* Horizontal scaling
* Fault isolation
* Polyglot development
* Strong portfolio value

Microservices also create:

* Additional networking
* More containers
* More configuration
* More testing complexity
* More deployment complexity

NEXUS intentionally uses microservices because cloud-native architecture is a primary project objective.

---

### Shared PostgreSQL Instance Versus Database Per Service

A production platform may use one database per service.

NEXUS may use one PostgreSQL container with isolated schemas or databases during local development.

This provides:

* Lower resource usage
* Simpler local setup
* Easier demonstration
* Logical service ownership
* Reduced infrastructure complexity

---

### REST Versus Event-Driven Communication

REST provides:

* Simpler implementation
* Easier debugging
* Clear API documentation
* Faster development

Event-driven communication provides:

* Stronger decoupling
* Better asynchronous scaling
* Durable event history
* Event replay

The initial implementation will use REST for primary requests and Redis-backed asynchronous processing for notifications and health tasks.

Apache Kafka remains a future enhancement.

---

### Local Kubernetes Versus Cloud Kubernetes

Local Kubernetes provides:

* No hosting cost
* No credit-card requirement
* Access to core Kubernetes capabilities
* Repeatable development
* Self-healing demonstrations
* Replica scaling demonstrations

Cloud Kubernetes provides:

* Public access
* Managed infrastructure
* Production-style networking
* Cloud integrations

The initial implementation will use local Kubernetes.

---

## Architecture Risks

Potential risks include:

* Excessive application complexity
* High local resource usage
* Difficult debugging across services
* Authentication inconsistencies
* API contract mismatches
* Database ownership confusion
* Slow container startup
* Kubernetes configuration errors
* Monitoring-tool overhead
* Cross-service failure propagation

Mitigation will include:

* Clear service responsibilities
* Visual frontend-first development
* Phased implementation
* Shared API conventions
* Automated tests
* Health checks
* Structured logs
* Correlation identifiers
* Docker Compose before Kubernetes
* A controlled number of services
* Incremental observability
* Documented troubleshooting procedures

---

# Related Architecture Documents

The NEXUS Cloud-Native Microservices Platform is documented through several complementary architecture documents, each focused on a specific aspect of the system.

| Document | Purpose |
|----------|---------|
| architecture.md | Overall system architecture, application flow, infrastructure, and microservices |
| database_architecture.md | Database domains, entity relationships, normalization strategy, and data modeling |
| technical_design.md | Implementation strategy and technical decisions |
| security_design.md | Authentication, authorization, and security architecture |
| deployment_strategy.md | Docker, Kubernetes, and deployment workflows |
| testing_strategy.md | Testing methodology and quality assurance |

---

## Architecture Decision Summary

NEXUS will use:

* React for the visible frontend application
* Node.js and Express for the API Gateway
* FastAPI for selected backend services
* Node.js or Python for additional services
* PostgreSQL for persistent relational data
* Redis for caching and asynchronous processing
* REST APIs for primary communication
* JSON Web Tokens for authentication
* Role-based access control for authorization
* Docker for containerization
* Docker Compose for local orchestration
* Kubernetes for cloud-native deployment
* Prometheus for metrics
* Grafana for monitoring dashboards
* OpenTelemetry-compatible tooling for tracing
* GitHub Actions for CI/CD
* Automated testing across multiple levels
* Free and open-source technologies wherever practical

---

## Final Architecture Outcome

NEXUS will be a visible, interactive full-stack application rather than a backend-only technical demonstration.

Users will be able to:

* Log in securely
* View platform health
* Monitor registered services
* Open service-detail pages
* Review uptime and response time
* Run health checks
* Create incidents
* Assign and resolve incidents
* Review notifications
* Manage users and roles
* View monitoring dashboards
* Observe service recovery and scaling

The backend architecture will power these visible capabilities through:

* A centralized API Gateway
* Identity management
* Service inventory management
* Health monitoring
* Incident management
* Notification processing
* PostgreSQL persistence
* Redis-backed asynchronous workflows
* Structured logs
* Prometheus metrics
* Distributed tracing
* Docker containers
* Kubernetes Deployments
* Kubernetes Services
* ConfigMaps
* Secrets
* Ingress
* Liveness probes
* Readiness probes
* Horizontal scaling
* Automated testing
* CI/CD
* Security validation

The project will follow a visual-first learning approach:

```text
SEE THE APPLICATION
        │
        ▼
UNDERSTAND THE USER ACTION
        │
        ▼
CONNECT THE ACTION TO AN API
        │
        ▼
CONNECT THE API TO A MICROSERVICE
        │
        ▼
CONNECT THE MICROSERVICE TO DATA
        │
        ▼
CONTAINERIZE THE COMPONENT
        │
        ▼
DEPLOY IT TO KUBERNETES
        │
        ▼
MONITOR, SCALE, AND RECOVER IT
```

This architecture creates a practical and visible foundation for the remaining Project #10 technical design, user-experience design, implementation, testing, deployment, and operational documentation.