"""
base_repository.py

Generic SQLAlchemy repository implementing common CRUD operations.

This repository serves as the foundation for all entity-specific
repositories throughout the NEXUS Operations Platform.

All repositories should inherit from BaseRepository and provide
their SQLAlchemy model class.
"""

from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository implementing reusable CRUD operations.

    Example:

        class DeploymentRepository(BaseRepository[Deployment]):
            def __init__(self):
                super().__init__(Deployment)
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # ------------------------------------------------------------------
    # READ OPERATIONS
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        db: Session,
        entity_id: Any,
    ) -> Optional[ModelType]:
        """
        Retrieve a single entity by primary key.
        """
        return (
            db.query(self.model)
            .filter(self.model.id == entity_id)
            .first()
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """
        Retrieve all entities using pagination.
        """
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(
        self,
        db: Session,
    ) -> int:
        """
        Return total row count.
        """
        return (
            db.query(func.count(self.model.id))
            .scalar()
        )

    def exists(
        self,
        db: Session,
        entity_id: Any,
    ) -> bool:
        """
        Determine whether an entity exists.
        """
        return (
            db.query(self.model)
            .filter(self.model.id == entity_id)
            .first()
            is not None
        )

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def create(
        self,
        db: Session,
        obj_in: Dict[str, Any],
    ) -> ModelType:
        """
        Create a new database record.
        """
        db_obj = self.model(**obj_in)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Dict[str, Any],
    ) -> ModelType:
        """
        Update only supplied fields.
        """

        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def delete(
        self,
        db: Session,
        db_obj: ModelType,
    ) -> None:
        """
        Delete an existing entity.
        """
        db.delete(db_obj)
        db.commit()

    # ------------------------------------------------------------------
    # FILTERING
    # ------------------------------------------------------------------

    def find_by(
        self,
        db: Session,
        **filters: Any,
    ) -> List[ModelType]:
        """
        Generic equality filtering.

        Example:

            repository.find_by(
                db,
                status="ACTIVE",
                environment="PRODUCTION"
            )
        """

        query = db.query(self.model)

        for field, value in filters.items():

            if hasattr(self.model, field):
                query = query.filter(
                    getattr(self.model, field) == value
                )

        return query.all()

    def first_by(
        self,
        db: Session,
        **filters: Any,
    ) -> Optional[ModelType]:
        """
        Return first matching record.
        """

        query = db.query(self.model)

        for field, value in filters.items():

            if hasattr(self.model, field):
                query = query.filter(
                    getattr(self.model, field) == value
                )

        return query.first()

    # ------------------------------------------------------------------
    # PAGINATION
    # ------------------------------------------------------------------

    def paginate(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 25,
    ) -> Dict[str, Any]:
        """
        Generic pagination helper.

        Returns:

            {
                "items": [...],
                "page": 1,
                "page_size": 25,
                "total": 143,
                "pages": 6
            }
        """

        total = self.count(db)

        offset = (page - 1) * page_size

        items = (
            db.query(self.model)
            .offset(offset)
            .limit(page_size)
            .all()
        )

        pages = (
            (total + page_size - 1) // page_size
            if total
            else 1
        )

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": pages,
        }

    # ------------------------------------------------------------------
    # BULK OPERATIONS
    # ------------------------------------------------------------------

    def bulk_create(
        self,
        db: Session,
        objects: List[Dict[str, Any]],
    ) -> List[ModelType]:
        """
        Insert multiple records.
        """

        db_objects = [
            self.model(**obj)
            for obj in objects
        ]

        db.add_all(db_objects)
        db.commit()

        for obj in db_objects:
            db.refresh(obj)

        return db_objects

    def bulk_delete(
        self,
        db: Session,
        ids: List[Any],
    ) -> int:
        """
        Delete multiple records.

        Returns number of rows deleted.
        """

        deleted = (
            db.query(self.model)
            .filter(self.model.id.in_(ids))
            .delete(
                synchronize_session=False
            )
        )

        db.commit()

        return deleted

    # ------------------------------------------------------------------
    # UTILITIES
    # ------------------------------------------------------------------

    def refresh(
        self,
        db: Session,
        db_obj: ModelType,
    ) -> ModelType:
        """
        Refresh object from database.
        """

        db.refresh(db_obj)

        return db_obj

    def save(
        self,
        db: Session,
        db_obj: ModelType,
    ) -> ModelType:
        """
        Persist changes.
        """

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj