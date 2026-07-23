# NEXUS Operations Service

The Operations Service manages the operational data used by the NEXUS platform.

## Responsibilities

- Maintain the enterprise service registry
- Track operational incidents
- Store API health-check results
- Store historical performance metrics
- Supply operational data to dashboard and analytics APIs

## Database Ownership

The service uses the following PostgreSQL schemas:

- `registry`
- `incidents`
