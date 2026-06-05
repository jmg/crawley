"""Relational persistence based on SQLAlchemy 2.x.

This module replaces the old ``elixir`` layer. User entities inherit from
:class:`Entity`; instantiating an entity automatically stages it in the
shared session, mirroring the original elixir behaviour::

    class Package(Entity):
        package = Field(Unicode(255))

    Package(package="crawley")   # staged in the session
    session.commit()
"""

from sqlalchemy import Column, Integer, Unicode, UnicodeText, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    scoped_session,
    sessionmaker,
)

#: The shared session used across the framework.
session = scoped_session(sessionmaker())

_engine = None


def Field(*args, **kwargs):
    """Shim mapping the old ``elixir.Field`` to a SQLAlchemy ``Column``."""
    return Column(*args, **kwargs)


class Base(DeclarativeBase):
    """Declarative base holding the metadata for every entity."""


class Entity(Base):
    """Base class for every crawley entity.

    Instances are added to the shared :data:`session` on construction.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls):  # noqa: N805
        return cls.__name__.lower()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        session.add(self)


class UrlEntity(Entity):
    """An entity intended to store urls."""

    __abstract__ = True

    href = Column(Unicode(255))
    parent = Column(Unicode(255))


def setup(connection_string, echo=False):
    """Create the engine, bind the session and create the tables."""
    global _engine
    _engine = create_engine(connection_string, echo=echo)
    # Drop any session already checked out from the scoped registry so the new
    # bind actually takes effect (configure() can't rebind live sessions).
    session.remove()
    session.configure(bind=_engine)
    Base.metadata.create_all(_engine)
    return _engine


__all__ = [
    "session",
    "Field",
    "Unicode",
    "UnicodeText",
    "Base",
    "Entity",
    "UrlEntity",
    "setup",
]
