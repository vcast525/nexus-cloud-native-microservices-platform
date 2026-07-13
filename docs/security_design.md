Monday, July 13, 2026 — 12:19 PM ET

# Security Design Document

## Security Design Overview

This document defines the security model for the NEXUS Cloud-Native Microservices Platform.

NEXUS is an internal service operations application that manages:

* User accounts
* User roles
* Service ownership information
* Health-monitoring results
* Operational incidents
* Notifications
* Audit activity
* Application configuration
* Kubernetes deployment resources

Although NEXUS uses synthetic portfolio data rather than real production information, the application will be designed using practical security principles that reflect professional software-engineering expectations.

The security design covers:

* Authentication
* Authorization
* Password protection
* JSON Web Token security
* Role-based access control
* API protection
* Input validation
* Database security
* Redis security
* Secret management
* Logging protection
* Auditability
* Container security
* Kubernetes security
* CI/CD security
* Dependency scanning
* Secret scanning
* Vulnerability management
* Secure error handling
* Threat mitigation
* Security testing
* Incident-response considerations

Security will be treated as a system-wide responsibility rather than a feature owned by only one microservice.

---

## Security Objectives

The NEXUS security model is designed to:

* Prevent unauthorized platform access
* Protect user credentials
* Prevent users from performing actions outside their assigned roles
* Protect backend APIs
* Prevent secrets from entering source control
* Validate all untrusted input
* Limit unnecessary service exposure
* Preserve traceable audit history
* Avoid sensitive data exposure through logs
* Reduce common web-application vulnerabilities
* Use secure container and Kubernetes configuration
* Detect vulnerable dependencies
* Detect accidentally committed secrets
* Provide clear but non-sensitive error responses
* Demonstrate practical security engineering within a portfolio project

---

## Security Principles

NEXUS will follow these core principles.

### Defense in Depth

Security controls will exist across multiple layers:

```text
USER INTERFACE
      │
      ▼
API GATEWAY
      │
      ▼
BACKEND SERVICES
      │
      ▼
DATABASE AND REDIS
      │
      ▼
DOCKER AND KUBERNETES
      │
      ▼
CI/CD AND SOURCE CONTROL
```

A failure in one layer should not eliminate all protection.

---

### Least Privilege

Users, services, containers, and Kubernetes resources should receive only the access required to perform their responsibilities.

Examples:

* Viewers receive read-only access
* Operations Analysts cannot manage user roles
* Frontend cannot access PostgreSQL directly
* Notification Worker cannot modify user accounts
* Database credentials are scoped to application needs
* Public ingress exposes only approved application endpoints

---

### Secure by Default

The default system behavior should be restrictive.

Examples:

* Protected endpoints require authentication
* Unknown roles receive no elevated permissions
* New users are assigned only approved roles
* Secrets are absent from committed files
* Internal services are not publicly exposed
* Error responses omit stack traces
* CORS allows only approved origins

---

### Never Trust Client-Side Enforcement Alone

The React frontend may hide or disable restricted controls.

However, backend services will always perform authorization checks.

```text
FRONTEND HIDES CONTROL
        │
        ▼
IMPROVES USER EXPERIENCE
        │
        ▼
BACKEND STILL VALIDATES ROLE
        │
        ▼
SECURITY DECISION IS ENFORCED
```

---

### Validate All External Input

Input from users, HTTP requests, API Gateway traffic, environment variables, health endpoints, and asynchronous tasks will be treated as untrusted until validated.

---

### Protect Secrets and Sensitive Values

Passwords, password hashes, tokens, signing secrets, database credentials, and private keys must not appear in:

* GitHub
* Application responses
* Screenshots
* Logs
* Documentation examples containing real values
* Frontend source code
* Docker images
* Public Kubernetes ConfigMaps

---

## Security Scope

### In Scope

The initial NEXUS security implementation includes:

* Local username and password authentication
* Secure password hashing
* JWT access tokens
* Role-based authorization
* Protected frontend routes
* Protected backend endpoints
* User activation and deactivation
* Input validation
* Rate limiting
* CORS configuration
* Secure HTTP headers
* Environment-based configuration
* `.env.example`
* Kubernetes Secrets
* Structured audit events
* Secure error handling
* Dependency scanning
* Secret scanning
* Container scanning
* Non-root containers where practical
* Internal Kubernetes Services
* Security-focused automated tests

### Out of Scope

The initial implementation excludes:

* Enterprise single sign-on
* SAML
* OAuth provider integration
* OpenID Connect provider integration
* Hardware security modules
* Production certificate management
* Managed secrets vaults
* Multi-factor authentication
* Production penetration testing
* Formal compliance certification
* Production identity governance
* Real employee or customer information
* Public internet production deployment

These capabilities may be documented as future enhancements.

---

## Security Trust Boundaries

NEXUS contains several trust boundaries.

```text
┌──────────────────────────────────────────────────────────────┐
│                         USER DEVICE                          │
│                                                              │
│  React Browser Application                                  │
└───────────────────────────┬──────────────────────────────────┘
                            │
                     Untrusted Network Request
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                     PUBLIC APPLICATION EDGE                  │
│                                                              │
│  Kubernetes Ingress                                         │
│  API Gateway                                                │
└───────────────────────────┬──────────────────────────────────┘
                            │
                     Internal Service Traffic
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                     APPLICATION SERVICES                     │
│                                                              │
│  Identity Service                                           │
│  Service Registry                                           │
│  Incident Service                                           │
│  Notification Service                                       │
│  Health Worker                                              │
└───────────────────────────┬──────────────────────────────────┘
                            │
                     Data and Queue Access
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                       DATA SERVICES                          │
│                                                              │
│  PostgreSQL                                                 │
│  Redis                                                      │
└──────────────────────────────────────────────────────────────┘
```

Controls will be applied at each boundary.

---

## Authentication Design

NEXUS will use local username and password authentication for the initial portfolio implementation.

The Identity Service will be the source of truth for:

* User accounts
* Password hashes
* User roles
* Account activation status
* Login events
* JWT issuance

---

## Authentication Flow

```text
USER ENTERS CREDENTIALS
        │
        ▼
REACT FRONTEND
        │
        ▼
API GATEWAY
        │
        ▼
IDENTITY SERVICE
        │
        ├── Validate request format
        ├── Locate active user
        ├── Verify password hash
        ├── Retrieve role
        ├── Record login event
        └── Generate JWT
        │
        ▼
TOKEN RETURNED TO FRONTEND
        │
        ▼
TOKEN INCLUDED IN PROTECTED REQUESTS
```

---

## Login Security Controls

The Login endpoint will:

* Accept only approved request fields
* Validate username or email format
* Validate password presence
* Avoid revealing whether a specific username exists
* Return the same general message for invalid usernames and passwords
* Record successful and failed authentication events
* Apply rate limiting
* Reject inactive accounts
* Avoid logging credentials
* Use HTTPS assumptions in production-oriented documentation

Example failed-login message:

```text
The username or password was not recognized.
```

The response should not say:

```text
This username does not exist.
```

That would assist account enumeration.

---

## Password Security

### Password Storage

Passwords will never be stored directly.

The Identity Service will store only password hashes.

The selected approach will use:

* bcrypt
* Passlib
* Unique salts generated by the hashing implementation

---

### Password Requirements

Initial password rules may include:

* Minimum length of 12 characters
* At least one uppercase letter
* At least one lowercase letter
* At least one number
* At least one special character
* Password must not equal the username
* Password must not equal the email address

Because this is a portfolio project, the exact rules may remain configurable.

---

### Password Handling Rules

Passwords must not be:

* Returned in API responses
* Stored in plain text
* Written to logs
* Included in audit-change details
* Added to frontend local storage
* Committed in seed files
* Displayed in screenshots
* Stored in Kubernetes ConfigMaps

---

### Demonstration User Credentials

Synthetic demonstration accounts may be created during seeding.

Default passwords should:

* Exist only in local setup instructions
* Be changed easily
* Never resemble real credentials
* Be excluded from screenshots where practical
* Be documented as demonstration-only

---

## JSON Web Token Design

NEXUS will use signed JWT access tokens.

### Token Purpose

JWT access tokens allow the platform to verify:

* User identity
* Assigned role
* Token issue time
* Token expiration
* Token identifier

---

### Token Claims

Approved claims may include:

```text
sub
username
role
iat
exp
jti
```

Definitions:

| Claim | Meaning |
| --- | --- |
| `sub` | Authenticated user identifier |
| `username` | Display or account identifier |
| `role` | Assigned authorization role |
| `iat` | Token issue time |
| `exp` | Token expiration time |
| `jti` | Unique token identifier |

Sensitive data should not be stored inside JWT claims.

---

### Token Lifetime

Initial access-token lifetime:

```text
30 minutes
```

Short-lived tokens reduce the impact of accidental token exposure.

A future refresh-token flow may be added if required.

---

### JWT Signing

JWTs will use a server-side signing secret supplied through:

* Local `.env`
* Docker Compose environment configuration
* Kubernetes Secret

The signing secret will not be:

* Stored in frontend code
* Committed to GitHub
* Added to `.env.example`
* Logged
* Returned in responses

---

### Token Validation

Protected services will validate:

* Signature
* Expiration
* Required claims
* Expected algorithm
* User activation status where practical
* Role values

The algorithm must be explicitly configured.

The application must not accept arbitrary algorithms supplied by the token header.

---

### Authorization Header

Protected requests will use:

```text
Authorization: Bearer <access-token>
```

The API Gateway will forward the header to downstream services.

The complete header will not be logged.

---

## Frontend Session Security

The frontend must store authentication state carefully.

The preferred implementation should avoid long-term token persistence where practical.

Possible storage choices include:

### In-Memory Storage

Advantages:

* Reduced persistence after browser closure
* Lower exposure to persistent storage theft

Considerations:

* Session is lost on page refresh unless restored

### Session Storage

Advantages:

* Survives page refresh
* Cleared when browser session ends

Considerations:

* Accessible to JavaScript
* Vulnerable if an XSS flaw exists

### HTTP-Only Cookie

Advantages:

* Not directly accessible to JavaScript
* Better protection against token theft through XSS

Considerations:

* Requires CSRF protections
* Adds implementation complexity

The initial project may use session storage for simplicity, with the security tradeoff clearly documented.

A future enhancement may move authentication to secure HTTP-only cookies.

---

## Logout Security

Logout will:

* Clear local authentication state
* Remove stored token information
* Redirect the user to Login
* Prevent access to protected routes
* Record a logout event where practical

Because stateless JWTs remain valid until expiration unless revocation is implemented, short token lifetimes are important.

A future token-denylist mechanism may use Redis.

---

## Account Activation and Deactivation

User accounts will include an active-status field.

Inactive users:

* Cannot authenticate
* Cannot receive new tokens
* Remain associated with historical audit activity
* Are not permanently deleted from operational records

When an administrator deactivates an account:

```text
ADMINISTRATOR REQUEST
        │
        ▼
IDENTITY SERVICE VALIDATES ROLE
        │
        ▼
ACCOUNT SET TO INACTIVE
        │
        ▼
AUDIT EVENT RECORDED
        │
        ▼
FUTURE LOGINS REJECTED
```

---

## Role-Based Access Control

NEXUS supports four primary roles:

* Platform Administrator
* Service Owner
* Operations Analyst
* Viewer

---

## Role Permissions

### Platform Administrator

May:

* Manage users
* Assign roles
* Activate and deactivate accounts
* Register and modify services
* Deactivate services
* Manage incidents
* Retry failed notifications
* Access monitoring
* Review audit information
* Change administrative configuration

---

### Service Owner

May:

* View services
* Register approved services
* Update assigned services
* Review service health
* Run health checks
* Create incidents
* Update incidents related to owned services
* Resolve incidents
* Review notifications
* Access monitoring information

---

### Operations Analyst

May:

* View services
* Review service health
* Run health checks
* Create incidents
* Assign incidents
* Change incident status
* Resolve incidents
* Review notifications
* Retry failed notifications
* Access monitoring information

---

### Viewer

May:

* View dashboard information
* View services
* View service health
* View incidents
* View notifications
* View permitted monitoring summaries

Viewer access is read-only.

---

## Authorization Matrix

| Capability | Administrator | Service Owner | Operations Analyst | Viewer |
| --- | --- | --- | --- | --- |
| View Dashboard | Yes | Yes | Yes | Yes |
| View Services | Yes | Yes | Yes | Yes |
| Register Service | Yes | Yes | No | No |
| Update Service | Yes | Assigned Services | Limited | No |
| Deactivate Service | Yes | No | No | No |
| Run Health Check | Yes | Yes | Yes | No |
| View Incidents | Yes | Yes | Yes | Yes |
| Create Incident | Yes | Yes | Yes | No |
| Assign Incident | Yes | Limited | Yes | No |
| Resolve Incident | Yes | Yes | Yes | No |
| Close Incident | Yes | Yes | Limited | No |
| View Notifications | Yes | Yes | Yes | Yes |
| Retry Notification | Yes | Limited | Yes | No |
| Manage Users | Yes | No | No | No |
| Assign Roles | Yes | No | No | No |
| View Monitoring | Yes | Yes | Yes | Limited |
| View Audit Events | Yes | Limited | Limited | No |

---

## Backend Authorization Enforcement

Authorization will occur inside backend services.

Example:

```text
REQUEST RECEIVED
      │
      ▼
TOKEN VALIDATED
      │
      ▼
USER ROLE EXTRACTED
      │
      ▼
REQUIRED PERMISSION CHECKED
      │
      ├── ALLOWED
      │     │
      │     ▼
      │  BUSINESS LOGIC EXECUTES
      │
      └── DENIED
            │
            ▼
         HTTP 403 RETURNED
```

---

## Ownership-Based Authorization

Some operations require more than a general role check.

Example:

A Service Owner may update:

* Services owned by the user
* Services owned by the user’s support team

The user should not automatically update every service in the platform.

Ownership checks may evaluate:

* User identifier
* Support-team membership
* Assigned service owner
* Administrator override

---

## API Gateway Security

The API Gateway is the primary public API entry point.

Security responsibilities include:

* Apply secure HTTP headers
* Configure CORS
* Apply rate limiting
* Generate correlation identifiers
* Reject excessively large requests
* Validate expected route patterns
* Forward authentication headers
* Normalize errors
* Prevent public access to undocumented internal routes
* Record safe request metadata
* Apply request timeouts

---

## Secure HTTP Headers

Helmet will be used where appropriate.

Headers may include:

* Content Security Policy
* X-Content-Type-Options
* X-Frame-Options
* Referrer-Policy
* Permissions-Policy
* Strict-Transport-Security in HTTPS environments

Exact policy settings will be tested to avoid breaking the frontend.

---

## CORS Security

CORS will allow only approved frontend origins.

Local example:

```text
http://localhost:3000
```

Kubernetes example:

```text
http://nexus.local
```

The platform will avoid unrestricted production-style configuration such as:

```text
Access-Control-Allow-Origin: *
```

when credentials or protected resources are involved.

---

## Rate Limiting

Rate limiting will protect selected endpoints.

Candidate endpoints include:

* Login
* Token refresh
* User creation
* Service registration
* Manual health-check requests
* Notification retries

Example limits may include:

| Endpoint | Example Limit |
| --- | --- |
| Login | 5 attempts per minute per client |
| Manual Health Check | 10 requests per minute per user |
| Notification Retry | 10 requests per minute per user |
| General API | 100 requests per minute per client |

Values will be tuned during implementation.

Redis may store distributed rate-limit state.

---

## Request Size Limits

The gateway and services will limit request body size.

This reduces risks involving:

* Resource exhaustion
* Accidental oversized submissions
* Malicious payloads
* Excessive logging

Example:

```text
1 MB maximum JSON request body
```

Larger values should require explicit justification.

---

## API Timeout Security

Gateway requests will use explicit downstream timeouts.

This reduces:

* Hanging connections
* Resource exhaustion
* Cascading failures
* Denial-of-service amplification

Example timeout:

```text
5 seconds for standard service calls
```

Health-check requests may use separate configurable timeouts.

---

## Input Validation

Each service will validate request data before business logic executes.

### Python Services

FastAPI and Pydantic will validate:

* Required fields
* Data types
* String lengths
* Email format
* Enum values
* UUID format
* Date and timestamp format
* Allowed status values

### Node.js Services

Zod or another approved validation library will validate:

* Request bodies
* Query parameters
* Route parameters
* Enum values
* String lengths
* URLs
* Identifiers

---

## Field Validation Examples

| Field | Validation |
| --- | --- |
| Username | Required, bounded length, approved characters |
| Email | Valid email format |
| Password | Required complexity |
| Service Code | Required, unique, approved characters |
| Service Name | Required, bounded length |
| Health Endpoint | Valid HTTP or HTTPS URL |
| Incident Title | Required, bounded length |
| Incident Description | Required, maximum length |
| Priority | Approved enum value |
| Status | Approved enum value |
| UUID | Valid UUID format |

---

## Output Encoding

React will render text content safely using standard framework behavior.

The application will avoid unnecessarily injecting raw HTML.

Any future raw HTML rendering must be sanitized.

This reduces cross-site scripting risk.

---

## SQL Injection Protection

The platform will use:

* SQLAlchemy parameterized queries
* Prisma query APIs
* ORM filters
* Prepared database operations

The application will avoid constructing SQL with untrusted string concatenation.

Unsafe example:

```text
"SELECT * FROM users WHERE username = '" + input + "'"
```

Approved access will occur through ORM or parameterized query mechanisms.

---

## NoSQL and Redis Injection Considerations

Redis keys will be created from controlled formats.

User input will not directly determine unrestricted Redis commands.

Redis operations will use approved client-library methods.

---

## URL Validation for Health Checks

Health-check endpoints present a server-side request risk.

Without controls, a user might register URLs targeting:

* Localhost
* Internal metadata services
* Private network addresses
* Unexpected protocols
* Sensitive internal endpoints

This creates a potential Server-Side Request Forgery risk.

---

## SSRF Mitigation

The Health Worker should apply controls such as:

* Allow only HTTP and HTTPS protocols
* Reject file URLs
* Reject unsupported protocols
* Reject localhost where practical
* Reject loopback IP addresses
* Reject cloud metadata addresses
* Optionally restrict private network ranges
* Apply strict timeouts
* Limit redirect count
* Limit response size
* Avoid forwarding authentication credentials
* Log rejected health endpoints safely

Because the project runs locally and monitors synthetic services, an allowlist approach may be used.

Example approved hosts:

```text
demo-health-service
service-registry
identity-service
incident-service
notification-api
api-gateway
```

---

## Health-Check Response Limits

The Health Worker will not download unlimited content.

Controls may include:

* Maximum response size
* Short connection timeout
* Short read timeout
* Limited redirects
* No file downloads
* No credential forwarding

The worker needs only health status and timing information.

---

## Business Rule Validation

Security also includes enforcing approved business states.

Examples:

* Closed incidents cannot be reopened without a defined workflow
* Resolved incidents require a resolution summary
* Viewers cannot modify records
* Inactive users cannot authenticate
* Duplicate service codes are rejected
* Only administrators may assign roles
* Notification retries require approved permissions
* A user should not deactivate their own administrator account when it would leave no active administrator

---

## Error Handling Security

Error responses will be understandable but non-sensitive.

The application must not expose:

* Stack traces
* SQL queries
* Database credentials
* Internal file paths
* JWT secrets
* Redis connection strings
* Container names unless useful and safe
* Internal exception objects
* Password hashes

---

## Standard Secure Error Response

```json
{
  "success": false,
  "error": {
    "code": "ACCESS_DENIED",
    "message": "You do not have permission to perform this action.",
    "details": []
  },
  "correlation_id": "example-correlation-id",
  "timestamp": "2026-07-13T16:19:00Z"
}
```

Technical error details belong in protected logs rather than user responses.

---

## Authentication Error Responses

### Invalid Credentials

```text
401 Unauthorized
The username or password was not recognized.
```

### Expired Token

```text
401 Unauthorized
Your session has expired. Please sign in again.
```

### Insufficient Permission

```text
403 Forbidden
You do not have permission to perform this action.
```

### Inactive Account

```text
403 Forbidden
This account is inactive. Contact a platform administrator.
```

---

## Audit Logging

Important security and business events will generate audit records.

### Authentication Events

* Successful login
* Failed login
* Logout
* Inactive-account login attempt
* Expired-token request
* Authorization denial

### User Administration Events

* User created
* User role changed
* User activated
* User deactivated

### Service Events

* Service registered
* Service updated
* Service deactivated
* Health-check requested
* Health status changed

### Incident Events

* Incident created
* Assignment changed
* Priority changed
* Status changed
* Incident resolved
* Incident closed

### Notification Events

* Notification created
* Notification processed
* Notification failed
* Notification retry requested

---

## Audit Record Design

Audit records may contain:

```text
event_type
source_service
user_id
resource_type
resource_id
action
result
change_summary
correlation_id
created_at
```

Audit records must not contain:

* Passwords
* JWTs
* Password hashes
* Full authorization headers
* Database credentials
* Secret values

---

## Audit Integrity

Audit records should:

* Be append-oriented
* Preserve original timestamps
* Avoid casual user deletion
* Record the acting user
* Record system-generated actions
* Include correlation identifiers
* Capture before-and-after values where appropriate

The initial implementation may not provide a user-facing delete function for audit records.

---

## Logging Security

Structured logs will support debugging and security investigation.

### Approved Log Fields

* Timestamp
* Service name
* Environment
* Log level
* Event name
* Correlation identifier
* Request method
* Request path
* HTTP status
* Duration
* User identifier when appropriate
* Resource identifier
* Error type
* Safe error message

---

## Logging Redaction

Logs must redact or omit:

* Authorization headers
* JWT values
* Password fields
* Password hashes
* Cookie values
* Database passwords
* Redis passwords
* Secret keys
* Private keys
* Full personal data where unnecessary

A shared logging utility should remove sensitive fields before output.

---

## Database Security

PostgreSQL security controls will include:

* Credentials supplied through environment variables
* No database password committed to GitHub
* Separate logical schemas
* Service-owned data access
* Parameterized ORM queries
* Required constraints
* Foreign keys
* Unique indexes
* Limited public exposure
* Persistent volume protection within local constraints

---

## Database User Strategy

A simple local implementation may begin with one application database user.

A stronger implementation may use separate service accounts:

```text
identity_app
registry_app
incident_app
notification_app
```

Each account would receive access only to its owned schema.

The final implementation will balance realism with local complexity.

---

## Database Network Exposure

PostgreSQL will be available to:

* Application services
* Migration tools
* Approved local administration tools

PostgreSQL should not be exposed through Kubernetes Ingress.

Local host port exposure should exist only when needed for development.

---

## Migration Security

Database migrations will:

* Be reviewed before execution
* Avoid embedded credentials
* Be version controlled
* Avoid destructive operations without explanation
* Run using approved service credentials
* Preserve required audit history

---

## Redis Security

Redis will be used for:

* Celery task queueing
* Retry coordination
* Health-check tasks
* Notification tasks
* Rate-limit state
* Optional caching

Security controls include:

* Internal network access only
* Environment-based connection values
* No public ingress
* Authentication where practical
* Controlled key naming
* Expiration for temporary data
* No storage of passwords or JWT signing secrets
* No use as the primary permanent system of record

---

## Asynchronous Task Validation

Celery tasks will validate incoming payloads.

A queued task must not be trusted merely because it originated inside the platform.

Task validation will include:

* Event type
* Resource identifier
* Required fields
* Timestamp
* Correlation identifier
* Supported severity
* Maximum message length

Invalid tasks will:

* Be rejected
* Produce safe logs
* Record failure status where practical
* Avoid endless retries

---

## Secret Management

NEXUS will use separate handling for sensitive and non-sensitive configuration.

### Non-Sensitive Configuration

Stored in:

* `.env.example`
* Docker Compose configuration
* Kubernetes ConfigMaps

Examples:

* Service URLs
* Port numbers
* Environment name
* Log level
* API prefix

### Sensitive Configuration

Stored in:

* Local `.env`
* Docker Compose environment values excluded from Git
* Kubernetes Secrets

Examples:

* PostgreSQL password
* JWT signing secret
* Redis password
* Administrative seed password

---

## `.env.example` Rules

The `.env.example` file will contain variable names but not live values.

Approved example:

```text
JWT_SECRET=
POSTGRES_PASSWORD=
REDIS_PASSWORD=
```

Unapproved example:

```text
JWT_SECRET=my-real-secret-value
```

---

## `.gitignore` Security Rules

The `.gitignore` file should exclude:

```text
.env
.env.local
.env.*.local
*.pem
*.key
*.crt
secrets/
kube-secrets.yaml
coverage/
node_modules/
.venv/
__pycache__/
```

Public certificate files may be handled differently if later required.

---

## Kubernetes Secret Design

Kubernetes Secrets may contain:

* JWT signing secret
* PostgreSQL username
* PostgreSQL password
* Redis password
* Administrative seed credentials

Secret manifests containing actual values will not be committed.

The repository may include:

```text
secret.example.yaml
```

with placeholders only.

---

## Kubernetes Secret Loading

Services may consume secrets through:

* Environment variables
* Mounted secret files where appropriate

Example logical mapping:

```text
JWT_SECRET ← Kubernetes Secret
POSTGRES_PASSWORD ← Kubernetes Secret
REDIS_PASSWORD ← Kubernetes Secret
```

---

## Kubernetes Security

### Namespace Isolation

NEXUS resources will use:

```text
namespace: nexus
```

This organizes application resources and supports policy isolation.

---

### Internal Services

Backend components will use ClusterIP Services.

The following should remain internal:

* Identity Service
* Service Registry
* Incident Service
* Notification API
* PostgreSQL
* Redis
* Prometheus
* Jaeger

External access should pass through approved ingress routes.

---

### Ingress Exposure

Approved ingress paths may include:

```text
/       → React Frontend
/api    → API Gateway
```

Grafana may use:

* Local port forwarding
* Restricted ingress
* Demonstration-only access

PostgreSQL and Redis will never use public ingress.

---

### Container Users

Containers should run as non-root users where practical.

This reduces the impact of container compromise.

Example security context concepts:

```text
runAsNonRoot: true
allowPrivilegeEscalation: false
readOnlyRootFilesystem: true
```

Some components may require exceptions, which must be documented.

---

### Kubernetes Security Context

Workloads may use:

* Non-root user
* Non-zero user identifier
* Disabled privilege escalation
* Dropped Linux capabilities
* Read-only root filesystem where practical
* Seccomp default profile

---

### Resource Limits

Resource requests and limits help reduce denial-of-service risk from uncontrolled consumption.

Example:

```text
requests:
  cpu: 100m
  memory: 128Mi

limits:
  cpu: 500m
  memory: 512Mi
```

---

### Network Policies

A future or stretch implementation may use Kubernetes NetworkPolicies.

Example communication rules:

* Frontend may call API Gateway
* API Gateway may call backend services
* Backend services may call PostgreSQL
* Workers may call Redis and approved services
* PostgreSQL accepts traffic only from approved application pods
* Redis accepts traffic only from approved application pods

---

## Docker Security

Docker images will follow these practices:

* Use official base images
* Use minimal images where practical
* Pin or bound dependency versions
* Exclude development secrets
* Use `.dockerignore`
* Avoid copying unnecessary files
* Run as non-root where practical
* Expose only required ports
* Scan images with Trivy
* Rebuild when security updates are available

---

## `.dockerignore` Design

Each service should exclude:

```text
.git
.env
.venv
node_modules
coverage
tests
__pycache__
*.pyc
*.log
```

Tests may remain available in development images if needed, but production-oriented images should remain minimal.

---

## Dependency Security

The project uses Python and Node.js dependencies.

Security controls include:

* Dependency locking
* Dependabot
* `pip-audit`
* `npm audit`
* Trivy
* Version review
* Removal of unused packages
* Avoidance of abandoned packages where practical

---

## Dependency Review Questions

Before adding a package, evaluate:

* Is it actively maintained?
* Is it necessary?
* Is there a standard-library alternative?
* Does it have known vulnerabilities?
* Does it add significant transitive dependencies?
* Is its license appropriate?
* Is it widely used and documented?

---

## Source-Control Security

GitHub repository protections should include:

* Public repository contains no live secrets
* Pull requests for major changes
* CI validation
* Secret scanning
* Dependabot alerts
* Clear commit history
* Protected main branch where practical
* Reviewed workflow files

---

## GitHub Actions Security

Workflow security controls include:

* Pin trusted action versions
* Grant minimal workflow permissions
* Avoid printing secrets
* Use repository secrets only when required
* Avoid executing untrusted scripts with elevated credentials
* Separate pull-request validation from deployment credentials
* Scan dependencies and containers
* Use manual approval for future deployment workflows

---

## Workflow Permission Principle

GitHub Actions should use minimal permissions.

Example:

```text
contents: read
```

Additional permissions should be granted only when necessary.

---

## Secret Scanning

Gitleaks will scan for:

* API keys
* Passwords
* Tokens
* Private keys
* Connection strings
* High-entropy secrets

Secret scanning should run:

* Locally when practical
* In GitHub Actions
* Before release milestones

---

## Container Scanning

Trivy may scan:

* Docker images
* Operating-system packages
* Application dependencies
* Kubernetes manifests
* Misconfigurations

Results should be reviewed rather than blindly ignored.

---

## Vulnerability Management

When a vulnerability is identified:

```text
VULNERABILITY DETECTED
        │
        ▼
ASSESS SEVERITY AND EXPOSURE
        │
        ├── LOW RISK
        │     │
        │     ▼
        │  TRACK AND PLAN UPDATE
        │
        └── HIGH OR CRITICAL RISK
              │
              ▼
           UPDATE DEPENDENCY OR CONFIGURATION
              │
              ▼
           RUN TESTS
              │
              ▼
           REBUILD IMAGE
              │
              ▼
           RESCAN
```

---

## Frontend Security

React security controls include:

* Avoid raw HTML injection
* Validate forms
* Protect routes
* Clear session on logout
* Clear session after token expiration
* Avoid storing secrets in frontend environment variables
* Avoid exposing internal service URLs
* Display safe error messages
* Use framework escaping
* Avoid sensitive values in browser logs

---

## Frontend Environment Variables

Vite variables are included in the built frontend and must be treated as public.

Variables beginning with:

```text
VITE_
```

must not contain:

* JWT signing secrets
* Database credentials
* Redis credentials
* Private keys
* Internal administrative passwords

Approved use:

```text
VITE_API_BASE_URL
```

---

## Content Security Policy

A Content Security Policy may restrict:

* Script sources
* Style sources
* Image sources
* Connection destinations
* Frame embedding

Policy configuration will account for:

* React application assets
* API Gateway communication
* Grafana embedding only if used
* Development tooling differences

---

## Cross-Site Scripting Mitigation

Controls include:

* React default escaping
* No untrusted raw HTML
* Validation of displayed text
* Safe error messages
* Content Security Policy
* Avoiding dangerous DOM APIs

---

## Cross-Site Request Forgery Considerations

When JWTs are sent through Authorization headers, classic cookie-based CSRF risk is reduced.

If future authentication moves to cookies, the platform will require:

* SameSite cookie configuration
* CSRF tokens
* Secure cookie flags
* Origin validation

---

## Clickjacking Protection

The application will use:

* `X-Frame-Options`
* Content Security Policy frame restrictions

This prevents unauthorized websites from embedding NEXUS inside deceptive frames.

---

## Sensitive Data Classification

NEXUS uses synthetic data, but information will still be classified by sensitivity.

### Public Portfolio Information

* Project architecture
* Technology stack
* Synthetic screenshots
* Documentation
* Example API structures

### Internal Application Information

* Synthetic users
* Service ownership
* Incident records
* Health results
* Audit events

### Sensitive Configuration

* Password hashes
* JWT signing secret
* Database credentials
* Redis credentials
* Administrative seed passwords

Sensitive configuration must never appear in the public repository.

---

## Data Minimization

The platform will store only information required for the demonstration.

It will avoid collecting:

* Social Security numbers
* Banking information
* Real employee identifiers
* Real customer information
* Real production credentials
* Unnecessary personal details

Synthetic names and email addresses will be used.

---

## Data Retention

The initial implementation may retain:

* Incident history
* Notification history
* Health history
* Audit events

Because the project is local, formal retention periods are not required.

Future production-oriented documentation may define:

* Health-history retention
* Audit retention
* Notification retention
* Incident archival rules

---

## Threat Model

The following threats are considered relevant to the initial project.

### Threat 1: Credential Theft

Potential causes:

* Weak passwords
* Logging passwords
* Storing tokens insecurely
* Committing secrets

Mitigations:

* bcrypt password hashing
* Password complexity
* Log redaction
* Short-lived JWTs
* Secret scanning
* `.gitignore`
* Kubernetes Secrets

---

### Threat 2: Unauthorized Privilege Escalation

Potential causes:

* Frontend-only role enforcement
* Trusting user-supplied roles
* Missing endpoint checks

Mitigations:

* Backend role checks
* JWT signature validation
* Roles loaded from trusted identity data
* Ownership checks
* Authorization tests

---

### Threat 3: SQL Injection

Potential causes:

* Dynamic SQL construction
* Unvalidated inputs

Mitigations:

* SQLAlchemy
* Prisma
* Parameterized queries
* Input validation
* Security tests

---

### Threat 4: Cross-Site Scripting

Potential causes:

* Raw HTML rendering
* Unsafe third-party components
* Unsanitized content

Mitigations:

* React escaping
* Avoid raw HTML
* Content Security Policy
* Input validation

---

### Threat 5: Server-Side Request Forgery

Potential causes:

* User-controlled health endpoints
* Unrestricted worker requests

Mitigations:

* URL validation
* Protocol allowlist
* Host allowlist for demonstrations
* Private-address restrictions
* Timeouts
* Redirect limits
* Response-size limits

---

### Threat 6: Secret Exposure

Potential causes:

* Committed `.env`
* Logging environment variables
* Public Kubernetes manifests
* GitHub Actions output

Mitigations:

* `.gitignore`
* Gitleaks
* Kubernetes Secrets
* Redacted logs
* Safe workflow configuration
* Placeholder-only examples

---

### Threat 7: Denial of Service

Potential causes:

* Unlimited requests
* Large request bodies
* Repeated health checks
* Endless retries
* Resource exhaustion

Mitigations:

* Rate limiting
* Request-size limits
* Timeouts
* Retry limits
* Kubernetes resources
* Queue controls
* Horizontal scaling

---

### Threat 8: Dependency Vulnerability

Potential causes:

* Outdated packages
* Vulnerable base images
* Unmaintained libraries

Mitigations:

* Dependabot
* `npm audit`
* `pip-audit`
* Trivy
* Version review
* Regular rebuilds

---

### Threat 9: Information Disclosure

Potential causes:

* Stack traces
* Verbose errors
* Sensitive logs
* Public internal services

Mitigations:

* Standard error responses
* Internal-only services
* Log redaction
* Restricted ingress
* Safe API schemas

---

### Threat 10: Queue Abuse

Potential causes:

* Malformed tasks
* Unlimited retries
* Duplicate tasks
* Unauthorized retry requests

Mitigations:

* Task schema validation
* Maximum retry counts
* Idempotency keys where practical
* Authorization checks
* Queue metrics

---

## Security Test Strategy

Security testing will be integrated into normal development.

### Authentication Tests

* Valid user can authenticate
* Invalid password is rejected
* Unknown user produces generic error
* Inactive user is rejected
* Expired token is rejected
* Modified token is rejected
* Missing token is rejected

---

### Authorization Tests

* Viewer cannot create service
* Viewer cannot create incident
* Operations Analyst cannot manage users
* Service Owner cannot edit unrelated service
* Administrator can access user management
* Unauthorized route returns 403
* Frontend hides restricted navigation

---

### Input Validation Tests

* Invalid UUID rejected
* Invalid email rejected
* Oversized strings rejected
* Unsupported status rejected
* Invalid priority rejected
* Invalid URL rejected
* Unsupported protocol rejected
* Duplicate service code rejected

---

### Health Endpoint Security Tests

* `file://` URL rejected
* Loopback endpoint rejected where configured
* Unsupported protocol rejected
* Timeout handled safely
* Oversized response limited
* Excessive redirect chain rejected

---

### Secret Tests

* `.env` not tracked
* Example files contain no real secret
* Gitleaks passes
* Logs omit authorization header
* API responses omit password hash
* Frontend bundle contains no private secret

---

### Container Tests

* Container runs as expected
* Image scan completes
* No unnecessary port exposure
* `.env` absent from image
* Non-root user used where practical

---

### Kubernetes Tests

* Secrets referenced correctly
* ConfigMaps contain no sensitive values
* PostgreSQL not exposed through ingress
* Redis not exposed through ingress
* Probes function correctly
* Security context applies where practical
* Resource limits exist

---

## Security Acceptance Criteria

Security design will be considered successfully implemented when:

* Passwords are never stored as plain text
* bcrypt hashing is used
* Login returns generic invalid-credential messaging
* JWTs are signed and validated
* Expired tokens are rejected
* Modified tokens are rejected
* Protected endpoints require authentication
* Backend services enforce role permissions
* Viewers cannot modify data
* Only administrators can manage roles
* Inactive users cannot authenticate
* Health endpoints are validated before requests execute
* Unsupported URL protocols are rejected
* SQL operations use ORM or parameterized access
* CORS allows approved origins only
* Secure HTTP headers are configured
* Login and selected operations are rate limited
* Request sizes are bounded
* Downstream timeouts are configured
* Secrets are absent from GitHub
* `.env` is excluded from source control
* `.env.example` contains placeholders only
* Kubernetes Secrets hold sensitive configuration
* ConfigMaps contain only non-sensitive values
* PostgreSQL and Redis remain internal
* Logs omit passwords and tokens
* API responses omit internal stack traces
* Audit events record important actions
* Gitleaks scanning is included
* Dependency scanning is included
* Container scanning is included
* Security-focused automated tests pass
* README documentation explains safe local setup
* Demonstration data remains synthetic

---

## Future Security Enhancements

### Enterprise Identity Integration

Future versions may support:

* OAuth 2.0
* OpenID Connect
* SAML
* Microsoft Entra ID
* Okta
* Corporate single sign-on

---

### Multi-Factor Authentication

Future capabilities may include:

* Time-based one-time passwords
* Authenticator applications
* Recovery codes
* Step-up authentication

---

### Refresh Tokens

Future token management may include:

* Short-lived access tokens
* Rotating refresh tokens
* Token revocation
* Redis denylist
* Device-session visibility

---

### Secrets Manager

Future deployments may use:

* HashiCorp Vault
* Azure Key Vault
* AWS Secrets Manager
* Google Secret Manager

---

### Service-to-Service Identity

Future microservice authentication may include:

* Mutual TLS
* Service accounts
* Signed internal tokens
* Service mesh identities
* Workload identity

---

### Network Policies

Future Kubernetes security may add:

* Default-deny policies
* Service-specific ingress rules
* Service-specific egress rules
* Database isolation
* Redis isolation

---

### Policy as Code

Future enhancements may use:

* Open Policy Agent
* Gatekeeper
* Kyverno
* Deployment-policy validation

---

### Web Application Firewall

A production deployment may add:

* Request filtering
* Bot protection
* Rate controls
* Managed threat rules

---

### Security Information and Event Management

Audit events and logs may integrate with:

* Splunk
* Elastic Security
* Microsoft Sentinel
* Datadog
* Other SIEM platforms

---

## Security Responsibilities by Component

| Component | Security Responsibilities |
| --- | --- |
| React Frontend | Safe rendering, protected routes, session clearing, no embedded secrets |
| API Gateway | Rate limiting, headers, CORS, routing, correlation IDs, timeouts |
| Identity Service | Password hashing, login, token issuance, user status, role data |
| Service Registry | Authorization, ownership checks, URL validation, service-data integrity |
| Incident Service | Role enforcement, state-transition validation, audit events |
| Notification Service | Task validation, retry limits, authorization for manual retries |
| Health Worker | SSRF protection, timeouts, response limits, URL validation |
| PostgreSQL | Persistent security-related records and constraints |
| Redis | Internal queueing, rate-limit state, temporary coordination |
| Docker | Isolated packaging and reduced image attack surface |
| Kubernetes | Secret delivery, internal networking, security contexts, resource limits |
| GitHub Actions | Automated security scanning and safe workflow execution |

---

## Security Review Checklist

Before completing each development phase, review:

### Authentication

* Are protected endpoints authenticated?
* Are inactive users rejected?
* Are tokens validated correctly?
* Are passwords excluded from logs?

### Authorization

* Is the backend checking role permissions?
* Are ownership rules enforced?
* Are restricted routes tested?

### Input

* Are all request fields validated?
* Are lengths bounded?
* Are enum values controlled?
* Are URLs validated?

### Secrets

* Are live values excluded from Git?
* Are environment files ignored?
* Are Kubernetes Secrets used correctly?
* Are frontend variables safe to expose?

### Data

* Are ORM methods used?
* Are sensitive fields excluded from responses?
* Are audit events recorded?

### Infrastructure

* Are internal services private?
* Do containers avoid unnecessary privileges?
* Are resource limits present?
* Are images scanned?

### CI/CD

* Does secret scanning run?
* Does dependency scanning run?
* Are workflow permissions minimal?
* Are logs safe?

---

## Final Security Outcome

The completed NEXUS platform will demonstrate that security is integrated throughout the software-development lifecycle.

```text
BUSINESS REQUIREMENTS
        │
        ▼
SECURITY REQUIREMENTS
        │
        ▼
AUTHENTICATION AND AUTHORIZATION
        │
        ▼
SECURE API AND DATA DESIGN
        │
        ▼
SECRET AND CONFIGURATION MANAGEMENT
        │
        ▼
CONTAINER AND KUBERNETES SECURITY
        │
        ▼
SECURITY TESTING AND SCANNING
        │
        ▼
AUDITABLE CLOUD-NATIVE APPLICATION
```

NEXUS will protect:

* User authentication
* User roles
* Service-management functions
* Incident-management functions
* Notification workflows
* Operational data
* Configuration
* Secrets
* Application infrastructure

The project will demonstrate practical security engineering through:

* Secure password hashing
* Signed JWT access tokens
* Role-based access control
* Ownership checks
* Protected APIs
* Input validation
* SQL-injection protection
* SSRF mitigation
* Rate limiting
* Secure headers
* CORS restrictions
* Safe error handling
* Audit logging
* Log redaction
* Secret scanning
* Dependency scanning
* Container scanning
* Kubernetes Secrets
* Internal service networking
* Non-root containers where practical
* Security-focused automated tests

This security design provides the blueprint for building a professional portfolio application that is not only functional and visible, but also intentionally protected, traceable, and maintainable.