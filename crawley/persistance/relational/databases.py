import panacea
from panacea import Field, Unicode, UnicodeText

session = panacea.session


class Entity(panacea.EntityBase):
    """
        Base Entity.

        Every Crawley's Entity must Inherit from this class
    """

    __metaclass__ = panacea.EntityMeta


class UrlEntity(panacea.EntityBase):
    """
        Entity intended to save urls
    """

    href = Field(Unicode(255))
    parent = Field(Unicode(255))

    __metaclass__ = panacea.EntityMeta


def setup(entities):
    """
        Setup the database based on a list of user's entities
    """

    panacea.setup_entities(entities)
    panacea.create_all()
