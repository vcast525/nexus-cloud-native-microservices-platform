"""Generate large-scale service metric data for NEXUS.

Creates:
- 100 categorized demo services
- 300,000 service metric records
- 3,000 observations per service

The generator uses batched SQLAlchemy Core inserts to keep memory
usage controlled and to demonstrate large-scale data engineering.
"""

import argparse
import math
import random
import time
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, func, insert, select

from app.database.session import SessionLocal
from app.models.service import Service
from app.models.service_metric import ServiceMetric


SERVICE_PREFIX = "NEXUS Demo"
DEFAULT_SERVICE_COUNT = 100
DEFAULT_METRIC_COUNT = 300_000
DEFAULT_BATCH_SIZE = 5_000
RANDOM_SEED = 20260717


CATEGORY_PROFILES = {
    "Payments": {
        "business_unit": "Digital Payments",
        "cpu": (42.0, 86.0),
        "memory": (50.0, 88.0),
        "requests": (8_000, 45_000),
        "error_rate": (0.05, 1.80),
        "response_time": (90.0, 420.0),
    },
    "Identity": {
        "business_unit": "Identity and Access Management",
        "cpu": (30.0, 72.0),
        "memory": (40.0, 78.0),
        "requests": (5_000, 35_000),
        "error_rate": (0.02, 1.20),
        "response_time": (55.0, 240.0),
    },
    "Customer": {
        "business_unit": "Customer Experience",
        "cpu": (35.0, 78.0),
        "memory": (45.0, 82.0),
        "requests": (6_000, 38_000),
        "error_rate": (0.08, 2.00),
        "response_time": (80.0, 360.0),
    },
    "Risk": {
        "business_unit": "Enterprise Risk",
        "cpu": (48.0, 92.0),
        "memory": (54.0, 91.0),
        "requests": (2_000, 16_000),
        "error_rate": (0.03, 1.00),
        "response_time": (180.0, 780.0),
    },
    "Fraud": {
        "business_unit": "Fraud Prevention",
        "cpu": (52.0, 95.0),
        "memory": (58.0, 94.0),
        "requests": (4_000, 24_000),
        "error_rate": (0.02, 0.90),
        "response_time": (120.0, 620.0),
    },
    "Analytics": {
        "business_unit": "Data and Analytics",
        "cpu": (55.0, 97.0),
        "memory": (62.0, 96.0),
        "requests": (1_000, 12_000),
        "error_rate": (0.10, 2.40),
        "response_time": (250.0, 1_200.0),
    },
    "Notifications": {
        "business_unit": "Enterprise Messaging",
        "cpu": (25.0, 68.0),
        "memory": (32.0, 72.0),
        "requests": (3_000, 22_000),
        "error_rate": (0.15, 3.20),
        "response_time": (70.0, 310.0),
    },
    "Infrastructure": {
        "business_unit": "Cloud Platform",
        "cpu": (38.0, 88.0),
        "memory": (46.0, 90.0),
        "requests": (4_000, 28_000),
        "error_rate": (0.05, 1.60),
        "response_time": (65.0, 340.0),
    },
    "Compliance": {
        "business_unit": "Compliance Technology",
        "cpu": (32.0, 76.0),
        "memory": (42.0, 84.0),
        "requests": (800, 8_000),
        "error_rate": (0.02, 0.75),
        "response_time": (140.0, 680.0),
    },
    "Reporting": {
        "business_unit": "Enterprise Reporting",
        "cpu": (40.0, 84.0),
        "memory": (50.0, 90.0),
        "requests": (1_200, 10_000),
        "error_rate": (0.08, 1.90),
        "response_time": (190.0, 900.0),
    },
}


def parse_arguments() -> argparse.Namespace:
    """Read command-line options."""

    parser = argparse.ArgumentParser(
        description="Seed categorized NEXUS service metrics."
    )

    parser.add_argument(
        "--records",
        type=int,
        default=DEFAULT_METRIC_COUNT,
        help="Total metric records to generate.",
    )

    parser.add_argument(
        "--services",
        type=int,
        default=DEFAULT_SERVICE_COUNT,
        help="Number of demo services to create.",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Rows inserted in each transaction.",
    )

    parser.add_argument(
        "--reset",
        action="store_true",
        help=(
            "Delete metrics and services previously generated "
            "by this script before reseeding."
        ),
    )

    return parser.parse_args()


def clamp(value: float, low: float, high: float) -> float:
    """Restrict a generated measurement to its valid range."""

    return max(low, min(value, high))


def create_or_load_services(
    session,
    service_count: int,
) -> list[tuple[uuid.UUID, str]]:
    """Create deterministic categorized demo services."""

    categories = list(CATEGORY_PROFILES.keys())
    services: list[tuple[uuid.UUID, str]] = []

    for index in range(service_count):
        category = categories[index % len(categories)]
        number = index + 1
        service_name = (
            f"{SERVICE_PREFIX} {category} Service {number:03d}"
        )

        existing = session.execute(
            select(Service).where(
                Service.service_name == service_name
            )
        ).scalar_one_or_none()

        if existing is not None:
            services.append((existing.id, category))
            continue

        service = Service(
            service_name=service_name,
            description=(
                f"Generated {category.lower()} workload used for "
                "large-scale NEXUS performance analysis."
            ),
            owner=f"{category} Engineering Team",
            business_unit=(
                CATEGORY_PROFILES[category]["business_unit"]
            ),
            environment=(
                "production"
                if number % 5 != 0
                else "staging"
            ),
            status=(
                "degraded"
                if number % 17 == 0
                else "healthy"
            ),
            version=f"v{1 + number % 4}.{number % 10}.0",
            repository_url=(
                "https://github.com/example/"
                f"nexus-{category.lower()}-{number:03d}"
            ),
            is_active=True,
        )

        session.add(service)
        session.flush()
        services.append((service.id, category))

    session.commit()

    return services


def reset_generated_data(session) -> None:
    """Delete only records created by this generator."""

    generated_service_ids = list(
        session.execute(
            select(Service.id).where(
                Service.service_name.like(f"{SERVICE_PREFIX}%")
            )
        ).scalars()
    )

    if not generated_service_ids:
        print("No existing generated data found.")
        return

    session.execute(
        delete(ServiceMetric).where(
            ServiceMetric.service_id.in_(generated_service_ids)
        )
    )

    session.execute(
        delete(Service).where(
            Service.id.in_(generated_service_ids)
        )
    )

    session.commit()

    print(
        "Deleted previously generated service metrics "
        "and demo services."
    )


def generate_metric_row(
    *,
    service_id: uuid.UUID,
    category: str,
    sequence: int,
    base_time: datetime,
) -> dict:
    """Generate one realistic categorized metric observation."""

    profile = CATEGORY_PROFILES[category]

    hour = sequence % 24
    weekday = (sequence // 24) % 7

    business_hour_factor = (
        1.20
        if 8 <= hour <= 18
        else 0.72
    )

    weekend_factor = (
        0.78
        if weekday in (5, 6)
        else 1.0
    )

    traffic_factor = business_hour_factor * weekend_factor

    minimum_requests, maximum_requests = profile["requests"]

    request_count = int(
        random.randint(minimum_requests, maximum_requests)
        * traffic_factor
    )

    baseline_error_rate = random.uniform(
        *profile["error_rate"]
    )

    incident_spike = (
        random.uniform(2.0, 8.0)
        if random.random() < 0.012
        else 0.0
    )

    error_rate = clamp(
        baseline_error_rate + incident_spike,
        0.0,
        100.0,
    )

    error_count = min(
        request_count,
        round(request_count * error_rate / 100),
    )

    cpu_usage = clamp(
        random.uniform(*profile["cpu"])
        * (0.82 + traffic_factor * 0.18)
        + incident_spike,
        0.0,
        100.0,
    )

    memory_usage = clamp(
        random.uniform(*profile["memory"])
        + math.sin(sequence / 48) * 4.0
        + incident_spike * 0.5,
        0.0,
        100.0,
    )

    response_time = max(
        1.0,
        random.uniform(*profile["response_time"])
        * (1.0 + incident_spike / 10.0),
    )

    recorded_at = base_time + timedelta(
        minutes=sequence * 5
    )

    return {
        "id": uuid.uuid4(),
        "service_id": service_id,
        "cpu_usage_percent": round(cpu_usage, 4),
        "memory_usage_percent": round(memory_usage, 4),
        "request_count": request_count,
        "error_count": error_count,
        "error_rate_percent": round(error_rate, 4),
        "average_response_time_ms": round(
            response_time,
            4,
        ),
        "recorded_at": recorded_at,
    }


def seed_metrics(
    session,
    *,
    services: list[tuple[uuid.UUID, str]],
    total_records: int,
    batch_size: int,
) -> None:
    """Insert metric records in bounded batches."""

    if not services:
        raise RuntimeError(
            "At least one registered service is required."
        )

    base_time = datetime.now(timezone.utc) - timedelta(
        days=365
    )

    batch: list[dict] = []
    started_at = time.perf_counter()

    for index in range(total_records):
        service_id, category = services[
            index % len(services)
        ]

        sequence = index // len(services)

        batch.append(
            generate_metric_row(
                service_id=service_id,
                category=category,
                sequence=sequence,
                base_time=base_time,
            )
        )

        if len(batch) >= batch_size:
            session.execute(
                insert(ServiceMetric),
                batch,
            )
            session.commit()
            batch.clear()

            inserted = index + 1
            elapsed = time.perf_counter() - started_at
            rate = inserted / elapsed if elapsed else 0

            print(
                f"Inserted {inserted:,}/{total_records:,} "
                f"records ({rate:,.0f} rows/second)"
            )

    if batch:
        session.execute(
            insert(ServiceMetric),
            batch,
        )
        session.commit()

    elapsed = time.perf_counter() - started_at

    print(
        f"\nCompleted {total_records:,} metric records "
        f"in {elapsed:,.2f} seconds."
    )


def print_database_totals(session) -> None:
    """Print final row counts for verification."""

    generated_services = session.execute(
        select(func.count(Service.id)).where(
            Service.service_name.like(f"{SERVICE_PREFIX}%")
        )
    ).scalar_one()

    total_metrics = session.execute(
        select(func.count(ServiceMetric.id))
    ).scalar_one()

    print("\nDatabase verification")
    print("---------------------")
    print(f"Generated services: {generated_services:,}")
    print(f"Total service metrics: {total_metrics:,}")


def main() -> None:
    """Run the large-scale metric seed operation."""

    args = parse_arguments()

    if args.records < 1:
        raise ValueError("--records must be at least 1")

    if args.services < 1:
        raise ValueError("--services must be at least 1")

    if args.batch_size < 1:
        raise ValueError("--batch-size must be at least 1")

    random.seed(RANDOM_SEED)

    session = SessionLocal()

    try:
        if args.reset:
            reset_generated_data(session)

        services = create_or_load_services(
            session,
            args.services,
        )

        existing_generated_metrics = session.execute(
            select(func.count(ServiceMetric.id))
            .join(
                Service,
                ServiceMetric.service_id == Service.id,
            )
            .where(
                Service.service_name.like(
                    f"{SERVICE_PREFIX}%"
                )
            )
        ).scalar_one()

        if existing_generated_metrics > 0 and not args.reset:
            raise RuntimeError(
                "Generated metrics already exist. "
                "Run again with --reset to replace them."
            )

        print(
            f"Generating {args.records:,} metrics across "
            f"{len(services):,} categorized services."
        )

        print(
            f"Insert batch size: {args.batch_size:,} rows\n"
        )

        seed_metrics(
            session,
            services=services,
            total_records=args.records,
            batch_size=args.batch_size,
        )

        print_database_totals(session)

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
