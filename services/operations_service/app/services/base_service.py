"""
base_service.py

Generic service layer implementing reusable business operations.

All entity-specific services should inherit from BaseService
and leverage these common CRUD operations.
"""

from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, TypeVar

from sqlalchemy.orm import Session

from ..repositories.base_repository import BaseRepository

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(Generic[RepositoryType]):
    """
    Generic business service.

    Wraps repository operations and serves as the foundation
    for all application services.
    """

    def __init__(self, repository: RepositoryType):
        self.repository = repository

    # ------------------------------------------------------------------
    # READ OPERATIONS
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        db: Session,
        entity_id: Any,
    ):
        """
        Retrieve an entity by primary key.
        """
        return self.repository.get_by_id(db, entity_id)

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Retrieve all entities.
        """
        return self.repository.get_all(
            db=db,
            skip=skip,
            limit=limit,
        )

    def count(
        self,
        db: Session,
    ) -> int:
        """
        Return total entity count.
        """
        return self.repository.count(db)

    def exists(
        self,
        db: Session,
        entity_id: Any,
    ) -> bool:
        """
        Determine whether an entity exists.
        """
        return self.repository.exists(
            db,
            entity_id,
        )

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def create(
        self,
        db: Session,
        obj_in: Dict[str, Any],
    ):
        """
        Create a new entity.
        """
        return self.repository.create(
            db,
            obj_in,
        )

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update(
        self,
        db: Session,
        entity_id: Any,
        obj_in: Dict[str, Any],
    ):
        """
        Update an existing entity.
        """

        db_obj = self.repository.get_by_id(
            db,
            entity_id,
        )

        if db_obj is None:
            raise ValueError(
                f"Entity with id '{entity_id}' was not found."
            )

        return self.repository.update(
            db,
            db_obj,
            obj_in,
        )

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def delete(
        self,
        db: Session,
        entity_id: Any,
    ) -> bool:
        """
        Delete an entity.
        """

        db_obj = self.repository.get_by_id(
            db,
            entity_id,
        )

        if db_obj is None:
            return False

        self.repository.delete(
            db,
            db_obj,
        )

        return True

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------

    def find_by(
        self,
        db: Session,
        **filters,
    ):
        """
        Find entities using equality filters.
        """
        return self.repository.find_by(
            db,
            **filters,
        )

    def first_by(
        self,
        db: Session,
        **filters,
    ):
        """
        Return first matching entity.
        """
        return self.repository.first_by(
            db,
            **filters,
        )

    # ------------------------------------------------------------------
    # PAGINATION
    # ------------------------------------------------------------------

    def paginate(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 25,
    ):
        """
        Return paginated results.
        """
        return self.repository.paginate(
            db=db,
            page=page,
            page_size=page_size,
        )

    # ------------------------------------------------------------------
    # BULK OPERATIONS
    # ------------------------------------------------------------------

    def bulk_create(
        self,
        db: Session,
        objects: List[Dict[str, Any]],
    ):
        """
        Create multiple entities.
        """
        return self.repository.bulk_create(
            db,
            objects,
        )

    def bulk_delete(
        self,
        db: Session,
        ids: List[Any],
    ) -> int:
        """
        Delete multiple entities.
        """
        return self.repository.bulk_delete(
            db,
            ids,
        )

    # ------------------------------------------------------------------
    # SAVE / REFRESH
    # ------------------------------------------------------------------

    def save(
        self,
        db: Session,
        db_obj,
    ):
        """
        Persist changes.
        """
        return self.repository.save(
            db,
            db_obj,
        )

    def refresh(
        self,
        db: Session,
        db_obj,
    ):
        """
        Refresh entity from the database.
        """
        return self.repository.refresh(
            db,
            db_obj,
        )