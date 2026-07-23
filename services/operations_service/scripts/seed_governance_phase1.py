"""Seed a small interconnected Operational Governance dataset.

Phase 1 creates:

- 5 services, only when the database does not already contain enough services
- 10 incidents
- 8 issues
- 10 changes
- 8 risk assessments

The script uses existing services whenever possible and creates relationships
between incidents, issues, changes, and risk assessments.

Run from the operations_service project root:

    python scripts/seed_governance_phase1.py
"""

import sys
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

from sqlalchemy import func

# Allow the script to import the app package when executed directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database.session import SessionLocal
from app.models.change import Change
from app.models.incident import Incident
from app.models.issue import Issue
from app.models.risk_assessment import RiskAssessment
from app.models.service import Service


PHASE_ONE_PREFIX = "P1-"

SERVICE_NAMES = [
    "NEXUS Identity Gateway",
    "NEXUS Payment Orchestrator",
    "NEXUS Customer Profile",
    "NEXUS Notification Hub",
    "NEXUS Reporting Engine",
]

SERVICE_OWNERS = [
    "Identity Engineering",
    "Payments Engineering",
    "Customer Platforms",
    "Communications Engineering",
    "Data Intelligence",
]

BUSINESS_UNITS = [
    "Enterprise Security",
    "Digital Payments",
    "Customer Experience",
    "Shared Technology",
    "Enterprise Analytics",
]

INCIDENT_TITLES = [
    "Authentication latency exceeded production threshold",
    "Payment-processing requests experienced elevated failures",
    "Customer profile synchronization became delayed",
    "Notification delivery queue accumulated a large backlog",
    "Reporting queries exceeded expected response time",
    "Identity-token validation returned intermittent errors",
    "Payment reconciliation job failed during overnight processing",
    "Customer preference updates were temporarily unavailable",
    "Outbound email provider experienced degraded connectivity",
    "Analytics export process exhausted available worker capacity",
]

ISSUE_TITLES = [
    "Improve authentication cache invalidation",
    "Add payment-provider circuit breaker",
    "Optimize profile synchronization batching",
    "Increase notification worker resilience",
    "Add reporting-query timeout controls",
    "Strengthen token-validation retry handling",
    "Improve reconciliation-job recovery",
    "Add capacity controls to analytics exports",
]

CHANGE_TITLES = [
    "Deploy authentication cache correction",
    "Enable payment-provider circuit breaker",
    "Release profile synchronization optimization",
    "Increase notification worker capacity",
    "Deploy reporting timeout configuration",
    "Update token-validation retry policy",
    "Release reconciliation recovery workflow",
    "Deploy analytics export capacity controls",
    "Rotate production authentication credentials",
    "Upgrade shared observability agents",
]

RISK_TITLES = [
    "Authentication service availability assessment",
    "Payment processing resilience assessment",
    "Customer data synchronization risk review",
    "Notification delivery continuity assessment",
    "Reporting platform performance assessment",
    "Token-validation control assessment",
    "Payment reconciliation operational risk review",
    "Analytics export capacity assessment",
]


def phase_one_data_exists(session) -> bool:
    """Return True when Phase 1 governance records already exist."""

    incident_count = (
        session.query(func.count(Incident.id))
        .filter(Incident.incident_number.like(f"{PHASE_ONE_PREFIX}%"))
        .scalar()
    )

    issue_count = (
        session.query(func.count(Issue.id))
        .filter(Issue.issue_number.like(f"{PHASE_ONE_PREFIX}%"))
        .scalar()
    )

    change_count = (
        session.query(func.count(Change.id))
        .filter(Change.change_number.like(f"{PHASE_ONE_PREFIX}%"))
        .scalar()
    )

    risk_count = (
        session.query(func.count(RiskAssessment.id))
        .filter(RiskAssessment.assessment_number.like(f"{PHASE_ONE_PREFIX}%"))
        .scalar()
    )

    return any(
        count > 0
        for count in (
            incident_count,
            issue_count,
            change_count,
            risk_count,
        )
    )


def get_or_create_services(session) -> list[Service]:
    """Use five existing services or create enough services for the test."""

    services = (
        session.query(Service)
        .order_by(Service.created_at.asc())
        .limit(5)
        .all()
    )

    if len(services) >= 5:
        print("Using 5 existing services.")
        return services

    existing_names = {
        service.service_name
        for service in session.query(Service).all()
    }

    for index, service_name in enumerate(SERVICE_NAMES):
        if len(services) >= 5:
            break

        if service_name in existing_names:
            existing_service = (
                session.query(Service)
                .filter(Service.service_name == service_name)
                .one()
            )
            services.append(existing_service)
            continue

        service = Service(
            service_name=service_name,
            description=(
                "Phase 1 test service used to validate the NEXUS "
                "Operational Governance domain."
            ),
            owner=SERVICE_OWNERS[index],
            business_unit=BUSINESS_UNITS[index],
            environment="production",
            status="healthy",
            version=f"1.{index + 1}.0",
            repository_url=(
                f"https://github.com/nexus-platform/"
                f"{service_name.lower().replace(' ', '-')}"
            ),
            is_active=True,
        )

        session.add(service)
        services.append(service)
        existing_names.add(service_name)

    session.flush()

    print(f"Using {len(services)} services.")
    return services


def create_incidents(
    session,
    services: list[Service],
    base_time: datetime,
) -> list[Incident]:
    """Create ten incidents connected to the selected services."""

    incidents = []

    severities = [
        "Critical",
        "High",
        "Medium",
        "Low",
        "High",
        "Medium",
        "Critical",
        "Low",
        "High",
        "Medium",
    ]

    priorities = [
        "P1",
        "P1",
        "P2",
        "P3",
        "P2",
        "P2",
        "P1",
        "P3",
        "P2",
        "P2",
    ]

    statuses = [
        "Resolved",
        "Resolved",
        "Monitoring",
        "Resolved",
        "Investigating",
        "Resolved",
        "Resolved",
        "Closed",
        "Monitoring",
        "Investigating",
    ]

    for index in range(10):
        started_at = base_time - timedelta(days=30 - index * 2)
        detected_at = started_at + timedelta(minutes=4 + index)
        acknowledged_at = detected_at + timedelta(minutes=5)
        is_resolved = statuses[index] in {"Resolved", "Closed"}
        resolved_at = (
            acknowledged_at + timedelta(minutes=35 + index * 8)
            if is_resolved
            else None
        )

        duration_minutes = (
            int((resolved_at - started_at).total_seconds() / 60)
            if resolved_at
            else None
        )

        incident = Incident(
            incident_number=f"{PHASE_ONE_PREFIX}INC-{index + 1:06d}",
            service_id=services[index % len(services)].id,
            title=INCIDENT_TITLES[index],
            description=(
                "Phase 1 operational incident generated to verify database "
                "relationships, constraints, indexes, and API behavior."
            ),
            incident_type=[
                "Availability",
                "Performance",
                "Data Synchronization",
                "Capacity",
                "Reliability",
            ][index % 5],
            severity=severities[index],
            priority=priorities[index],
            status=statuses[index],
            assigned_team=SERVICE_OWNERS[index % len(SERVICE_OWNERS)],
            detected_by=[
                "Automated Monitoring",
                "Synthetic Test",
                "Application Alert",
                "Operations Center",
            ][index % 4],
            root_cause=(
                "Configuration and capacity conditions caused temporary "
                "service degradation."
                if is_resolved
                else None
            ),
            customer_impact=(
                "A subset of users experienced delayed or failed requests."
            ),
            resolution_summary=(
                "The engineering team stabilized the service and verified "
                "normal production behavior."
                if is_resolved
                else None
            ),
            correlation_id=uuid.uuid4(),
            started_at=started_at,
            detected_at=detected_at,
            acknowledged_at=acknowledged_at,
            resolved_at=resolved_at,
            duration_minutes=duration_minutes,
            sla_breached=severities[index] in {"Critical", "High"},
        )

        session.add(incident)
        incidents.append(incident)

    session.flush()
    return incidents


def create_issues(
    session,
    incidents: list[Incident],
    base_time: datetime,
) -> list[Issue]:
    """Create eight issues connected to incidents and services."""

    issues = []

    for index in range(8):
        incident = incidents[index]
        created_at = incident.detected_at + timedelta(hours=2)
        target_date = created_at + timedelta(days=14 + index)

        issue = Issue(
            issue_number=f"{PHASE_ONE_PREFIX}ISS-{index + 1:06d}",
            service_id=incident.service_id,
            incident_id=incident.id,
            title=ISSUE_TITLES[index],
            description=(
                "Engineering issue opened after incident review to track "
                "corrective and preventive work."
            ),
            issue_type=[
                "Defect",
                "Resilience Improvement",
                "Performance Improvement",
                "Control Enhancement",
            ][index % 4],
            severity=[
                "Critical",
                "High",
                "Medium",
                "High",
                "Medium",
                "High",
                "Critical",
                "Medium",
            ][index],
            priority=[
                "P1",
                "P1",
                "P2",
                "P2",
                "P2",
                "P2",
                "P1",
                "P3",
            ][index],
            status=[
                "Closed",
                "In Progress",
                "Open",
                "Closed",
                "In Progress",
                "Closed",
                "Open",
                "In Progress",
            ][index],
            assigned_team=SERVICE_OWNERS[index % len(SERVICE_OWNERS)],
            owner=f"engineer{index + 1}@nexus.local",
            remediation_plan=(
                "Implement the corrective change, validate it in a controlled "
                "environment, deploy it, and monitor production results."
            ),
            estimated_effort_hours=float(12 + index * 4),
            actual_effort_hours=(
                float(10 + index * 3)
                if index in {0, 3, 5}
                else None
            ),
            target_resolution_date=target_date,
            actual_resolution_date=(
                target_date - timedelta(days=2)
                if index in {0, 3, 5}
                else None
            ),
            overdue=index == 6,
            correlation_id=uuid.uuid4(),
            created_at=created_at,
            updated_at=base_time,
        )

        session.add(issue)
        issues.append(issue)

    session.flush()
    return issues


def create_changes(
    session,
    services: list[Service],
    issues: list[Issue],
    base_time: datetime,
) -> list[Change]:
    """Create ten changes, eight linked to issues and two service-only."""

    changes = []

    for index in range(10):
        issue = issues[index] if index < len(issues) else None
        service = (
            services[index % len(services)]
            if issue is None
            else None
        )

        planned_start = base_time + timedelta(days=index + 1)
        planned_end = planned_start + timedelta(hours=2)

        completed = index in {0, 3, 5}
        actual_start = (
            planned_start + timedelta(minutes=5)
            if completed
            else None
        )
        actual_end = (
            actual_start + timedelta(minutes=65)
            if actual_start
            else None
        )

        change = Change(
            change_number=f"{PHASE_ONE_PREFIX}CHG-{index + 1:06d}",
            service_id=(
                issue.service_id
                if issue is not None
                else service.id
            ),
            issue_id=issue.id if issue is not None else None,
            title=CHANGE_TITLES[index],
            description=(
                "Controlled Phase 1 production change generated to validate "
                "the NEXUS change-management workflow."
            ),
            change_type=(
                "Emergency"
                if index == 1
                else "Normal"
            ),
            change_category=[
                "Application",
                "Infrastructure",
                "Configuration",
                "Security",
            ][index % 4],
            status=(
                "Completed"
                if completed
                else [
                    "Scheduled",
                    "Pending Approval",
                    "Approved",
                ][index % 3]
            ),
            approval_status=(
                "Approved"
                if completed or index % 3 != 1
                else "Pending"
            ),
            risk_level=[
                "Low",
                "High",
                "Medium",
                "Medium",
                "Low",
                "Medium",
                "High",
                "Medium",
                "Low",
                "Medium",
            ][index],
            business_justification=(
                "Reduce operational risk and improve production-service "
                "reliability."
            ),
            implementation_plan=(
                "Deploy the approved release, execute validation checks, "
                "and monitor service health."
            ),
            validation_plan=(
                "Run automated smoke tests, health checks, and operational "
                "metric validation."
            ),
            rollback_plan=(
                "Restore the previous release and configuration if validation "
                "criteria are not met."
            ),
            implementation_team=SERVICE_OWNERS[index % len(SERVICE_OWNERS)],
            requested_by=f"requester{index + 1}@nexus.local",
            approved_by=(
                f"approver{index + 1}@nexus.local"
                if completed or index % 3 != 1
                else None
            ),
            approval_notes=(
                "Approved after technical and operational review."
                if completed or index % 3 != 1
                else None
            ),
            planned_start_at=planned_start,
            planned_end_at=planned_end,
            actual_start_at=actual_start,
            actual_end_at=actual_end,
            outage_required=index in {1, 6},
            outage_duration_minutes=(
                "30"
                if index in {1, 6}
                else None
            ),
            implementation_successful=completed,
            rollback_required=False,
            rollback_completed=False,
            post_implementation_review=(
                "Implementation completed successfully with no material "
                "production impact."
                if completed
                else None
            ),
            customer_notification_sent=index in {1, 6},
            emergency_change=index == 1,
            correlation_id=uuid.uuid4(),
            created_at=base_time - timedelta(days=10 - index),
            updated_at=base_time,
        )

        session.add(change)
        changes.append(change)

    session.flush()
    return changes


def create_risk_assessments(
    session,
    issues: list[Issue],
    base_time: datetime,
) -> list[RiskAssessment]:
    """Create eight risk assessments linked to the eight issues."""

    risk_assessments = []

    for index in range(8):
        issue = issues[index]

        likelihood_score = [5, 4, 3, 4, 3, 4, 5, 3][index]
        impact_score = [5, 5, 4, 4, 3, 4, 5, 4][index]
        inherent_score = float(likelihood_score * impact_score)
        control_effectiveness = [70, 55, 65, 75, 80, 60, 45, 70][index]
        residual_score = round(
            inherent_score * (1 - control_effectiveness / 100),
            2,
        )

        if residual_score >= 12:
            rating = "Critical"
        elif residual_score >= 8:
            rating = "High"
        elif residual_score >= 4:
            rating = "Medium"
        else:
            rating = "Low"

        assessment = RiskAssessment(
            assessment_number=f"{PHASE_ONE_PREFIX}RSK-{index + 1:06d}",
            service_id=issue.service_id,
            issue_id=issue.id,
            title=RISK_TITLES[index],
            description=(
                "Phase 1 operational risk assessment generated to validate "
                "risk scoring and governance relationships."
            ),
            assessment_type=[
                "Operational Risk",
                "Technology Risk",
                "Resilience Risk",
                "Control Assessment",
            ][index % 4],
            status=[
                "Approved",
                "Under Review",
                "Open",
                "Approved",
                "Monitoring",
                "Approved",
                "Escalated",
                "Under Review",
            ][index],
            methodology="Likelihood and Impact Matrix",
            risk_owner=SERVICE_OWNERS[index % len(SERVICE_OWNERS)],
            business_owner=BUSINESS_UNITS[index % len(BUSINESS_UNITS)],
            assessed_by=f"risk.analyst{index + 1}@nexus.local",
            likelihood_score=likelihood_score,
            impact_score=impact_score,
            inherent_risk_score=inherent_score,
            control_effectiveness=control_effectiveness,
            residual_risk_score=residual_score,
            overall_risk_rating=rating,
            risk_statement=(
                "If the identified service weakness is not remediated, "
                "customers and business operations may experience disruption."
            ),
            key_controls=(
                "Automated monitoring, alerting, deployment approval, "
                "incident response, and recovery procedures."
            ),
            identified_gaps=(
                "Additional resilience automation and control evidence are "
                "required."
            ),
            mitigation_strategy=(
                "Complete the linked engineering issue and validate the "
                "resulting production change."
            ),
            action_plan=(
                "Track remediation through implementation and conduct a "
                "follow-up risk review."
            ),
            target_completion_date=base_time + timedelta(days=30 + index),
            next_review_date=base_time + timedelta(days=45 + index * 2),
            last_review_date=base_time - timedelta(days=5 + index),
            risk_accepted=rating in {"Low", "Medium"},
            executive_approval=rating in {"Critical", "High"},
            correlation_id=uuid.uuid4(),
            created_at=base_time - timedelta(days=15 - index),
            updated_at=base_time,
        )

        session.add(assessment)
        risk_assessments.append(assessment)

    session.flush()
    return risk_assessments


def print_summary(session) -> None:
    """Print Phase 1 record totals after insertion."""

    incident_count = (
        session.query(func.count(Incident.id))
        .filter(Incident.incident_number.like(f"{PHASE_ONE_PREFIX}%"))
        .scalar()
    )

    issue_count = (
        session.query(func.count(Issue.id))
        .filter(Issue.issue_number.like(f"{PHASE_ONE_PREFIX}%"))
        .scalar()
    )

    change_count = (
        session.query(func.count(Change.id))
        .filter(Change.change_number.like(f"{PHASE_ONE_PREFIX}%"))
        .scalar()
    )

    risk_count = (
        session.query(func.count(RiskAssessment.id))
        .filter(RiskAssessment.assessment_number.like(f"{PHASE_ONE_PREFIX}%"))
        .scalar()
    )

    print("\nPhase 1 seed completed successfully.")
    print("------------------------------------")
    print(f"Incidents:        {incident_count}")
    print(f"Issues:           {issue_count}")
    print(f"Changes:          {change_count}")
    print(f"Risk assessments: {risk_count}")
    print(f"Governance total: {incident_count + issue_count + change_count + risk_count}")


def main() -> None:
    """Execute the Phase 1 seed transaction."""

    session = SessionLocal()

    try:
        print("Starting NEXUS Operational Governance Phase 1 seed...")

        if phase_one_data_exists(session):
            print(
                "\nPhase 1 records already exist. No new records were added."
            )
            print(
                "This protection prevents duplicate incident, issue, change, "
                "and risk-assessment numbers."
            )
            return

        base_time = datetime.now(UTC)

        services = get_or_create_services(session)

        incidents = create_incidents(
            session=session,
            services=services,
            base_time=base_time,
        )

        issues = create_issues(
            session=session,
            incidents=incidents,
            base_time=base_time,
        )

        create_changes(
            session=session,
            services=services,
            issues=issues,
            base_time=base_time,
        )

        create_risk_assessments(
            session=session,
            issues=issues,
            base_time=base_time,
        )

        session.commit()
        print_summary(session)

    except Exception as exc:
        session.rollback()
        print("\nPhase 1 seed failed. The transaction was rolled back.")
        print(f"Error: {exc}")
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()