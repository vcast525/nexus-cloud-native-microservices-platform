"""Generate large-scale categorized API health-check data for NEXUS."""

import argparse
import random
import time
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, func, insert, select

from app.database.session import SessionLocal
from app.models.api_health import APIHealth
from app.models.service import Service


DEFAULT_RECORD_COUNT = 120_000
DEFAULT_BATCH_SIZE = 5_000
RANDOM_SEED = 20260718
SERVICE_PREFIX = "NEXUS Demo"

ENDPOINTS = (
    "/health",
    "/ready",
    "/api/v1/status",
    "/api/v1/customers",
    "/api/v1/payments",
    "/api/v1/authenticate",
    "/api/v1/reports",
)

HTTP_METHODS = {
    "/health": "GET",
    "/ready": "GET",
    "/api/v1/status": "GET",
    "/api/v1/customers": "GET",
    "/api/v1/payments": "POST",
    "/api/v1/authenticate": "POST",
    "/api/v1/reports": "GET",
}


def parse_arguments() -> argparse.Namespace:
    """Read command-line options."""

    parser = argparse.ArgumentParser(
        description="Seed categorized NEXUS API health checks."
    )

    parser.add_argument(
        "--records",
        type=int,
        default=DEFAULT_RECORD_COUNT,
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
    )

    parser.add_argument(
        "--reset",
        action="store_true",
    )

    return parser.parse_args()


def load_demo_services(session) -> list[uuid.UUID]:
    """Load the existing NEXUS demo-service identifiers."""

    service_ids = list(
        session.execute(
            select(Service.id)
            .where(Service.service_name.like(f"{SERVICE_PREFIX}%"))
            .order_by(Service.service_name)
        ).scalars()
    )

    if not service_ids:
        raise RuntimeError(
            "No NEXUS demo services were found. "
            "Seed service metrics first."
        )

    return service_ids


def reset_generated_health_checks(
    session,
    service_ids: list[uuid.UUID],
) -> None:
    """Delete generated health checks without touching other data."""

    session.execute(
        delete(APIHealth).where(
            APIHealth.service_id.in_(service_ids)
        )
    )
    session.commit()

    print("Deleted previously generated API health checks.")


def generate_health_row(
    *,
    service_id: uuid.UUID,
    index: int,
    base_time: datetime,
) -> dict:
    """Generate one realistic API health-check observation."""

    endpoint = ENDPOINTS[index % len(ENDPOINTS)]
    checked_at = base_time + timedelta(minutes=index * 3)

    hour = checked_at.hour
    weekday = checked_at.weekday()

    is_business_hour = 8 <= hour <= 18
    is_weekend = weekday >= 5
    is_maintenance_window = weekday == 6 and 2 <= hour <= 4

    failure_probability = 0.012
    degraded_probability = 0.055

    if is_business_hour:
        degraded_probability += 0.025

    if is_weekend:
        failure_probability -= 0.003

    if is_maintenance_window:
        failure_probability += 0.11
        degraded_probability += 0.18

    outcome = random.random()

    if outcome < failure_probability:
        status = "failed"
        status_code = random.choice([500, 502, 503, 504])
        response_time_ms = random.uniform(1_500.0, 5_000.0)
        availability_percent = random.uniform(82.0, 96.5)

    elif outcome < failure_probability + degraded_probability:
        status = "degraded"
        status_code = random.choice([200, 429, 503])
        response_time_ms = random.uniform(600.0, 1_800.0)
        availability_percent = random.uniform(96.5, 99.5)

    else:
        status = "healthy"
        status_code = random.choice([200, 200, 200, 204])
        response_time_ms = random.uniform(
            35.0 if not is_business_hour else 55.0,
            420.0 if not is_business_hour else 650.0,
        )
        availability_percent = random.uniform(99.5, 100.0)

    return {
        "id": uuid.uuid4(),
        "service_id": service_id,
        "endpoint": endpoint,
        "http_method": HTTP_METHODS[endpoint],
        "status": status,
        "status_code": status_code,
        "response_time_ms": round(response_time_ms, 4),
        "availability_percent": round(
            availability_percent,
            4,
        ),
        "checked_at": checked_at,
    }


def seed_health_checks(
    session,
    *,
    service_ids: list[uuid.UUID],
    total_records: int,
    batch_size: int,
) -> None:
    """Insert health-check records in controlled batches."""

    base_time = datetime.now(timezone.utc) - timedelta(days=250)
    batch: list[dict] = []
    started_at = time.perf_counter()

    for index in range(total_records):
        service_id = service_ids[index % len(service_ids)]

        batch.append(
            generate_health_row(
                service_id=service_id,
                index=index,
                base_time=base_time,
            )
        )

        if len(batch) >= batch_size:
            session.execute(insert(APIHealth), batch)
            session.commit()
            batch.clear()

            inserted = index + 1
            elapsed = time.perf_counter() - started_at
            rate = inserted / elapsed if elapsed else 0

            print(
                f"Inserted {inserted:,}/{total_records:,} "
                f"health checks ({rate:,.0f} rows/second)"
            )

    if batch:
        session.execute(insert(APIHealth), batch)
        session.commit()

    elapsed = time.perf_counter() - started_at

    print(
        f"\nCompleted {total_records:,} API health checks "
        f"in {elapsed:,.2f} seconds."
    )


def print_totals(session) -> None:
    """Print database verification totals."""

    total = session.execute(
        select(func.count(APIHealth.id))
    ).scalar_one()

    healthy = session.execute(
        select(func.count(APIHealth.id)).where(
            APIHealth.status == "healthy"
        )
    ).scalar_one()

    degraded = session.execute(
        select(func.count(APIHealth.id)).where(
            APIHealth.status == "degraded"
        )
    ).scalar_one()

    failed = session.execute(
        select(func.count(APIHealth.id)).where(
            APIHealth.status == "failed"
        )
    ).scalar_one()

    print("\nDatabase verification")
    print("---------------------")
    print(f"Total API health checks: {total:,}")
    print(f"Healthy: {healthy:,}")
    print(f"Degraded: {degraded:,}")
    print(f"Failed: {failed:,}")


def main() -> None:
    """Run the API health seed operation."""

    args = parse_arguments()

    if args.records < 1:
        raise ValueError("--records must be at least 1")

    if args.batch_size < 1:
        raise ValueError("--batch-size must be at least 1")

    random.seed(RANDOM_SEED)
    session = SessionLocal()

    try:
        service_ids = load_demo_services(session)

        existing_count = session.execute(
            select(func.count(APIHealth.id)).where(
                APIHealth.service_id.in_(service_ids)
            )
        ).scalar_one()

        if args.reset:
            reset_generated_health_checks(
                session,
                service_ids,
            )
        elif existing_count > 0:
            raise RuntimeError(
                "Generated API health checks already exist. "
                "Run again with --reset to replace them."
            )

        print(
            f"Generating {args.records:,} API health checks "
            f"across {len(service_ids):,} services."
        )
        print(f"Batch size: {args.batch_size:,}\n")

        seed_health_checks(
            session,
            service_ids=service_ids,
            total_records=args.records,
            batch_size=args.batch_size,
        )

        print_totals(session)

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
